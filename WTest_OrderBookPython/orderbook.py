from items import *
from sortedcontainers import SortedSet


class OrderBookInterface:
    """Interface for order book implementation."""

    def add(self, order: OrderItem):
        """
        Adds order.
        :param order: Order to add.
        """
        pass

    def remove(self, order_id):
        """
        Removes order.
        :param order_id: Previously added order id.
        """
        pass

    def max_price_order(self):
        """Returns top-price order."""
        pass

    def size(self):
        """Returns amount of orders in the book."""
        pass

    def __del__(self):
        pass


class _OrderBook(OrderBookInterface):
    """Default implementation for order book interface."""

    _orders = SortedSet()      # Container of orders.
    _orders_map = dict()       # Supporting 'map' to store order id and data.
    _null_order = OrderItem()  # Default order to return if order book is empty.

    def add(self, order):
        """
        O(log(n))
        Inserts order to the 'set'. It will be automatically inserted to a sort-keep position.
        :param order: Order to add.
        """
        self._orders.add(order) # O(log(n))

        # Insert order to 'map'.
        try:
            self._orders_map[order.id()] = order.data() # O(1)
        except Exception as e:
            self._orders.remove(order)
            raise Exception(f'Cannot insert order with the given id ({e}).')

    def remove(self, order_id):
        """
        O(log(n))
        Removes order.
        :param order_id: Previously added order id.
        """
        if 0 == order_id:
            raise Exception('Invalid order id.')

        # Find order in 'map' by order id and remove it.
        data = self._orders_map[order_id] # O(1)
        self._orders_map.pop(order_id)    # O(1)

        # Remove the order from 'set'.
        self._orders.remove(OrderItem.from_data(order_id, data)) # O(log(n))

    def max_price_order(self):
        """Returns top - price order.The top - price order is located at the end of 'set'."""
        return self._null_order if self.size() == 0 else self._orders[-1]

    def size(self):
        """Returns amount of orders in the book."""
        return len(self._orders_map)


class OrderBookFactory:
    """Fabric to instantiate current order book implementation."""
    @classmethod
    def get(cls) -> OrderBookInterface:
        return _OrderBook()
