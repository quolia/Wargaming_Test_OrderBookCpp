#pragma once
#ifndef  _WTEST_APP_H
#define _WTEST_APP_H

#include <iostream>
#include "CLI.h"
#include "File.h"
#include "OrderBook.h"
#include "Accumulator.h"

namespace WG_ORDERBOOK
{
	using namespace std;

	/// <summary> Application class. </summary>
	class application
	{
		volatile bool _is_inited;					/// <summary> The flag is true if the application instance has been inited successfully. </summary>
		orders_file _src_file;						/// <summary> File to read. </summary>
		shared_ptr<order_book_iface> _order_book;	/// <summary> Pointer to order book interface. </summary>
		accumulator _accumulator;					/// <summary> Orders time-weight accumulator. </summary>
	
	public:

		/// <summary> Default ctor. </summary>
		application() noexcept
		{
			_is_inited = false;
		}

		/// <summary> Initiate application instance. </summary>
		/// <param name="argc"> Amoung of command line parameters. </param>
		/// <param name="argv"> Command line parameters. </param>
		void init(int argc, char* argv[])
		{
			_is_inited = false;

			command_line cli_params;
			cli_params.init(argc, argv);

			cout << "Source file: " << cli_params.src_file_name() << endl;
			_src_file.open_for_read(cli_params.src_file_name());

			_order_book.reset(new order_book());
			_accumulator.init(_order_book);

			_is_inited = true;
		}

		/// <summary> Reads source file till the end. </summary>
		void run()
		{
			if (!_is_inited)
			{
				throw exception("Application has not been inited yet.");
			}

			order_record record;
			while (_src_file.read_order_record(record))
			{
				if (record.is_insert())
				{
					_accumulator.add_order(record);
				}
				else
				{
					_accumulator.remove_order(record.id(), record.timestamp());
				}
			}
		}

		/// <summary> Returns time-weighted average highest price of orders. </summary>
		/// <returns> Time-weighted average highest price of orders. </returns>
		double average_highest_price()
		{
			if (!_is_inited)
			{
				throw exception("Application has not been inited yet.");
			}

			return _accumulator.average_highest_price();
		}
	};
}

#endif // _WTEST_APP_H