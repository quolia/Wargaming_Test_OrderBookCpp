// WTest_OrderBook.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include "OrderBook.h"
#include "Accumulator.h"
#include "App.h"

using namespace std;
using namespace WG_ORDERBOOK;

int main(int argc, char* argv[])
{
	cout << "Started" << endl;

	try
	{
		application app;
		app.init(argc, argv);
		app.run();

		cout << app.average_highest_price() << endl;

		cout << "Done" << endl;
		return 0;
	}
	catch (const exception& e)
	{
		cout << "Error: " << e.what() << endl;
		exit(-1);
	}
}