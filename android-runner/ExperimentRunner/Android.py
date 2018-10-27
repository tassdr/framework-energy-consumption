import os.path as op
import time
from util import makedirs
import timeit
import threading
import csv

from Profiler import Profiler
import paths
import Tests


class Android(Profiler):
    def __init__(self, config):
        super(Android, self).__init__(config)
        self.profile = False
        available_data_points = ['cpu', 'mem']
        self.interval = float(Tests.is_integer(config.get('sample_interval', 0))) / 1000
        self.data_points = config['data_points']
        invalid_data_points = [dp for dp in config['data_points'] if dp not in set(available_data_points)]
        if invalid_data_points:
            self.logger.warning('Invalid data points in config: {}'.format(invalid_data_points))
        self.data_points = [dp for dp in config['data_points'] if dp in set(available_data_points)]
        self.data = [['datetime'] + self.data_points]

    def get_cpu_usage(self, device):
        """Get CPU usage in percentage"""
        #return device.shell('dumpsys cpuinfo | grep TOTAL | cut -d" " -f1').strip()[:-1]
        return device.shell('dumpsys cpuinfo | grep TOTAL').split('%')[0]

    def get_mem_usage(self, device, app):
        """Get memory usage in KB for app, if app is None system usage is used"""
        if not app:
            # return device.shell('dumpsys meminfo | grep Used | cut -d" " -f5').strip()[1:-1]
            # return device.shell('dumpsys meminfo | grep Used').split()[2].strip()[1:-1].replace(",", ".")
            return device.shell('dumpsys meminfo | grep Used').translate(None, '(kB,K').split()[2]
        else:
            result = device.shell('dumpsys meminfo {} | grep TOTAL'.format(app))
            if 'No process found' in result:
                raise Exception('Android Profiler: {}'.format(result))
            return ' '.join(result.strip().split()).split()[1]

    def start_profiling(self, device, **kwargs):
        super(Android, self).start_profiling(device, **kwargs)
        self.profile = True
        app = kwargs.get('app', None)
        self.get_data(device, app)

    def get_data(self, device, app):
        """Runs the profiling methods every self.interval seconds in a separate thread"""
        start = timeit.default_timer()
        device_time = device.shell('date -u')
        row = [device_time]
        if 'cpu' in self.data_points:
            row.append(self.get_cpu_usage(device))
        if 'mem' in self.data_points:
            row.append(self.get_mem_usage(device, app))
        self.data.append(row)
        end = timeit.default_timer()
        # timer results could be negative
        interval = max(float(0), self.interval - max(0, end - start))
        if self.profile:
            threading.Timer(interval, self.get_data, args=(device, app)).start()

    def stop_profiling(self, device, **kwargs):
        super(Android, self).stop_profiling(device, **kwargs)
        self.profile = False

    def collect_results(self, device, path=None):
        super(Android, self).collect_results(device)
        output_dir = op.join(paths.OUTPUT_DIR, 'android/')
        makedirs(output_dir)
        filename = '{}_{}.csv'.format(device.id, time.strftime('%Y.%m.%d_%H%M%S'))
        with open(op.join(output_dir, filename), 'w+') as f:
            writer = csv.writer(f)
            for row in self.data:
                writer.writerow(row)
