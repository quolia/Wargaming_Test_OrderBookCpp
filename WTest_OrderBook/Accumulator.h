#pragma once
#ifndef _WTEST_ACCUM_H
#define _WTEST_ACCUM_H

#include "OrderItem.h"
#include "OrderBook.h"

namespace WG_ORDERBOOK
{
	using namespace std;

	class accumulator
	{
		shared_ptr<order_book_iface> _order_book;

		double _accumulator;
		timestamp_type _last_timestamp;
		timestamp_type _first_timestamp;

	public:

		accumulator()
		{
			reset();
		}

		void init(shared_ptr<order_book_iface>& order_book)
		{
			_order_book = order_book;
		}

		void reset()
		{
			_order_book = nullptr;

			_accumulator = 0;
			_last_timestamp = 0;
			_first_timestamp = 0;
		}

		void add_order(order_item& order)
		{
			double current_max_price = _order_book->max_price_order().price();
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

#endif // _WTEST_ACCUM_H