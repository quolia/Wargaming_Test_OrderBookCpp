from orderbook import OrderBookInterface
from items import *


class Accumulator:
    """Orders time and price accumulator."""

    def __init__(self):
        self._order_book: OrderBookInterface = None  # Pointer to underlying order book container.
        self._accumulator_price = float(0)           # Accumulated value of prices.
        self._accumulator_time = int(0)              # Accumulated value of time.
        self._last_timestamp = invalid_timestamp     # Last time maximum price was changed.
        self.reset()

    def init(self, order_book: OrderBookInterface):
        """
        Init accumulator.
        :param order_book: Order book interface.
        """
        self._order_book = order_book

    def reset(self):
        """Resets accumulator state."""
        self._order_book = None
        self._accumulator_price = float(0)
        self._accumulator_time = int(0)
        self._last_timestamp = invalid_timestamp

    def add_order(self, order: OrderItem):
        """"
        Adds order to accumulator.
        :param order: Order to add.
        """
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

    def remove_order(self, order_id, timestamp):
        """
        Removes order from accumulator.
        :param order_id: Previously added order id.
        :param timestamp: Current timestamp.
        """
        if self._order_book is None:
            raise Exception('Accumulator not inited.')

        # Check if the order being removed is the top-price order.
        max_price_order = self._order_book.max_price_order()
        if max_price_order.id() == order_id:
            if timestamp < self._last_timestamp:
                raise Exception('Time line inconsistent.')
            elif timestamp != self._last_timestamp: # If not removed at the same time.
                # Accumulate top-price order time and update time of top-price order changing.
                time = timestamp - self._last_timestamp
                self._accumulator_price += max_price_order.price() * time
                self._accumulator_time += time
                self._last_timestamp = timestamp

        # Remove the order from the book.
        self._order_book.remove(order_id)

    def average_highest_price(self):
        """Returns time-weighted average highest price of orders."""
        return 0 if 0 == self._accumulator_time else self._accumulator_price / self._accumulator_time
