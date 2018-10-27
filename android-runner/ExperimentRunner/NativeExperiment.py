import os
import os.path as op
from Experiment import Experiment
from util import ConfigError, makedirs, slugify
import paths
import Tests
import time


class NativeExperiment(Experiment):
    def __init__(self, config):
        self.package = None
        self.duration = Tests.is_integer(config.get('duration', 0)) / 1000
        super(NativeExperiment, self).__init__(config)
        for apk in config.get('paths', []):
            if not op.isfile(apk):
                raise ConfigError('File %s not found' % apk)

    def cleanup(self, device):
        super(NativeExperiment, self).cleanup(device)
        if self.package in device.get_app_list():
            device.uninstall(self.package)

    def before_experiment(self, device, *args, **kwargs):
        super(NativeExperiment, self).before_experiment(device)

    def before_first_run(self, device, path, *args, **kwargs):
        super(NativeExperiment, self).before_first_run(device, path)
        filename = op.basename(path)
        paths.OUTPUT_DIR = op.join(paths.OUTPUT_DIR, slugify(filename))
        makedirs(paths.OUTPUT_DIR)
        self.logger.info('APK: %s' % filename)
        device.install(path)
        self.package = op.splitext(op.basename(path))[0]

    def before_run(self, device, path, run, *args, **kwargs):
        super(NativeExperiment, self).before_run(device, path, run)
        device.launch_package(self.package)
        self.scripts.run('after_launch', device, device.id, device.current_activity())

    def start_profiling(self, device, path, run, *args, **kwargs):
        self.profilers.start_profiling(device, app=self.package)
        time.sleep(self.duration)

    def after_run(self, device, path, run, *args, **kwargs):
        self.scripts.run('before_close', device, device.id, device.current_activity())
        device.force_stop(self.package)
        super(NativeExperiment, self).after_run(device, path, run)

    def after_last_run(self, device, path, *args, **kwargs):
        super(NativeExperiment, self).after_last_run(device, path)
        device.uninstall(self.package)
        self.package = None
        # https://stackoverflow.com/a/2860193
        paths.OUTPUT_DIR = op.abspath(op.join(paths.OUTPUT_DIR, os.pardir))

    def after_experiment(self, device, *args, **kwargs):
        super(NativeExperiment, self).after_experiment(device)
