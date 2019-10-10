#pragma once
#ifndef _WTEST_ORDERBOOK_H
#define _WTEST_ORDERBOOK_H

#include <set>
#include <map>
#include "OrderItem.h"

namespace WG_ORDERBOOK
{
	using namespace std;

	// Interface for order book implementation.
	class order_book_iface
	{
	public:
		virtual void add(order_item& order) = 0;
		virtual void remove(unsigned id, timestamp_type timestamp) = 0;
		virtual const order_item& max_price_order() const = 0;
		virtual ~order_book_iface() = 0 {};
	};

	// Default implementation for order book interface.
	class order_book : public order_book_iface
	{
		typedef set<order_item, order_comparer> orders_stack_type;
		typedef map<unsigned, orders_stack_type::iterator> id_map_type;
		typedef pair<unsigned, orders_stack_type::iterator> id_map_item_type;

		orders_stack_type _orders_stack;
		id_map_type _id_map;

		order_item _null_order;

	public:

		void add(order_item& order)
		{
			auto ret_price = _orders_stack.insert(order);
			if (!ret_price.second)
			{
				throw exception("Cannot insert order.");
			}

			auto ret_id = _id_map.insert(id_map_item_type(order.id(), ret_price.first));
			if (!ret_id.second)
			{
				throw exception("Cannot insert order with the given id.");
			}
		}

		void remove(unsigned id, timestamp_type timestamp)
		{
			if (!_id_map.size())
			{
				throw exception("Cannot remove an order from empty book.");
			}
			else
			{
				auto it = _id_map.at(id);
				_id_map.erase(id);
				_orders_stack.erase(it);
			}
		}

		const order_item& max_price_order() const
		{
			auto it = _orders_stack.rbegin();
			return it == _orders_stack.rend() ? _null_order : *it;
		}

		size_t size() const
		{
			return _id_map.size();
		}
	};
}

#endif // _WTEST_ORDERBOOK_H