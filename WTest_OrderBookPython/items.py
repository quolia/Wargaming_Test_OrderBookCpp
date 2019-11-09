invalid_timestamp = int(-1)


class OrderData:
    """Order data."""

    def __init__(self):
        self._price = int(0)                 # Order price.
        self._timestamp = invalid_timestamp  # Order timestamp.

    def timestamp(self):
        """Returns order timestamp."""
        return self._timestamp

    def price(self):
        """Returns order price."""
        return self._price


class OrderRecord(OrderData):
    """Order record in source file."""

    def __init__(self):
        super().__init__()
        self._id = int(0)        # Order id.
        self._is_insert = False  # Is insert operation.

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
        Initializes instance with text string.

        Strings example:
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


class OrderItem(OrderData):
    """Order item class."""

    def __init__(self):
        super().__init__()
        self._id = int(0) # Order id.

    @classmethod
    def from_record(cls, record: OrderRecord):
        """
        Converts OrderRecord to OrderItem instance.
        :param record: OrderRecord instance.
        :return: OrderItem record.
        """
        order = OrderItem()
        order._id = record.id()
        order._timestamp = record.timestamp()
        order._price = record.price()
        return order

    @classmethod
    def from_data(cls, order_id: int, data: OrderData):
        """
        Converts OrderData to OrderItem instance.
        :param order_id: Order id.
        :param data: Order data.
        :return: OrderItem record.
        """
        order = OrderItem()
        order._id = order_id
        order._timestamp = data.timestamp()
        order._price = data.price()
        return order

    @classmethod
    def from_id(cls, order_id: int, timestamp: int, price: float):
        """
        Converts OrderData to OrderItem instance.
        :param order_id: Order id.
        :param timestamp: Order timestamp.
        :param price: Order price.
        :return: OrderItem record.
        """
        order = OrderItem()
        order._id = order_id
        order._timestamp = timestamp
        order._price = price
        return order

    def data(self):
        """Returns order's data without id."""
        data = OrderData()
        data._timestamp = self.timestamp()
        data._price = self.price()
        return data

    def id(self):
        """Returns order id."""
        return self._id

    def __eq__(self, other):
        return self.id() == other.id()

    def __hash__(self):
        return self.id()

    def __lt__(self, other):
        """If prices are equal than compare timestamps and than ids."""
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
