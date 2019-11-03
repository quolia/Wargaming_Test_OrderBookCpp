
# ifdef MT
# include <mutex>
# endif
import OrderItem

#// / < summary > Interface for order book implementation.< / summary >


class order_book_iface:

        #public:

    #// / < summary > Adds    order. < / summary >
    #// / < param    name = "order" > Order    to    add. < / param >
    virtual    void    add(const    order_item & order) = 0;

    #// / < summary > Removes    order. < / summary >
    #// / < param    name = "id" > Previously    added    order    id. < / param >
    #// / < param    name = "timestamp" > Current    timestamp. < / param >
    virtual    void    remove(unsigned    id) = 0;

    #// / < summary > Returns    top - price    order. < / summary >
    virtual    const    order_item & max_price_order() = 0;

    #// / < summary > Returns    amount    of    orders in the    book. < / summary >
    virtual    size_t    size() = 0;

    #// / < summary > Default    virtual    destructor    to    allow    implementations    instances   destructors    to    be    called    when    deleted as abstract    class . < / summary >

    virtual    ~order_book_iface() = 0
    {};



#// / < summary > Defaultimplementationfor order book interface.< / summary >


class order_book: public order_book_iface

#// Types aliases.
    typedef set < order_item, order_comparer > orders_container_type;
    typedef unordered_map < unsigned, order_data > orders_map_type;
    typedef pair < unsigned, order_data > orders_map_pair_type;

orders_container_type _orders; #// / < summary > Container of orders. < / summary >
            orders_map_type _orders_map; #// / < summary > Supporting 'map' to store order id and data. < / summary >
                 order_item _null_order; #// / < summary > Default order to return if order book is empty.< / summary >

# ifdef MT
#mutex _lock; // / < summary > Operations mutex. < / summary >
# endif

#public:

#// / < summary > Adds order. < / summary >
#// / < param name = "order" > Order to add.O(log(n)). < / param >
virtual void add(const order_item & order)

    # ifdef MT
    # lock_guard < mutex > lock(_lock);
    # endif
    #// Insert order to the 'set'.It will be automatically inserted to a sort - keep position.
    auto result = _orders.insert(order); #// O(log(n))
    if (!result.second):
        throw exception("Cannot insert order.")

    #// Insert order to 'map'.
    auto map_result = _orders_map.insert(orders_map_pair_type(order.id(), order.data())); #// O(1)
    if (!map_result.second):
        _orders.erase(order)
        throw exception("Cannot insert order with the given id.")

    #// / < summary > Removes order. O(log(n)). # < / summary >
    #// / < param name = "id" > Previously added order id. < / param >
virtual void remove(unsigned id)

    # ifdef MT
    # lock_guard < mutex > lock(_lock);
    # endif
    if (0 == id):
        throw exception("Invalid order id.")

    #// Find order in 'map' by order id and remove it.
    auto order_data = _orders_map.at(id); #// O(1)
    _orders_map.erase(id); // O(1)

    # // Remove the order from 'set'.
    _orders.erase(order_item(id, order_data)); // O(log(n))


#// / < summary > Returns top - price order.The top - price order is located at the end of 'set'. < / summary >
virtual const order_item & max_price_order() noexcept

    # ifdef MT
    #lock_guard < mutex > lock(_lock);
    # endif
    auto it = _orders.rbegin();
    return it == _orders.rend() ? _null_order: *it;


#// / < summary > Returns amount of orders in the book. < / summary >
virtual size_t size() noexcept

    # ifdef MT
    #lock_guard < mutex > lock(_lock);
    # endif
    return _orders_map.size();