from cli import CommandLine
from file import OrdersFile
from orderbook import OrderBookIface, OrderBook
from accumulator import Accumulator
from items import *


class Application:
    """Application class."""

    _is_inited = False                  # The flag is true if the application instance has been inited successfully.
    _src_file = OrdersFile()            # File to read.
    _order_book: OrderBookIface = None  # Pointer to order book interface.
    _accumulator = Accumulator()        # Orders time-weight accumulator.

    def init(self, args):
        """Initiates application instance."""
        self._is_inited = False

        cli = CommandLine()
        cli.init(args)

        print(f'Source file: {cli.src_file_name()}')
        self._src_file.open_for_read(cli.src_file_name())

        self._order_book = OrderBook()
        self._accumulator.init(self._order_book)

        self._is_inited = True

    def run(self):
        """Reads source file till the end."""
        if not self._is_inited:
            raise Exception('Application has not been inited yet.')

        record = OrderRecord()
        while self._src_file.read_order_record(record):
            if record.is_insert():
                self._accumulator.add_order(OrderItem.from_record(record))
            else:
                self._accumulator.remove_order(record.id(), record.timestamp())

    def average_highest_price(self):
        """Returns time-weighted average highest price of orders."""
        if not self._is_inited:
            raise Exception('Application has not been inited yet.')
        return self._accumulator.average_highest_price()
