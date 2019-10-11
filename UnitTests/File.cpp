#include "pch.h"
#include "CppUnitTest.h"
#include "../WTest_OrderBook/File.h"
using namespace WG_ORDERBOOK;

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

namespace UnitTests
{
	TEST_CLASS(Test_File)
	{
	public:

		TEST_METHOD(Test_File_file_not_exists)
		{
			try
			{
				orders_file file;
				file.open_for_read("not_exists.txt");
				Assert::Fail(L"Exception missing.");
			}
			catch (const exception & e)
			{
				//
			}
		}

		TEST_METHOD(Test_File_file_not_opened)
		{
			orders_file file;

			try
			{	
				file.open_for_read("not_exists.txt");
				Assert::Fail(L"Exception missing.");
			}
			catch (const exception & e)
			{
				Assert::IsFalse(file.is_opened(), L"File is opened.");
			}
		}

		TEST_METHOD(Test_File_file_read_from_not_opened)
		{
			orders_file file;

			try
			{
				order_record order;
				file.read_order_record(order);
				Assert::Fail(L"Exception missing.");
			}
			catch (const exception & e)
			{
				//
			}
		}
	};
}
