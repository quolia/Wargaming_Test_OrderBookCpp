#include "pch.h"
#include "CppUnitTest.h"
#include "../WTest_OrderBook/CLI.h"

using namespace WG_ORDERBOOK;
using namespace Microsoft::VisualStudio::CppUnitTestFramework;

namespace UnitTests
{
	TEST_CLASS(Test_CLI)
	{
	public:
		
		TEST_METHOD(Test_CLI_invalid_count)
		{
			try
			{
				command_line cli;
				cli.init(1, nullptr);

				Assert::Fail(L"Exception missing.");
			}
			catch (const exception&)
			{
				//
			}
		}

		TEST_METHOD(Test_CLI_invalid_args)
		{
			try
			{
				command_line cli;
				cli.init(2, nullptr);

				Assert::Fail(L"Exception missing.");
			}
			catch (const exception&)
			{
				//
			}
		}

		TEST_METHOD(Test_CLI_file_name)
		{
			char* argv[2] = {"path", "test.txt"};

			command_line cli;
			cli.init(2, argv);

			Assert::AreEqual(cli.src_file_name(), argv[1]);
		}
	};
}
