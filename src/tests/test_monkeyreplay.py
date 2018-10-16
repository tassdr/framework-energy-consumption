import unittest
import tempfile
from ExperimentRunner.MonkeyReplay import MonkeyReplay
from FakeDevice import FakeDevice


class TestMonkeyReplay(unittest.TestCase):
    def setUp(self):
        self.monkey = '/opt/platform-tools/bin/monkeyrunner'
        self.device = FakeDevice('fake_id')
        self.current_activity = 'fake_activity'
        self.file = tempfile.NamedTemporaryFile()
        self.file.write('\n'.join(['{"type": "hello"}',
                                   '{"type": "dont"}'])
                        )
        self.file.flush()

    def tearDown(self):
        self.file.close()

    def test_normal(self):
        self.assertEqual(
            MonkeyReplay(self.file.name, monkeyrunner_path=self.monkey).run(self.device),
            'script'
        )

    def test_timeout(self):
        self.assertEqual(
            MonkeyReplay(self.file.name, timeout=10, monkeyrunner_path=self.monkey).run(self.device),
            'timeout'
        )

    def test_logcat(self):
        self.assertEqual(
            MonkeyReplay(self.file.name, logcat_regex='', monkeyrunner_path=self.monkey).run(self.device),
            'logcat'
        )


if __name__ == '__main__':
    unittest.main()
