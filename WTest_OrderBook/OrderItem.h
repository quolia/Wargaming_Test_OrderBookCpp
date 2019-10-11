#pragma once
#ifndef _WTEST_ORDERITEM_H
#define _WTEST_ORDERITEM_H

#include "Types.h"

namespace WG_ORDERBOOK
{
	using namespace std;

	// Order record in source file.
	struct order_record
	{
		timestamp_type timestamp;
		unsigned id;
		bool is_insert;
		double price;

		// Default ctor.
		order_record() noexcept
		{
			timestamp = invalid_timestamp;
			id = 0;
			is_insert = false;
			price = 0;
		}

		// Validates order record data.
		void validate()
		{
			if (id < 1)
			{
				throw exception("Invalid order id.");
			}

			if (invalid_timestamp == timestamp)
			{
				throw exception("Invalid order timestamp.");
			}

			if (is_insert && price < 0)
			{
				throw exception("Invalid order price.");
			}
			
			if (!is_insert && price != 0)
			{
				throw exception("Invalid order data.");
			}
		}
	};

	// Order item class.
	class order_item
	{
		unsigned _id;
		double _price;
		timestamp_type _timestamp;

	public:

		// Default ctor.
		order_item() noexcept
		{
			_id = 0;
			_timestamp = invalid_timestamp;
			_price = 0;
		}

		// Data ctor.
		order_item(unsigned id, timestamp_type timestamp, double price) noexcept
		{
			_id = id;
			_timestamp = timestamp;
			_price = price;
		}

		// Copy ctor to copy from order record.
		order_item(const order_record& record) noexcept
		{
			_id = record.id;
			_timestamp = record.timestamp;
			_price = record.price;
		}

		// Returns order id.
		unsigned id() const noexcept
		{
			return _id;
		}

		// Returns order price.
		double price() const noexcept
		{
			return _price;
		}

		// Returns order timestamp.
		timestamp_type timestamp() const noexcept
		{
			return _timestamp;
		}
	};

	// Comparer to use in set to sort items by price and timestamp.
	class order_comparer
	{
	public:
		bool operator()(const order_item& l, const order_item& r) const noexcept
		{
			// If the prices are equal than compare timestamp.
			return l.price() == r.price() ? l.timestamp() < r.timestamp() : l.price() < r.price();
		}
	};
}

#endif // _WTEST_ORDERITEM_H