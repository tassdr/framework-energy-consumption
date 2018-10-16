import logging
import os.path as op
import re
import time

import Adb
from Adb import AdbError
from util import makedirs


class Device:
    def __init__(self, name, device_id):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.name = name
        self.id = device_id
        Adb.connect(device_id)

    def get_version(self):
        """Returns the Android version"""
        return Adb.shell(self.id, 'getprop ro.build.version.release')

    def get_api_level(self):
        """Returns the Android API level as a number"""
        return Adb.shell(self.id, 'getprop ro.build.version.sdk')

    def is_installed(self, apps):
        """Returns a boolean if a package is installed"""
        return {app: app in self.get_app_list() for app in apps}

    def get_app_list(self):
        """Returns a list of installed packages on the system"""
        return Adb.list_apps(self.id)

    def install(self, apk):
        """Check if the file exists, and then install the package"""
        if not op.isfile(apk):
            raise AdbError("%s is not found" % apk)
        Adb.install(self.id, apk)

    def uninstall(self, name):
        """Uninstalls the package on the device"""
        Adb.uninstall(self.id, name)

    def unplug(self):
        """Fakes the device to think it is unplugged, so the Doze mode can be activated"""
        if self.get_api_level() < 23:
            # API level < 23, 4.4.3+ tested, WARNING: hardcoding
            Adb.shell(self.id, 'dumpsys battery set usb 0')
            # Adb.shell(self.id, 'dumpsys battery set ac 0')
            # Adb.shell(self.id, 'dumpsys battery set wireless 0')
        else:
            # API level 23+ (Android 6.0+)
            Adb.shell(self.id, 'dumpsys battery unplug')

    def plug(self):
        """Reset the power status of the device"""
        if self.get_api_level() < 23:
            # API level < 23, 4.4.3+ tested, WARNING: hardcoding
            # reset only restarts auto-update
            Adb.shell(self.id, 'dumpsys battery set usb 1')
        # API level 23+ (Android 6.0+)
        Adb.shell(self.id, 'dumpsys battery reset')

    def current_activity(self):
        """Returns the current focused activity on the system"""
        # https://github.com/aldonin/appium-adb/blob/7b4ed3e7e2b384333bb85f8a2952a3083873a90e/lib/adb.js#L1278
        windows = Adb.shell(self.id, 'dumpsys window windows')
        null_re = r'mFocusedApp=null'
        # https://regex101.com/r/xZ8vF7/1
        current_focus_re = r'mCurrentFocus.+\s([^\s\/\}]+)\/[^\s\/\}]+(\.[^\s\/\}]+)}'
        focused_app_re = r'mFocusedApp.+Record\{.*\s([^\s\/\}]+)\/([^\s\/\}\,]+)(\s[^\s\/\}]+)*\}'
        match = None
        found_null = False
        for line in windows.split('\n'):
            current_focus = re.search(current_focus_re, line)
            focused_app = re.search(focused_app_re, line)
            if current_focus:
                match = current_focus
            elif focused_app and match is None:
                match = focused_app
            elif re.search(null_re, line):
                found_null = True
        if match:
            result = match.group(1).strip()
            self.logger.debug('Current activity: %s' % result)
            return result
        elif found_null:
            self.logger.debug('Current activity: null')
            return None
        else:
            self.logger.error('Results from dumpsys window windows: \n%s' % windows)
            raise AdbError('Could not parse activity from dumpsys')

    def launch_package(self, package):
        """Launches a package by name without activity, returns instantly"""
        # https://stackoverflow.com/a/25398877
        result = Adb.shell(self.id, 'monkey -p {} 1'.format(package))
        if 'monkey aborted' in result:
            raise AdbError('Could not launch "{}"'.format(package))

    def launch_activity(self, package, activity, action='', data_uri='', from_scratch=False, force_stop=False):
        """Launches an activity using 'am start', returns instantly"""
        # https://developer.android.com/studio/command-line/adb.html#am
        # https://developer.android.com/studio/command-line/adb.html#IntentSpec
        # https://stackoverflow.com/a/3229077
        cmd = 'am start'
        if force_stop:
            cmd += ' -S'
        if action:
            cmd += ' -a %s' % action
        cmd += ' -n %s/%s' % (package, activity)
        if data_uri:
            cmd += ' -d %s' % data_uri
        # https://android.stackexchange.com/a/113919
        if from_scratch:
            cmd += ' --activity-clear-task'
        return Adb.shell(self.id, cmd)

    def force_stop(self, name):
        """Force stop an app by package name"""
        Adb.shell(self.id, 'am force-stop %s' % name)

    def clear_app_data(self, name):
        """Clears the data of an app by package name"""
        Adb.clear_app_data(self.id, name)

    def logcat_to_file(self, path):
        """Dumps the last x lines of logcat into a file specified by path"""
        makedirs(path)
        with open(op.join(path, '%s_%s.txt' % (self.id, time.strftime('%Y.%m.%d_%H%M%S'))), 'w+') as f:
            f.write(Adb.logcat(self.id))

    def logcat_regex(self, regex):
        return Adb.logcat(self.id, regex=regex)

    def push(self, local, remote):
        """Pushes a file from the computer to the device"""
        return Adb.push(self.id, local, remote)

    def pull(self, remote, local):
        """Pulls a file from the device to the computer"""
        return Adb.pull(self.id, remote, local)

    def shell(self, cmd):
        """Runs the device shell with command specified by cmd"""
        return Adb.shell(self.id, cmd)

    def __str__(self):
        return '%s (%s, Android %s, API level %s)' % (self.name, self.id, self.get_version(), self.get_api_level())
