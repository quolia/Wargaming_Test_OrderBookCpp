#pragma once
#ifndef  _WTEST_FILE_H
#define _WTEST_FILE_H

#include <string>
#include <fstream>
#include <cstddef>
#include "OrderItem.h"

namespace WG_ORDERBOOK
{
	using namespace std;

	// Simple wrapper for a file.
	class orders_file
	{
		// Stream to read.
		ifstream _stream;

	public:

		~orders_file()
		{
			close();
		}

		// Close file if opened.
		void close()
		{
			if (is_opened())
			{
				_stream.close();
			}
		}

		// Opens file for read.
		void open_for_read(const char* file_name)
		{
			close();

			_stream.open(file_name);
			if (!is_opened())
			{
				throw exception("Cannot open file.");
			}
		}

		// Reads and validate orders records.
		bool read_order_record(order_record& record)
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
				if (!(_stream >> record.timestamp))
				{
					throw exception("Invalid file format.");
				}

				char type;

				if (!(_stream >> type) || (type != 'I' && type != 'E'))
				{
					throw exception("Invalid file format.");
				}

				record.is_insert = type == 'I';

				if (!(_stream >> record.id))
				{
					throw exception("Invalid file format.");
				}

				if (record.is_insert)
				{
					if (!(_stream >> record.price))
					{
						throw exception("Invalid file format.");
					}
				}

				record.validate();

				return true;
			}
		}

		// Checks if file is opened.
		bool const is_opened()
		{
			return _stream.is_open();
		}
	};
}

#endif // ! _WTEST_FILE_H