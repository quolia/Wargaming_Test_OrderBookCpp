#pragma once
#ifndef _WTEST_ORDERITEM_H
#define _WTEST_ORDERITEM_H

#include "Types.h"

namespace WG_ORDERBOOK
{
	using namespace std;

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
	};

	// Comparer to use in set to order items by price and timestamp.
	class order_comparer
	{
	public:
		bool operator()(const order_item& l, const order_item& r) const
		{
			return l.price() == r.price() ? l.timestamp() < r.timestamp() : l.price() < r.price();
		}
	};
}

#endif // _WTEST_ORDERITEM_H