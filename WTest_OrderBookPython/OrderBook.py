from .OrderItem import *
from sortedcontainers import SortedSet

#// / < summary > Interface for order book implementation.< / summary >
class order_book_iface:

    #// / < summary > Adds    order. < / summary >
    #// / < param    name = "order" > Order    to    add. < / param >
    def add(self, order):
        pass

    #// / < summary > Removes    order. < / summary >
    #// / < param    name = "id" > Previously    added    order    id. < / param >
    #// / < param    name = "timestamp" > Current    timestamp. < / param >
    def remove(self, id):
        pass

    #// / < summary > Returns    top - price    order. < / summary >
    def max_price_order(self):
        pass

    #// / < summary > Returns    amount    of    orders in the    book. < / summary >
    def size(self):
        pass

    #// / < summary > Default    virtual    destructor    to    allow    implementations    instances   destructors    to    be    called    when    deleted as abstract    class . < / summary >
    def __del__(self):
        pass

class order_book(order_book_iface):
    """Default implementation for order book interface."""
    def __init__(self):
        self._orders = SortedSet() #// / < summary > Container of orders. < / summary >
        self._orders_map = dict() #// / < summary > Supporting 'map' to store order id and data. < / summary >
        self._null_order = order_item() #// / < summary > Default order to return if order book is empty.< / summary >

    #// / < summary > Adds order. < / summary >
    #// / < param name = "order" > Order to add.O(log(n)). < / param >
    def add(self, order):
        #// Insert order to the 'set'.It will be automatically inserted to a sort - keep position.
        self._orders.add(order) #// O(log(n))

        #// Insert order to 'map'.
        map_result = self._orders_map[order.id()] = order.data() #// O(1)
        if not map_result.second:
            self._orders.remove(order)
            raise Exception('Cannot insert order with the given id.')

    #// / < summary > Removes order. O(log(n)). # < / summary >
    #// / < param name = "id" > Previously added order id. < / param >
    def remove(self, id):
        if 0 == id:
            raise Exception('Invalid order id.')

        #// Find order in 'map' by order id and remove it.
        order_data = self._orders_map[id] #// O(1)
        self._orders_map.pop(id) #// O(1)

        # // Remove the order from 'set'.
        self._orders.remove(order_item(id, order_data)) #// O(log(n))

    #// / < summary > Returns top - price order.The top - price order is located at the end of 'set'. < / summary >
    def max_price_order(self):
        top = self._orders[-1]
        return self._null_order if top == None else top

    #// / < summary > Returns amount of orders in the book. < / summary >
    def size(self):
        return len(self._orders_map)