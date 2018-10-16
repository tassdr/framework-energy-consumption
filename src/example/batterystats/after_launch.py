def main(device, *args, **kwargs):
    """ Enable for Web Experiments using Chrome
    # Tap coordinates can be found by enabling 'Pointer location' in Developer options
    # Accept Chrome policy prompts
    device.shell('input tap 600 1420')
    device.shell('input tap 200 1420')
    
    # Enable permissions for Chrome
    device.shell('pm grant com.android.chrome android.permission.RECORD_AUDIO')
    device.shell('pm grant com.android.chrome android.permission.CAMERA')
    device.shell('pm grant com.android.chrome android.permission.WRITE_EXTERNAL_STORAGE')
    device.shell('pm grant com.android.chrome android.permission.READ_EXTERNAL_STORAGE')
    """
    pass
