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
		// Pointer to underlying order book container.
		shared_ptr<order_book_iface> _order_book;

		// Accumulated value of prices.
		double _accumulator;

		// Last time maximum price was changed.
		timestamp_type _last_timestamp;

		// First order timestamp. 
		timestamp_type _first_timestamp;

	public:

		accumulator()
		{
			reset();
		}

		// Init accumulator with order book interface.
		void init(shared_ptr<order_book_iface>& order_book)
		{
			_order_book = order_book;
		}

		// Reset accumulator state.
		void reset()
		{
			_order_book.reset();

			_accumulator = 0;
			_last_timestamp = invalid_timestamp;
			_first_timestamp = invalid_timestamp;
		}

		// Add order to accumulator.
		void add_order(order_item& order)
		{
			// WARNING:
			// We could validate time consistentcy (straight time line), but in case of multi-threading or
			// multiple orders providers orders timestamp could be inconsistent.

			if (!_order_book)
			{
				throw exception("Accumulator not inited.");
			}

			// Check if new order is top-price order and accumulate previous top-price order time. 

			double current_max_price = _order_book->max_price_order().price();

			if (order.price() > current_max_price)
			{
				if (current_max_price > 0)
				{
					_accumulator += current_max_price * (order.timestamp() - _last_timestamp);
				}

				// Update last timestamp of top-price order changing.
				_last_timestamp = order.timestamp();
			}

			_order_book->add(order);

			// If this is first order than remember it's timestamp to calculate duration at the end.

			if (_first_timestamp == invalid_timestamp)
			{
				_first_timestamp = order.timestamp();
			}
		}

		// Remove order from accumulator.
		void remove_order(unsigned id, timestamp_type timestamp)
		{
			if (!_order_book)
			{
				throw exception("Accumulator not inited.");
			}

			// Check if the order being removed is the top-price order.

			const order_item& max_price_order = _order_book->max_price_order();
			if (max_price_order.id() == id)
			{
				// Accumulate top-price order time and update time of top-price order changing.
				_accumulator += max_price_order.price() * (timestamp - _last_timestamp);
				_last_timestamp = timestamp;
			}

			// Remove the order from the book.
			_order_book->remove(id, timestamp);
		}

		// Returns time-weighted average highest price of orders.
		double average_highest_price() const
		{
			if (_last_timestamp == invalid_timestamp || _first_timestamp == invalid_timestamp)
			{
				return 0;
			}
			else
			{
				return _last_timestamp == _first_timestamp ? 0 : _accumulator / (_last_timestamp - _first_timestamp);
			}
		}
	};
}

#endif // _WTEST_ACCUM_H