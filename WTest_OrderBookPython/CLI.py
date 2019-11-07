
class command_line:
    """Command line parameters validator."""
    def __init__(self):
        self.__src_file_name = None

    def src_file_name(self):
        """Returns source file name."""
        return self.__src_file_name

    def init(self, args):
        """Initiates and validates command line parameters."""
        if args is None or len(args) < 2:
            raise Exception('Invalid parameters count. Example parameters: srcfile')
        self.__src_file_name = args[1]
