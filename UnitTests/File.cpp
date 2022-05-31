#include "pch.h"
#include "CppUnitTest.h"
#include "../WTest_OrderBook/File.h"
#include "Utils.h"

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
			catch (const exception&)
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
			catch (const exception&)
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
			catch (const exception&)
			{
				//
			}
		}

		TEST_METHOD(Test_File_file_open_and_close)
		{
			orders_file file;

			try
			{
				file.open_for_read("../UnitTests/TestOrders/valid10.5.txt");
				file.close();
			}
			catch (const exception& e)
			{
				string str = e.what();
				Assert::Fail(utils::widen(str).c_str());
			}

			Assert::IsFalse(file.is_opened(), L"File is still opened.");
		}

		TEST_METHOD(Test_File_file_read_from_invalid)
		{
			try
			{
				orders_file file;
				file.open_for_read("../UnitTests/TestOrders/invalid.txt");

				order_record order;
				file.read_order_record(order);
				Assert::Fail(L"Exception missing.");
			}
			catch (const exception&)
			{
				//
			}
		}

		TEST_METHOD(Test_File_file_read_from_empty)
		{
			try
			{
				orders_file file;
				file.open_for_read("../UnitTests/TestOrders/empty.txt");
				order_record order;
				Assert::IsFalse(file.read_order_record(order), L"Read from empty.");
			}
			catch (const exception&)
			{
				//
			}
		}
	};
}
