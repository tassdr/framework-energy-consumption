from Browser import Browser


class Opera(Browser):
    def __init__(self, config):
        super(Opera, self).__init__(config)
        self.package_name = 'com.opera.browser'
        self.main_activity = 'com.opera.Opera'
