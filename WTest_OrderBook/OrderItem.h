#pragma once
#ifndef _WTEST_ORDERITEM_H
#define _WTEST_ORDERITEM_H

#include "Types.h"

namespace WG_ORDERBOOK
{
	using namespace std;

	/// <summary> Order record in source file. </summary>
	struct order_record
	{
		unsigned id;				/// <summary> Order id. </summary>
		timestamp_type timestamp;	/// <summary> Order timestamp. </summary>
		bool is_insert;				/// <summary> Is insert operation. </summary>
		double price;				/// <summary> Order price (valid for insert operation). </summary>

		/// <summary> Default ctor. </summary>
		order_record() noexcept
		{
			timestamp = invalid_timestamp;
			id = 0;
			is_insert = false;
			price = 0;
		}

		/// <summary> Validates order record data. </summary>
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

	/// <summary> Order item class. </summary>
	class order_item
	{
		unsigned _id;				/// <summary> Order id. </summary>
		double _price;				/// <summary> Order price. </summary>
		timestamp_type _timestamp;	/// <summary> Order timestamp. </summary>

	public:

		/// <summary> Default ctor. </summary>
		order_item() noexcept
			: _id(0), _timestamp(invalid_timestamp), _price(0)
		{
			//
		}

		/// <summary> Data ctor. </summary>
		/// <param name="id"> Order id. </param>
		/// <param name="timestamp"> Order timestamp. </param>
		/// <param name="price"> Order price. </param>
		order_item(unsigned id, timestamp_type timestamp, double price) noexcept
			: _id(id), _timestamp(timestamp), _price(price)
		{
			//
		}

		/// <summary> Copy ctor to copy from order record. </summary>
		/// <param name="record"> Record to make order copy from. </param>
		order_item(const order_record& record) noexcept
			: _id(record.id), _timestamp(record.timestamp), _price(record.price)
		{
			//
		}

		/// <summary> Returns order id. </summary>
		unsigned id() const noexcept
		{
			return _id;
		}

		/// <summary> Returns order price. </summary>
		double price() const noexcept
		{
			return _price;
		}

		/// <summary> Returns order timestamp. </summary>
		timestamp_type timestamp() const noexcept
		{
			return _timestamp;
		}
	};

	/// <summary> Comparer to use in set to sort items by price and timestamp (functor). </summary>
	class order_comparer
	{
	public:
		bool operator()(const order_item& l, const order_item& r) const noexcept
		{
			// If the prices are equal than compare timestamps.
			return l.price() == r.price() ? l.timestamp() < r.timestamp() : l.price() < r.price();
		}
	};
}

#endif // _WTEST_ORDERITEM_H