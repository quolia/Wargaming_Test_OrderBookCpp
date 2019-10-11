#pragma once
#ifndef _WTEST_ORDERBOOK_H
#define _WTEST_ORDERBOOK_H

#include <set>
#include <unordered_map>
#include <mutex>
#include "OrderItem.h"

namespace WG_ORDERBOOK
{
	using namespace std;

	// Interface for order book implementation.
	class order_book_iface
	{
	public:
		// Adds order.
		virtual void add(order_item& order) = 0;

		// Removes order.
		virtual void remove(unsigned id, timestamp_type timestamp) = 0;

		// Returns top-price order.
		virtual const order_item& max_price_order() = 0;

		// Returns amount of orders in the book.
		virtual size_t size() = 0;

		// Default virtual destructor to allow implementations instances destructors to be called when deleted as abstract class.
		virtual ~order_book_iface() = 0 {};
	};

	// Default implementation for order book interface.
	class order_book : public order_book_iface
	{
		// Types aliases.
		typedef set<order_item, order_comparer> orders_stack_type;
		typedef unordered_map<unsigned, orders_stack_type::iterator> id_map_type;
		typedef pair<unsigned, orders_stack_type::iterator> id_map_item_type;

		// Stack of orders sorted by price and then by timestamp.
		// 'set' type allows sorting and value uniqness.
		orders_stack_type _orders_stack;

		// Supporting 'map' to store 'set' iterator for fast deleting from 'set'.
		id_map_type _id_map;

		// 'set' keeps orders in sort manner.
		// 'map' keeps pointers to 'set' positions by orders id.

		// Default order to return is order book is empty.
		order_item _null_order;

		// Operations mutex.
		mutex _lock;

	public:

		// Default ctor.
		order_book() noexcept
		{
			//
		}

		// Adds order.
		virtual void add(order_item& order) // O(log(n))
		{
			lock_guard<mutex> lock(_lock);

			// Insert order to the 'set'. It will be automatically inserted to a sort-keep position.
			auto ret_price = _orders_stack.insert(order); // O(log(n))
			if (!ret_price.second)
			{
				throw exception("Cannot insert order.");
			}

			// Insert 'set' iterator to 'map'.
			auto ret_id = _id_map.insert(id_map_item_type(order.id(), ret_price.first)); // O(1)
			if (!ret_id.second)
			{
				throw exception("Cannot insert order with the given id.");
			}
		}

		// Removes order.
		virtual void remove(unsigned id, timestamp_type timestamp) // O(1)
		{
			lock_guard<mutex> lock(_lock);

			if (!_id_map.size())
			{
				throw exception("Cannot remove an order from empty book.");
			}

			if (id == 0)
			{
				throw exception("Invalid order id.");
			}

			// Find 'set' iterator in 'map' by order id and remove the pair.
			auto it = _id_map.at(id); // O(1)
			_id_map.erase(id); // O(1)

			// Remove the iterator from 'set'.
			_orders_stack.erase(it); // O(log(n))
		}

		// Returns max price order or default order.
		// The top-price order is located at the end of 'set'.
		virtual const order_item& max_price_order() noexcept
		{
			lock_guard<mutex> lock(_lock);

			auto it = _orders_stack.rbegin();
			return it == _orders_stack.rend() ? _null_order : *it;
		}

		// Amount of orders in the book.
		virtual size_t size() noexcept
		{
			lock_guard<mutex> lock(_lock);

			return _id_map.size();
		}
	};
}

#endif // _WTEST_ORDERBOOK_H