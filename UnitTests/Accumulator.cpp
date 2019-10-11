#include "pch.h"
#include "CppUnitTest.h"
#include "../WTest_OrderBook/Accumulator.h"
using namespace WG_ORDERBOOK;

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

namespace UnitTests
{
	TEST_CLASS(Test_Accumulator)
	{
	public:

		TEST_METHOD(Test_Accumulator_not_init_add)
		{
			try
			{
				accumulator acc;
				order_item order;
				acc.add_order(order);

				Assert::Fail(L"Exception missing.");
			}
			catch (const exception & e)
			{
				//
			}
		}

		TEST_METHOD(Test_Accumulator_not_init_remove)
		{
			try
			{
				accumulator acc;
				order_item order;
				acc.remove_order(1, 1);

				Assert::Fail(L"Exception missing.");
			}
			catch (const exception & e)
			{
				//
			}
		}

		TEST_METHOD(Test_Accumulator_init)
		{
			accumulator acc;			
			{
				shared_ptr<order_book_iface> ptr(new order_book());
				acc.init(ptr);
			}
			order_item order;
			acc.add_order(order);
		}

		TEST_METHOD(Test_Accumulator_remove_from_empty)
		{
			accumulator acc;
			{
				shared_ptr<order_book_iface> ptr(new order_book());
				acc.init(ptr);
			}

			try
			{
				acc.remove_order(1, 1);
				Assert::Fail(L"Exception missing.");
			}
			catch (const exception & e)
			{
				//
			}
		}

		TEST_METHOD(Test_Accumulator_remove_invalid_order)
		{
			accumulator acc;
			{
				shared_ptr<order_book_iface> ptr(new order_book());
				acc.init(ptr);
			}

			try
			{
				order_item order(1, 1, 1);
				acc.add_order(order);
				acc.remove_order(2, 1);
				Assert::Fail(L"Exception missing.");
			}
			catch (const exception & e)
			{
				//
			}
		}

		TEST_METHOD(Test_Accumulator_default_average)
		{
			accumulator acc;
			{
				shared_ptr<order_book_iface> ptr(new order_book());
				acc.init(ptr);
			}

			Assert::IsTrue(acc.average_highest_price() == 0);
		}
	};
}
