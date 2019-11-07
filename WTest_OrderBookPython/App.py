import sys
from CLI import command_line
from File import orders_file
from OrderBook import order_book_iface, order_book
from Accumulator import accumulator
from OrderItem import *

class application:
    """Application class."""
    def __init__(self):
        self._is_inited = False             # The flag is true if the application instance has been inited successfully.
        self._src_file = orders_file()      # File to read.
        self._order_book = None             # Pointer to order book interface.
        self._accumulator = accumulator()   # Orders time-weight accumulator.

    def init(self):
        """Initiates application instance."""
        self._is_inited = False

        cli_params = command_line()
        cli_params.init(sys.argv)

        print(f'Source file: {cli_params.src_file_name()}')
        self._src_file.open_for_read(cli_params.src_file_name())

        self._order_book = order_book()
        self._accumulator.init(self._order_book)

        self._is_inited = True

    def run(self):
        """Reads source file till the end."""
        if not self._is_inited:
            raise Exception('Application has not been inited yet.')

        record = order_record()
        while self._src_file.read_order_record(record):
            if record.is_insert():
                self._accumulator.add_order(order_item.from_record(record))
            else:
                self._accumulator.remove_order(record.id(), record.timestamp())

    def average_highest_price(self):
        """Returns time-weighted average highest price of orders."""
        if not self._is_inited:
            raise Exception('Application has not been inited yet.')
        return self._accumulator.average_highest_price()
