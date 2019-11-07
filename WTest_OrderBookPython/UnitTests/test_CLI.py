import unittest
#import sys
#sys.path.append('..')
from CLI import command_line

class CLI_TestCase(unittest.TestCase):
    def test_CLI_invalid_count(self):
        cli = command_line()
        with self.assertRaises(Exception):
            cli.init(['path'])

    def test_CLI_invalid_args(self):
        cli = command_line()
        with self.assertRaises(Exception):
            cli.init(None)

    def test_CLI_file_name(self):
        cli = command_line()
        args = ['path', 'test.txt']
        cli.init(args)
        self.assertEqual(cli.src_file_name(), args[1])


if __name__ == '__main__':
    unittest.main()
