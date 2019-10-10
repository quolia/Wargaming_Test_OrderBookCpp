#pragma once
#include "CLI.h"
#include <iostream>
#include "File.h"
#ifndef  _WTEST_APP_H
#define _WTEST_APP_H


namespace WG_ORDERBOOK
{
	using namespace std;

	class application
	{
		bool _is_inited;
		orders_file _src_file;
		shared_ptr<order_book_iface> _order_book;
		accumulator _accumulator;
	
	public:

		application()
		{
			_is_inited = false;
		}

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

		void run()
		{
			if (!_is_inited)
			{
				throw exception("Application has not been inited yet.");
			}

			order_record order_record;

			while (_src_file.read_order_record(order_record))
			{
				if (order_record.is_insert)
				{
					order_item order = order_record;
					_accumulator.add_order(order);
				}
				else
				{
					_accumulator.remove_order(order_record.id, order_record.timestamp);
				}
			}
		}

		double average_highest_price() const
		{
			return _accumulator.average_highest_price();
		}
	};
}

#endif // _WTEST_APP_H