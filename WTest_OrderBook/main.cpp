// WTest_OrderBook.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include "App.h"

using namespace std;
using namespace WG_ORDERBOOK;

int main(int argc, char* argv[])
{
	cout << "Started" << endl;

	try
	{
		// Create application instance, initiate it and run.
		application app;
		app.init(argc, argv);
		app.run();

		// Output result.
		cout << "Time-weighted average highest price of orders: " << app.average_highest_price() << endl;

		cout << "Done" << endl;
		return 0;
	}
	catch (const exception& e) // Catch all exceptions and exit.
	{
		cout << "Error: " << e.what() << endl;
		exit(-1);
	}
}