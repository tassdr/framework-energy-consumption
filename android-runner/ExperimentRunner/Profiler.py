import logging


class Profiler(object):
    @staticmethod
    def dependencies():
        return []

    def __init__(self, config):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Initialized')

    def load(self, device):
        """Load (and start) the profiler process on the device"""
        self.logger.debug('%s: Loading configuration' % device)

    def start_profiling(self, device, **kwargs):
        """Start the profiling process"""
        self.logger.debug('%s: Start profiling' % device)

    def stop_profiling(self, device, **kwargs):
        """Stop the profiling process"""
        self.logger.debug('%s: Stop profiling' % device)

    def collect_results(self, device, path=None):
        """Collect the data and clean up extra files on the device"""
        self.logger.debug('%s: Collecting data' % device)

    def unload(self, device):
        """Stop the profiler, removing configuration files on device"""
        self.logger.debug('%s: Cleanup' % device)
