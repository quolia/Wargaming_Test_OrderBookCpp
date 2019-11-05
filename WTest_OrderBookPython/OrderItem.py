from .Types import *

class order_data:
    """Order data."""
    def __init__(self):
        """Ctor."""
        self._price = 0;
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

                friend
                istream & operator >> (istream & stream, order_record & record)
                {
                if (!(stream >> record._timestamp))
                {
                    throw
                exception("Invalid file format.");
                }

                char
                type;

                if (!(stream >> type) | | ('I' != type & & 'E' != type))
                {
                    throw
                exception("Invalid file format.");
                }

                record._is_insert = 'I' == type;

                if (!(stream >> record._id))
                {
                    throw
                exception("Invalid file format.");
                }

                if (record._is_insert)
                    {
                    if (!(stream >> record._price))
                    {
                        throw
                    exception("Invalid file format.");
                    }
                    }
                    else
                    {
                        record._price = 0;
                    }

                    record.validate();
                    return stream;
                    }
                    };

                    // / < summary > Order
                    item


                    class . < / summary >


                    class order_item: protected


                    order_data
                    {
                        protected:

                            unsigned _id; // / < summary > Order
                    id. < / summary >

                            public:

                    // / < summary > Default
                    ctor. < / summary >
                              order_item()
                    noexcept
                    : _id(0)
                    {
                    //
                    }

                    // / < summary > Data
                    ctor. < / summary >
                    // / < param
                    name = "id" > Order
                    id. < / param >
                    // / < param
                    name = "timestamp" > Order
                    timestamp. < / param >
                    // / < param
                    name = "price" > Order
                    price. < / param >
                               order_item(unsigned
                    id, timestamp_type
                    timestamp, double
                    price) noexcept
                    : _id(id)
                    {
                        _timestamp = timestamp;
                    _price = price;
                    }

                    // / < summary > Copy
                    ctor
                    to
                    copy
                    from order record.< / summary >
                    // / < param
                    name = "record" > Record
                    to
                    make
                    order
                    copy
                    from . < / param >
                               order_item(const
                    order_record & record) noexcept
                    : _id(record.id())
                    {
                        _timestamp = record.timestamp();
                    _price = record.price();
                    }

                    // / < summary > Data
                    ctor
                    to
                    copy
                    from order data.< / summary >
                    // / < param
                    name = "data" > Data
                    to
                    make
                    order
                    copy
                    from . < / param >
                               order_item(unsigned
                    id, const
                    order_data & data) noexcept
                    : _id(id)
                    {
                        _timestamp = data.timestamp();
                    _price = data.price();
                    }

                    // / < summary > Returns
                    order
                    's data without id. </summary>
                    order_data & data()
                    const
                    noexcept
                    {
                    return *(order_data *)
                    this;
                    }

                    // / < summary > Returns
                    order
                    id. < / summary >
                            unsigned
                    id()
                    const
                    noexcept
                    {
                    return _id;
                    }

                    // / < summary > Returns
                    order
                    price. < / summary >
                               double
                    price()
                    const
                    noexcept
                    {
                    return _price;
                    }

                    // / < summary > Returns
                    order
                    timestamp. < / summary >
                                   timestamp_type
                    timestamp()
                    const
                    noexcept
                    {
                    return _timestamp;
                    }
                    };

                    // / < summary > Comparer
                    to
                    use in set
                    to
                    sort
                    order
                    items. < / summary >


                    class order_comparer
                        {
                            public:

                        // / < summary > Implements
                        'less'
                        operation. < / summary >
                        // / < param
                        name = "l" > Left
                        operand. < / param >
                        // / < param
                        name = "r" > Right
                        operand. < / param >
                                     bool
                        operator()(const
                        order_item & l, const
                        order_item & r) const
                        noexcept
                        {
                        // If
                        prices
                        are
                        equal
                        than
                        compare
                        timestamps and than
                        ids.

                        if (l.price() == r.price())
                        {
                        if (l.timestamp() == r.timestamp())
                        {
                        if (l.id() == r.id())
                        {


                    return false; // The
                    same
                    order is always
                    not less
                    than
                    itself.
                    }
                    else
                    {
                    return l.id() < r.id();
                    }
                    }
                    else
                    {
                    return l.timestamp() < r.timestamp();
                    }
                    }
                    else
                    {
                    return l.price() < r.price();
                    }
                    }
                    };
                    }

                    # endif // _WTEST_ORDERITEM_H