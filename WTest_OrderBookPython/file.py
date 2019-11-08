
class OrdersFile:
    """Simple wrapper for a file of orders."""
    def __init__(self):
        self._f = None # File to read.

    def __del__(self):
        self.close()

    def close(self):
        """Closes file if opened."""
        if self.is_opened():
            self._f.close()
            self._f = None

    def open_for_read(self, file_name):
        """
        Opens file for read.
        :param file_name: File name to open.
        """
        self.close()
        self._f = open(file_name)
        if not self.is_opened():
            raise Exception('Cannot open file.')

    def read_order_record(self, record):
        """
        Reads and validates orders records.
        :param record: Reference to a record to write data in.
        :return False if end of file reached, true otherwise.
        """
        if not self.is_opened():
            raise Exception('File is not opened.')

        line = self._f.readline()
        if not line:
            return False
        record.from_string(line)
        record.validate()
        return True

    def is_opened(self):
        """
        Checks if file is opened.
        :return True if the file is in opened state.
        """
        return self._f is not None
