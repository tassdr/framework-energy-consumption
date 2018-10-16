class FakeDevice(object):
    def __init__(self, device_id):
        self.id = device_id

    def current_activity(self):
        return 'fake.activity'

    def logcat_regex(self, regex):
        return regex
