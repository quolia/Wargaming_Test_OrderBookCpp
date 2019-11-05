import sys

class command_line:
    """Command line parameters validator."""
    def __init__(self):
        """Ctor."""
        self.__src_file_name = None

    def src_file_name(self):
        """Returns source file name."""
        return self.__src_file_name

    def init(self):
        """Initiates and validates command line parameters."""
        argv = sys.argv[1:]
        argc = len(argv)
        if argc < 1:
            raise Exception('Invalid parameters count. Example parameters: srcfile')

        __src_file_name = argv[0]
