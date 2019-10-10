// WTest_OrderBook.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include "OrderBook.h"

using namespace std;
using namespace WG_ORDERBOOK;

int main()
{
    cout << "Started" << endl;

	order_book book;
	accumulator accum;
	accum.init(&book);	

	order_item o100(100, 1000, 10);
	order_item o101(101, 2000, 13);
	order_item o102(102, 2200, 13);

	cout << book.current_maximum_price() << endl;

	accum.add_order(o100);

	cout << book.current_maximum_price() << endl;

	accum.add_order(o101);

	cout << book.current_maximum_price() << endl;

	accum.add_order(o102);

	cout << book.current_maximum_price() << endl;

	cout << "---" << endl;

	accum.remove_order(101, 2400);
	cout << book.current_maximum_price() << endl;
	accum.remove_order(102, 2500);
	cout << book.current_maximum_price() << endl;
	accum.remove_order(100, 4000);
	cout << book.current_maximum_price() << endl;

	cout << accum.average_highest_price() << endl;
}