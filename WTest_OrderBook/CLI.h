#pragma once
#ifndef _WTEST_CLI_H
#define _WTEST_CLI_H

#include <string>

namespace WG_ORDERBOOK
{
	using namespace std;

	// Command line parameters validator.
	class command_line
	{
		string _src_file_name;

	public:

		const char* src_file_name() const
		{
			return _src_file_name.c_str();
		}

		void init(int argc, char* argv[])
		{
			if (argc < 2)
			{
				throw exception("Invalid parameters count. Example parameters: srcfile");
			}

			if (!argv)
			{
				throw exception("Parameters missing. Example parameters: srcfile");
			}

			_src_file_name = argv[1];
		}
	};
}

#endif // _WTEST_CLI_H