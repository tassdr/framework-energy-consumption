from Browser import Browser


class Firefox(Browser):
    def __init__(self, config):
        super(Firefox, self).__init__(config)
        self.package_name = 'org.mozilla.firefox'
        self.main_activity = 'org.mozilla.gecko.BrowserApp'
