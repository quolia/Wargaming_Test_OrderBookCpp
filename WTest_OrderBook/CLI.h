#pragma once
#ifndef _WTEST_CLI_H
#define _WTEST_CLI_H

#include <string>

namespace WG_ORDERBOOK
{
	using namespace std;

	/// <summary> Command line parameters validator. </summary>
	class command_line
	{
		string _src_file_name; /// <summary> File name string. </summary>

	public:

		/// <summary> Source file name. </summary>
		/// <returns> File name pointer. </returns>
		const char* src_file_name() const noexcept
		{
			return _src_file_name.c_str();
		}
 
		/// <summary> Initiate and validate command line parameters. </summary>
		/// <param name="argc"> Amoung of command line parameters. </param>
		/// <param name="argv"> Command line parameters. </param>
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