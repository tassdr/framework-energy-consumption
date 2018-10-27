import logging
import os.path as op
from pyand import ADB

logger = logging.getLogger(__name__)


class AdbError(Exception):
    """Raised when there's an error with ADB"""
    pass


class ConnectionError(Exception):
    """Raised when there's an connection error"""
    pass

adb = None


def setup(path='adb'):
    global adb
    adb = ADB(adb_path=path)
    # Accessing class private variables to avoid another print of the same error message
    # https://stackoverflow.com/a/1301369
    if adb._ADB__error:
        raise AdbError('adb path is incorrect')


def connect(device_id):
    device_list = adb.get_devices()
    if not device_list:
        raise ConnectionError('No devices are connected')
    logger.debug('Device list:\n%s' % device_list)
    if device_id not in device_list.values():
        raise ConnectionError('%s: Device can not connected' % device_id)


def shell(device_id, cmd):
    adb.set_target_by_name(device_id)
    result = adb.shell_command(cmd)
    logger.debug('%s: "%s" returned: \n%s' % (device_id, cmd, result))
    if 'error' in result:
        raise AdbError(result)
    return result.rstrip()


def list_apps(device_id):
    return shell(device_id, 'pm list packages').replace('package:', '').split()


def install(device_id, apk, replace=True, all_permissions=True):
    filename = op.basename(apk)
    logger.debug('%s: Installing "%s"' % (device_id, filename))
    adb.set_target_by_name(device_id)
    cmd = 'install'
    if replace:
        cmd += ' -r'
    if all_permissions:
        cmd += ' -g'
    adb.run_cmd('%s %s' % (cmd, apk))
    # WARNING: Accessing class private variables
    output = adb._ADB__output
    logger.debug('install returned: %s' % output)
    return output


def uninstall(device_id, name, keep_data=False):
    logger.debug('%s: Uninstalling "%s"' % (device_id, name))
    adb.set_target_by_name(device_id)
    # Flips the keep_data flag as it is incorrectly implemented in the pyand library
    keep_data = not keep_data
    result = adb.uninstall(package=name, keepdata=keep_data)
    success_or_exception(result,
                         '%s: "%s" uninstalled' % (device_id, name),
                         '%s: Failed to uninstall "%s"' % (device_id, name)
                         )


def clear_app_data(device_id, name):
    adb.set_target_by_name(device_id)
    success_or_exception(adb.shell_command('pm clear %s' % name),
                         '%s: Data of "%s" cleared' % (device_id, name),
                         '%s: Failed to clear data for "%s"' % (device_id, name)
                         )


def success_or_exception(result, success_msg, fail_msg):
    if 'Success' in result:
        logger.info(success_msg)
    else:
        logger.info(fail_msg + '\nMessage returned:\n%s' % result)
        raise AdbError(result)


# Same with push_local_file(), but with the quotes removed
# adb doesn't want quotes for some reason
def push(device_id, local, remote):
    adb.set_target_by_name(device_id)
    adb.run_cmd('push %s %s' % (local, remote))
    # WARNING: Accessing class private variables
    return adb._ADB__output


# Same with get_remote_file(), but with the quotes removed
# adb doesn't want quotes for some reason
def pull(device_id, remote, local):
    adb.set_target_by_name(device_id)
    adb.run_cmd('pull %s %s' % (remote, local))
    # WARNING: Accessing class private variables
    if adb._ADB__error and "bytes in" in adb._ADB__error:
        adb._ADB__output = adb._ADB__error
        adb._ADB__error = None
    return adb._ADB__output


def logcat(device_id, regex=None):
    # https://developer.android.com/studio/command-line/logcat.html#Syntax
    # -d prints to screen and exits
    params = '-d'
    if regex is not None:
        params += ' -e %s' % regex
    adb.set_target_by_name(device_id)
    return adb.get_logcat(lcfilter=params)
