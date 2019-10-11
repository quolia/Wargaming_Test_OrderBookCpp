#pragma once
#ifndef _WTEST_ACCUM_H
#define _WTEST_ACCUM_H

#include <mutex>
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
		double _accumulator_price;

		// Accumulated value of time.
		double _accumulator_time;

		// Last time maximum price was changed.
		timestamp_type _last_timestamp;

		// First order timestamp (after start or time gap). 
		timestamp_type _first_timestamp;

		// Operations mutex.
		mutex _lock;

	public:

		// Default ctor.
		accumulator() noexcept
		{
			reset();
		}

		// Init accumulator with order book interface.
		void init(shared_ptr<order_book_iface>& order_book) noexcept
		{
			_order_book = order_book;
		}

		// Reset accumulator state.
		void reset() noexcept
		{
			lock_guard<mutex> lock(_lock);

			_order_book.reset();

			_accumulator_price = 0;
			_accumulator_time = 0;
			_last_timestamp = invalid_timestamp;
			_first_timestamp = invalid_timestamp;
		}

		// Add order to accumulator.
		void add_order(order_item& order)
		{
			// WARNING:
			// We could validate time consistentcy (straight time line), but in case of multi-threading or
			// multiple orders providers timestamps could be inconsistent.

			lock_guard<mutex> lock(_lock);

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
					_accumulator_price += current_max_price * (order.timestamp() - _last_timestamp);
				}

				// Update last timestamp of top-price order changing.
				_last_timestamp = order.timestamp();
			}

			_order_book->add(order);

			// If this is first order than remember it's timestamp to calculate duration at the end.

			if (invalid_timestamp == _first_timestamp)
			{
				_first_timestamp = order.timestamp();
			}
		}

		// Remove order from accumulator.
		void remove_order(unsigned id, timestamp_type timestamp)
		{
			lock_guard<mutex> lock(_lock);

			if (!_order_book)
			{
				throw exception("Accumulator not inited.");
			}

			// Check if the order being removed is the top-price order.

			const order_item& max_price_order = _order_book->max_price_order();
			if (max_price_order.id() == id)
			{
				// Accumulate top-price order time and update time of top-price order changing.
				_accumulator_price += max_price_order.price() * (timestamp - _last_timestamp);
				_last_timestamp = timestamp;
			}

			// Remove the order from the book.
			_order_book->remove(id, timestamp);

			if (0 == _order_book->size())
			{
				_accumulator_time += (timestamp - _first_timestamp);
				_first_timestamp = invalid_timestamp;
			}
		}

		// Returns time-weighted average highest price of orders.
		double average_highest_price() noexcept
		{
			lock_guard<mutex> lock(_lock);

			return 0 == _accumulator_time ? 0 : _accumulator_price / _accumulator_time;
		}
	};
}

#endif // _WTEST_ACCUM_H