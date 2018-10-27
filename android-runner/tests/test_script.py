import unittest
from ExperimentRunner.Script import Script
from ExperimentRunner.util import FileNotFoundError


class TestScript(unittest.TestCase):
    def test_filenotfound(self):
        with self.assertRaises(FileNotFoundError):
            Script('some_nonexistant_path')

if __name__ == '__main__':
    unittest.main()
