import logging
import os.path as op

from util import ConfigError
from Python2 import Python2
from MonkeyReplay import MonkeyReplay
import paths


class Scripts(object):
    def __init__(self, config, monkeyrunner_path='monkeyrunner'):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.scripts = {}
        for name, script in config.items():
            self.scripts[name] = []
            if isinstance(script, basestring):
                path = op.join(paths.CONFIG_DIR, script)
                self.scripts[name].append(Python2(path))
                continue
            for s in script:
                path = op.join(paths.CONFIG_DIR, s['path'])
                timeout = s.get('timeout', 0)
                logcat_regex = s.get('logcat_regex', None)
                if s['type'] == 'python2':
                    self.scripts[name].append(Python2(path, timeout, logcat_regex))
                elif s['type'] == 'monkeyreplay':
                    self.scripts[name].append(
                        MonkeyReplay(path, timeout, logcat_regex, monkeyrunner_path=monkeyrunner_path))
                else:
                    raise ConfigError('Unknown script type')

    def run(self, name, device, *args, **kwargs):
        self.logger.debug('Running hook {} on device {}\nargs: {}\nkwargs: {}'.format(name, device, args, kwargs))
        for script in self.scripts.get(name, []):
            script.run(device, *args, **kwargs)
