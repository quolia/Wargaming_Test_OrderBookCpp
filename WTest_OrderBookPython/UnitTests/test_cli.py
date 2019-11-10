import sys
sys.path.append('..')
import unittest
from cli import CommandLine


class CLITestCase(unittest.TestCase):

    def test_CLI_invalid_count(self):
        cli = CommandLine()
        with self.assertRaises(Exception):
            cli.init(['path'])

    def test_CLI_invalid_args(self):
        cli = CommandLine()
        with self.assertRaises(Exception):
            cli.init(None)

    def test_CLI_file_name(self):
        cli = CommandLine()
        args = ['path', 'test.txt']
        cli.init(args)
        self.assertEqual(cli.src_file_name(), args[1])


if __name__ == '__main__':
    unittest.main()
