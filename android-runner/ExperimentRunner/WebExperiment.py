import os.path as op
import os
import time

import Tests
import paths
from Experiment import Experiment
from BrowserFactory import BrowserFactory
from util import makedirs, slugify


class WebExperiment(Experiment):
    def __init__(self, config):
        super(WebExperiment, self).__init__(config)
        self.browsers = [BrowserFactory.get_browser(b)(config) for b in config.get('browsers', ['chrome'])]
        Tests.check_dependencies(self.devices, [b.package_name for b in self.browsers])
        self.duration = Tests.is_integer(config.get('duration', 0)) / 1000

    def run(self, device, path, run):
        for browser in self.browsers:
            paths.OUTPUT_DIR = op.join(paths.OUTPUT_DIR, slugify(unicode(browser.package_name)))
            self.before_run(device, path, run, browser)
            self.after_launch(device, path, run, browser)
            self.start_profiling(device, path, run, browser)
            self.interaction(device, path, run, browser)
            self.stop_profiling(device, path, run, browser)
            self.before_close(device, path, run, browser)
            self.after_run(device, path, run, browser)
            paths.OUTPUT_DIR = op.abspath(op.join(paths.OUTPUT_DIR, os.pardir))

    def before_first_run(self, device, path, *args, **kwargs):
        super(WebExperiment, self).before_first_run(device, path)
        paths.OUTPUT_DIR = op.join(paths.OUTPUT_DIR, slugify(path))
        makedirs(paths.OUTPUT_DIR)
        self.logger.info('URL: %s' % path)

    def before_run(self, device, path, run, *args, **kwargs):
        super(WebExperiment, self).before_run(device, path, run)
        browser = args[0]
        browser.start(device)
        time.sleep(5)
        self.scripts.run('after_launch', device, device.id, device.current_activity())

    def interaction(self, device, path, run, *args, **kwargs):
        browser = args[0]
        browser.load_url(device, path)
        time.sleep(5)
        super(WebExperiment, self).interaction(device, path, run, *args, **kwargs)

        # TODO: Fix web experiments running longer than self.duration
        time.sleep(self.duration)

    def after_run(self, device, path, run, *args, **kwargs):
        self.scripts.run('before_close', device, device.id, device.current_activity())
        browser = args[0]
        browser.stop(device, clear_data=True)
        time.sleep(3)
        super(WebExperiment, self).after_run(device, path, run)

    def after_last_run(self, device, path, *args, **kwargs):
        super(WebExperiment, self).after_last_run(device, path, *args, **kwargs)
        # https://stackoverflow.com/a/2860193
        paths.OUTPUT_DIR = op.abspath(op.join(paths.OUTPUT_DIR, os.pardir))

    def cleanup(self, device):
        super(WebExperiment, self).cleanup(device)
        for browser in self.browsers:
            browser.stop(device, clear_data=True)
