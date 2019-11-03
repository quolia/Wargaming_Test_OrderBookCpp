from .CLI import command_line
from .File import orders_file
from .OrderBook import order_book_iface, order_book
from .Accumulator import accumulator

class application:
    """Application class."""
    def __init__(self):
        # Ctor.
        self._is_inited = False # The flag is true if the application instance has been inited successfully.
        self._src_file = orders_file() # File to read.
        self._order_book = None # Pointer to order book interface.
        self._accumulator = accumulator() # Orders time-weight accumulator.

    def init(self):
        """Initiates application instance."""
        self._is_inited = False

        cli_params = command_line()
        cli_params.init()

        print("Source file: ") # << cli_params.src_file_name() << endl;
        self._src_file.open_for_read(cli_params.src_file_name())

        self._order_book = order_book()
        self._accumulator.init(self._order_book)

        _is_inited = True

    def run(self):
        """Reads source file till the end."""
        if (!self._is_inited):
            raise BaseException("Application has not been inited yet.")

        order_record record;

        while (_src_file.read_order_record(record))
            if (record.is_insert()):
                _accumulator.add_order(record);
            else:
                _accumulator.remove_order(record.id(), record.timestamp());

    """
    // / < summary > Returns    time - weighted    average    highest    price    of    orders. < / summary >
    // / < returns > Time - weighted    average    highest    price    of    orders. < / returns >
    """
    def average_highest_price(self):

        if (!self._is_inited):
            throw exception("Application has not been inited yet.")

        return _accumulator.average_highest_price()
