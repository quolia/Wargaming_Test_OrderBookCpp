from .Types import *

class order_data:
    """Order data."""
    def __init__(self):
        """Ctor."""
        self._price = 0
        self._timestamp = invalid_timestamp

    def timestamp(self):
        """Returns order timestamp."""
        return self._timestamp

    def price(self):
        """Returns order price."""
        return self._price

class order_record(order_data):
    """Order record in source file."""
    def __init__(self):
        """Ctor."""
        self._id = 0 #// / < summary > Order id. < / summary >
        self._is_insert = False #// / < summary > Is insert operation. < / summary >

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

    def init(self, string):
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
        self._id = parts[2]
        self._price = 0 if not self._is_insert else float(parts[3])

class order_item(order_data):
    """Order item class."""
    def __init__(self):
        """Ctor."""
        self._id = 0 #// / < summary > Order id. < / summary >

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


    #// / < summary > Returns order's data without id. </summary>
    def data(self):
        return super

    #// / < summary > Returns order id. < / summary >
    def id(self):
        return self._id

    #// / < summary > Returns order price. < / summary >
    def price(self):
        return self._price

    #// / < summary > Returns order timestamp. < / summary >
    def timestamp(self):
        return self._timestamp

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