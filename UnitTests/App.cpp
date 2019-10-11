#include "pch.h"
#include "CppUnitTest.h"
#include "Utils.h"
#include "../WTest_OrderBook/App.h"
using namespace WG_ORDERBOOK;

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

namespace UnitTests
{
	TEST_CLASS(Test_App)
	{
	public:

		TEST_METHOD(Test_App_invalid_init)
		{
			try
			{
				application app;
				app.init(1, nullptr);

				Assert::Fail(L"Exception missing.");
			}
			catch (const exception & e)
			{
				//
			}
		}

		TEST_METHOD(Test_App_invalid_args)
		{
			try
			{
				application app;
				app.init(2, nullptr);

				Assert::Fail(L"Exception missing.");
			}
			catch (const exception & e)
			{
				//
			}
		}

		TEST_METHOD(Test_App_file_not_exists)
		{
			char* argv[2] = { "path", "test.txt" };

			try
			{
				application app;
				app.init(2, argv);

				Assert::Fail(L"Exception missing.");
			}
			catch (const exception & e)
			{
				//
			}
		}

		TEST_METHOD(Test_App_not_inited)
		{
			try
			{
				application app;
				app.run();

				Assert::Fail(L"Exception missing.");
			}
			catch (const exception & e)
			{
				//
			}
		}

		TEST_METHOD(Test_App_not_inited2)
		{
			try
			{
				application app;
				app.average_highest_price();

				Assert::Fail(L"Exception missing.");
			}
			catch (const exception & e)
			{
				//
			}
		}

		TEST_METHOD(Test_App_valid_file)
		{
			char* argv[2] = { "path", "../UnitTests/TestOrders/valid10.5.txt" };

			try
			{
				application app;
				app.init(2, argv);
				app.run();
				Assert::IsTrue(app.average_highest_price() == 10.5, L"Incorrect result.");
			}
			catch (const exception & e)
			{
				string str = e.what();
				Assert::Fail(utils::widen(str).c_str());
			}
		}
	};
}
