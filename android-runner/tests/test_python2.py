import unittest
import tempfile
from ExperimentRunner.Python2 import Python2
from FakeDevice import FakeDevice


class TestPython2(unittest.TestCase):
    def setUp(self):
        self.device = FakeDevice('fake_id')
        self.file = tempfile.NamedTemporaryFile()
        self.file.write('\n'.join(['from time import sleep',
                                   'def main(device_id, current_activity):\n',
                                   '    sleep(0.5)\n'])
                        )
        self.file.flush()

    def tearDown(self):
        self.file.close()

    def test_normal(self):
        self.assertEqual(
            Python2(self.file.name).run(self.device),
            'script'
        )

    def test_timeout(self):
        self.assertEqual(
            Python2(self.file.name, timeout=10).run(self.device),
            'timeout'
        )

    def test_logcat(self):
        self.assertEqual(
            Python2(self.file.name, logcat_regex='').run(self.device),
            'logcat'
        )


if __name__ == '__main__':
    unittest.main()
