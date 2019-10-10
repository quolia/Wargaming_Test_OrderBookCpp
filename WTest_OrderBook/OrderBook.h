#pragma once
#ifndef _WTEST_ORDERBOOK_H
#define _WTEST_ORDERBOOK_H

#include <list>
#include <set>
#include <map>
#include <cstddef>

namespace WG_ORDERBOOK
{
	using namespace std;

	typedef unsigned timestamp_type;

	// Order item class.
	class order_item
	{
		unsigned _id;
		double _price;
		timestamp_type _timestamp;

	public:

		order_item()
		{
			_id = 0;
			_timestamp = 0;
			_price = 0;
		}

		order_item(unsigned id, timestamp_type timestamp, double price)
		{
			_id = id;
			_timestamp = timestamp;
			_price = price;
		}

		unsigned id() const
		{
			return _id;
		}

		double price() const
		{
			return _price;
		}

		timestamp_type timestamp() const
		{
			return _timestamp;
		}

		// Less-operator overload to use in multimap to order by price and timestamp.
		bool const operator<(const order_item& item)
		{
			return _price == item._price ? _timestamp < item._timestamp : _price < item._price;
		}
	};

	class order_book
	{
		typedef multimap<double, order_item> price_stack_type;
		typedef map<unsigned, price_stack_type::iterator> id_map_type;
		typedef pair<double, order_item> price_stack_item_type;
		typedef pair<unsigned, price_stack_type::iterator> id_map_item_type;

		price_stack_type _price_stack;
		id_map_type _id_map;

		order_item _null_order;

	public:

		void add(order_item& order)
		{
			auto ret_price = _price_stack.insert(price_stack_item_type(order.price(), order));
			auto ret_id = _id_map.insert(id_map_item_type(order.id(), ret_price));
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

				if (it == --_price_stack.end())
				{
					int a = 1; ////!!!!!
				}

				_price_stack.erase(it);
			}
		}

		double current_maximum_price() const
		{
			return max_price_order().price();
		}

		const order_item& max_price_order() const
		{
			auto it = _price_stack.rbegin();
			return it == _price_stack.rend() ? _null_order : it->second;
		}

		size_t size() const
		{
			return _id_map.size();
		}
	};

	class accumulator
	{
		order_book* _order_book;
		double _accumulator;
		timestamp_type _last_timestamp;
		timestamp_type _first_timestamp;

	public:

		accumulator()
		{
			reset();
		}

		void init(order_book* order_book)
		{
			_order_book = order_book;
		}

		void reset()
		{
			_accumulator = 0;
			_last_timestamp = 0;
			_first_timestamp = 0;
		}

		void add_order(order_item& order)
		{
			double current_max_price = _order_book->current_maximum_price();
			if (current_max_price > 0)
			{
				_accumulator += current_max_price * (order.timestamp() - _last_timestamp);
			}

			_last_timestamp = order.timestamp();
			_order_book->add(order);

			if (_first_timestamp == 0)
			{
				_first_timestamp = order.timestamp();
			}
		}

		void remove_order(unsigned id, timestamp_type timestamp)
		{
			const order_item& max_price_order = _order_book->max_price_order();
			if (max_price_order.id() == id)
			{
				_accumulator += max_price_order.price() * (timestamp - _last_timestamp);
				_last_timestamp = timestamp;
			}
			_order_book->remove(id, timestamp);
		}

		double average_highest_price() const
		{
			return _last_timestamp == _first_timestamp ? 0 : _accumulator / (_last_timestamp - _first_timestamp);
		}
	};
}

#endif // _WTEST_ORDERBOOK_H