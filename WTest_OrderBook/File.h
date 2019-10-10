#pragma once
#ifndef  _WTEST_FILE_H
#define _WTEST_FILE_H

#include <string>
#include <fstream>
#include <cstddef>

namespace WG_ORDERBOOK
{
	using namespace std;

	// Simple wrapper for a file.
	class orders_file
	{
		ifstream _stream;

	public:

		orders_file()
		{

		}

		~orders_file()
		{
			close();
		}

		void close()
		{
			if (is_opened())
			{
				_stream.close();
			}
		}

		void open_for_read(const string& file_name)
		{
			close();

			_stream.open(file_name);
			if (!is_opened())
			{
				throw exception("Cannot open file.");
			}
		}

		bool read_order_record(order_record& order)
		{
			if (!is_opened())
			{
				throw exception("File is not opened.");
			}

			if (_stream.eof())
			{
				return false;
			}
			else
			{
				if (!(_stream >> order.timestamp))
				{
					throw exception("Invalid file format.");
				}

				char type;

				if (!(_stream >> type) || (type != 'I' && type != 'E'))
				{
					throw exception("Invalid file format.");
				}

				order.is_insert = type == 'I';

				if (!(_stream >> order.id))
				{
					throw exception("Invalid file format.");
				}

				if (order.is_insert)
				{
					if (!(_stream >> order.price))
					{
						throw exception("Invalid file format.");
					}
				}

				return true;
			}
		}

		bool const is_opened()
		{
			return _stream.is_open();
		}
	};
}

#endif // ! _WTEST_FILE_H