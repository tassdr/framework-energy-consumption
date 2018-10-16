import os.path as op
import os
from subprocess import Popen, PIPE
import time
import timeit
from util import makedirs, load_json
import csv

from Profiler import Profiler
import paths
import Tests
import Parser


class Batterystats(Profiler):
    def __init__(self, config):
        super(Batterystats, self).__init__(config)
        self.profile = False
        self.cleanup = config.get('cleanup')

        # "config" only passes the fields under "profilers", so config.json is loaded again for the fields below
        config_file = load_json(op.join(paths.CONFIG_DIR, 'config.json'))
        self.type = config_file['type']
        self.systrace = config_file.get('systrace_path', 'systrace')
        self.powerprofile = config_file['powerprofile_path']
        self.duration = Tests.is_integer(config_file.get('duration', 0)) / 1000

    def start_profiling(self, device, **kwargs):
        # Reset logs on the device
        device.shell('dumpsys batterystats --reset')
        device.shell('logcat -c')
        print('Batterystats cleared')
        print('Logcat cleared')

        # Create output directories
        global app
        global systrace_file
        global logcat_file
        global batterystats_file
        global results_file
        output_dir = op.join(paths.OUTPUT_DIR, 'android/')
        makedirs(output_dir)

        if self.type == 'native':
            app = kwargs.get('app', None)
        # TODO: add support for other browsers, required form: app = 'package.name'
        elif self.type == 'web':
            app = 'com.android.chrome'

        # Create files on system
        systrace_file = '{}systrace_{}_{}.html'.format(output_dir, device.id, time.strftime('%Y.%m.%d_%H%M%S'))
        logcat_file = '{}logcat_{}_{}.txt'.format(output_dir, device.id, time.strftime('%Y.%m.%d_%H%M%S'))
        batterystats_file = op.join(output_dir, 'batterystats_history_{}_{}.txt'.format(device.id, time.strftime(
            '%Y.%m.%d_%H%M%S')))
        results_file = op.join(output_dir, 'results_{}_{}.csv'
                               .format(device.id, time.strftime('%Y.%m.%d_%H%M%S')))

        super(Batterystats, self).start_profiling(device, **kwargs)
        self.profile = True
        self.get_data(device, app)

    def get_data(self, device, app):
        """Runs the systrace method for self.duration seconds in a separate thread"""
        # TODO: Check if 'systrace freq idle' is supported by the device
        global sysproc
        sysproc = Popen('{} freq idle -e {} -a {} -t {} -b 50000 -o {}'.format
              (self.systrace, device.id, app, int(self.duration + 5), systrace_file), shell=True)

    def stop_profiling(self, device, **kwargs):
        super(Batterystats, self).stop_profiling(device, **kwargs)
        self.profile = False

    def collect_results(self, device, path=None):
        # Pull logcat file from device
        device.shell('logcat -f /mnt/sdcard/logcat.txt -d')
        device.pull('/mnt/sdcard/logcat.txt', logcat_file)
        device.shell('rm -f /mnt/sdcard/logcat.txt')

        # Get BatteryStats data
        with open(batterystats_file, 'w+') as f:
            f.write(device.shell('dumpsys batterystats --history'))
        batterystats_results = Parser.parse_batterystats(app, batterystats_file, self.powerprofile)

        # Estimate total consumption
        charge = device.shell('dumpsys batterystats | grep "Computed drain:"').split(',')[1].split(':')[1]
        volt = device.shell('dumpsys batterystats | grep "volt="').split('volt=')[1].split()[0]
        energy_consumed = (float(charge) / 1000) * (float(volt) / 1000.0) * 3600.0

        # Wait for Systrace file finalisation before parsing
        sysproc.wait()
        cores = int(device.shell('cat /proc/cpuinfo | grep processor | wc -l'))
        systrace_results = Parser.parse_systrace(app, systrace_file, logcat_file, batterystats_file, self.powerprofile, cores)

        with open(results_file, 'w+') as results:
            writer = csv.writer(results, delimiter="\n")
            writer.writerow(['Start Time (Seconds),End Time (Seconds),Duration (Seconds),Component,Energy Consumption (Joule)'])
            writer.writerow(batterystats_results)
            writer.writerow(systrace_results)
            writer.writerow([''])
            writer.writerow(['Android Internal Estimation:,{}'.format(energy_consumed)])

        # Remove log files
        if self.cleanup is True:
            os.remove(systrace_file)
            os.remove(logcat_file)
            os.remove(batterystats_file)
