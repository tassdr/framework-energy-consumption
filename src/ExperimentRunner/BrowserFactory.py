from Browsers import Chrome, Firefox, Opera


class BrowserFactory(object):
    @staticmethod
    def get_browser(name):
        if name == "chrome":
            return Chrome.Chrome
        if name == "firefox":
            return Firefox.Firefox
        if name == "opera":
            return Opera.Opera
        return Exception("No Browser found")
