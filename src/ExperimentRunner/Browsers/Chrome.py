from Browser import Browser


class Chrome(Browser):
    def __init__(self, config):
        super(Chrome, self).__init__(config)
        self.package_name = 'com.android.chrome'
        # https://stackoverflow.com/a/28151563
        self.main_activity = 'com.google.android.apps.chrome.Main'
