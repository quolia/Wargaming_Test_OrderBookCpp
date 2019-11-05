from .OrderBook import order_book_iface
from .Types import *

class accumulator:
    """Orders time and price accumulator."""
    def __init__(self):
        self._order_book = None	            #/// <summary> Pointer to underlying order book container. </summary>
        self._accumulator_price = float(0)	#/// <summary> Accumulated value of prices. </summary>
        self._accumulator_time = int(0)		#/// <summary> Accumulated value of time. </summary>
        self._last_timestamp = int(0)		#/// <summary> Last time maximum price was changed. </summary>
        self.reset()

    #	/// <param name="order_book"> Order book interface. </param>
    def init(self, order_book):
        """Init accumulator."""
        self._order_book = order_book

        #/// <summary> Reset accumulator state. </summary>
    def reset(self):
        self._order_book.reset()
        self._accumulator_price = 0
        self._accumulator_time = 0
        self._last_timestamp = invalid_timestamp

        #/// <param name="order"> Order to add. </param>
    def add_order(self, order):
        """"Adds order to accumulator."""
        if self._order_book is None:
            raise Exception('Accumulator not inited.')

        # Check if new order is top-price order and accumulate previous top-price order time.

        current_max_price = self._order_book.max_price_order().price()

        if order.price() > current_max_price:
            if current_max_price > 0:
                time = order.timestamp() - self._last_timestamp
                self._accumulator_price += current_max_price * time
                self._accumulator_time += time

            # Update last timestamp of top-price order changing.
            self._last_timestamp = order.timestamp()


        self._order_book.add(order)

    #/// <param name="id"> Previously added order id. </param>
    #/// <param name="timestamp"> Current timestamp. </param>
    def remove_order(self, id, timestamp):
        """Removes order from accumulator."""
        if self._order_book is None:
            raise Exception('Accumulator not inited.')

        # Check if the order being removed is the top-price order.
        max_price_order = self._order_book.max_price_order()
        if max_price_order.id() == id:
            if timestamp < self._last_timestamp:
                raise Exception('Time line inconsistent.')
            elif timestamp != self._last_timestamp: # If not removed at the same time.
                # Accumulate top-price order time and update time of top-price order changing.
                time = timestamp - self._last_timestamp
                self._accumulator_price += max_price_order.price() * time
                self._accumulator_time += time
                self._last_timestamp = timestamp

        # Remove the order from the book.
        self._order_book.remove(id)

    def average_highest_price(self):
        """Returns time-weighted average highest price of orders."""
        return 0 if 0 == self._accumulator_time else self._accumulator_price / self._accumulator_time