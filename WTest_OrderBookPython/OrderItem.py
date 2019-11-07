from Types import *

class order_data:
    """Order data."""
    def __init__(self):
        self._price = int(0)
        self._timestamp = invalid_timestamp

    def timestamp(self):
        """Returns order timestamp."""
        return self._timestamp

    def price(self):
        """Returns order price."""
        return self._price

class order_record(order_data):
    """Order record in source file."""

    _id = int(0)  # Order id.
    _is_insert = False  # Is insert operation.

    def __init__(self):
        super().__init__()

    def id(self):
        """Returns order id."""
        return self._id

    def is_insert(self):
        """Returns true if insert operation."""
        return self._is_insert

    def validate(self):
        """Validates order record data."""
        if self._id < 1:
            raise Exception('Invalid order id.')

        if invalid_timestamp == self._timestamp:
            raise Exception('Invalid order timestamp.')

        if self._is_insert and self._price < 0:
            raise Exception('Invalid order price.')

        if not self._is_insert and self._price != 0:
            raise Exception('Invalid order data.')

    def from_string(self, string):
        """
        1000 I 100 10.0
        2000 I 101 13.0
        2200 I 102 13.0
        2400 E 101
        2500 E 102
        4000 E 100
        :param string: String to init the record.
        """
        parts = string.split(' ')
        self._timestamp = int(parts[0])
        t = parts[1]
        self._is_insert = 'I' == t
        self._id = int(parts[2])
        self._price = 0 if not self._is_insert else float(parts[3])

class order_item(order_data):
    """Order item class."""
    _id = int(0)  # Order id.

    def __init__(self):
        super().__init__()

    @classmethod
    def from_record(cls, record: order_record) -> 'order_item':
        order = order_item()
        order._id = record.id()
        order._timestamp = record.timestamp()
        order._price = record.price()
        return order

    @classmethod
    def from_data(cls, id: int, data: order_data) -> 'order_item':
        order = order_item()
        order._id = id
        order._timestamp = data.timestamp()
        order._price = data.price()
        return order

    """
    #// / < summary > Data  ctor. < / summary >
    #// / < param name = "id" > Order id. < / param >
    #// / < param  name = "timestamp" > Order   timestamp. < / param >
    #// / < param name = "price" > Order price. < / param >
    def __init__(self, id, timestamp, price):
        self._id = id
        self._timestamp = timestamp
        self._price = price

    # // / < summary > Copy ctor to copy from order record.< / summary >
    #// / < param name = "record" > Record to make order copy from . < / param >
    def __init__(self, record):
        self._id = record.id()
        self._timestamp = record.timestamp()
        self._price = record.price()


    #// / < summary > Data ctor to copy from order data.< / summary >
    #// / < param name = "data" > Data to make order copy from . < / param >
    def __init__(self, id, data):
        self._id = id
        self._timestamp = data.timestamp()
        self._price = data.price()

    """
    #// / < summary > Returns order's data without id. </summary>
    def data(self) -> 'order_data':
        data = order_data()
        data._timestamp = self.timestamp()
        data._price = self.price()
        return data

    def id(self):
        """Returns order id."""
        return self._id
    """
    #// / < summary > Returns order price. < / summary >
    def price(self):
        return self._price
    
    #// / < summary > Returns order timestamp. < / summary >
    def timestamp(self):
        return self._timestamp
    """
    def __eq__(self, other):
        return self.id() == other.id()

    def __hash__(self):
        return self.id()

    def __lt__(self, other):
        # // / < summary > Implements 'less' operation. < / summary >
        # // / < param name = "l" > Left operand. < / param >
        # // / < param name = "r" > Right operand. < / param >
        # // If prices are equal than compare timestamps and than ids.

        if self.price() == other.price():
            if self.timestamp() == other.timestamp():
                if self.id() == other.id():
                    return False # The same order is always not less than itself.
                else:
                    return self.id() < other.id()
            else:
                return self.timestamp() < other.timestamp()
        else:
            return self.price() < other.price()
