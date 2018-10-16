import logging
import os.path as op
import time

import paths
import Tests
from Devices import Devices
from Profilers import Profilers
from Scripts import Scripts
from util import ConfigError, makedirs


class Experiment(object):
    def __init__(self, config):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.basedir = None
        if 'devices' not in config:
            raise ConfigError('"device" is required in the configuration')
        adb_path = config.get('adb_path', 'adb')
        self.devices = Devices(config['devices'], adb_path=adb_path)
        self.replications = Tests.is_integer(config.get('replications', 1))
        self.paths = config.get('paths', [])
        self.profilers = Profilers(config.get('profilers', {}))
        monkeyrunner_path = config.get('monkeyrunner_path', 'monkeyrunner')
        self.scripts = Scripts(config.get('scripts', {}), monkeyrunner_path=monkeyrunner_path)
        self.time_between_run = Tests.is_integer(config.get('time_between_run', 0))
        Tests.check_dependencies(self.devices, self.profilers.dependencies())
        self.output_root = paths.OUTPUT_DIR

    def prepare(self, device):
        """Prepare the device for experiment"""
        self.logger.info('Device: %s' % device)
        self.profilers.load(device)
        device.unplug()

    def cleanup(self, device):
        """Cleans up the changes on the devices"""
        device.plug()
        self.profilers.stop_profiling(device)
        self.profilers.unload(device)

    def start(self):
        """Runs the experiment"""
        for device in self.devices:
            try:
                paths.OUTPUT_DIR = op.join(self.output_root, 'data/', device.name)
                makedirs(paths.OUTPUT_DIR)
                self.prepare(device)
                self.before_experiment(device)
                for path in self.paths:
                    self.before_first_run(device, path)
                    for run in range(self.replications):
                        self.run(device, path, run)
                    self.after_last_run(device, path)
                self.after_experiment(device)
            except Exception, e:
                import traceback
                print(traceback.format_exc())
                self.logger.error('%s: %s' % (e.__class__.__name__, e.message))
            finally:
                self.cleanup(device)
        self.scripts.run('aggregation', None, self.output_root)

    def run(self, device, path, run):
        self.before_run(device, path, run)
        self.start_profiling(device, path, run)
        self.interaction(device, path, run)
        self.stop_profiling(device, path, run)
        self.after_run(device, path, run)

    def before_experiment(self, device, *args, **kwargs):
        """Hook executed before the start of experiment"""
        self.scripts.run('before_experiment', device, *args, **kwargs)

    def before_first_run(self, device, path, *args, **kwargs):
        """Hook executed before the first run for a subject"""
        pass

    def before_run(self, device, path, run, *args, **kwargs):
        """Hook executed before a run"""
        self.logger.info('Run %s of %s' % (run + 1, self.replications))
        self.scripts.run('before_run', device, *args, **kwargs)

    def after_launch(self, device, path, run, *args, **kwargs):
        self.scripts.run('after_launch', device, *args, **kwargs)

    def start_profiling(self, device, path, run, *args, **kwargs):
        self.profilers.start_profiling(device)

    def interaction(self, device, path, run, *args, **kwargs):
        """Interactions on the device to be profiled"""
        self.scripts.run('interaction', device, *args, **kwargs)

    def stop_profiling(self, device, path, run, *args, **kwargs):
        self.profilers.stop_profiling(device)

    def before_close(self, device, path, run, *args, **kwargs):
        self.scripts.run('before_close', device, *args, **kwargs)

    def after_run(self, device, path, run, *args, **kwargs):
        """Hook executed after a run"""
        self.scripts.run('after_run', device, *args, **kwargs)
        self.profilers.collect_results(device)
        self.logger.debug('Sleeping for %s milliseconds' % self.time_between_run)
        time.sleep(self.time_between_run / 1000.0)

    def after_last_run(self, device, path, *args, **kwargs):
        """Hook executed after the last run of a subject"""
        pass

    def after_experiment(self, device, *args, **kwargs):
        """Hook executed after the end of experiment"""
        self.logger.info('Experiment completed, start cleanup')
        self.scripts.run('after_experiment', device, *args, **kwargs)
