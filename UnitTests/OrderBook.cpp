#include "pch.h"
#include "CppUnitTest.h"
#include "../WTest_OrderBook/OrderBook.h"
using namespace WG_ORDERBOOK;

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

namespace UnitTests
{
	TEST_CLASS(Test_OrderBook)
	{
	public:

		TEST_METHOD(Test_OrderBook_add)
		{
			order_item order;
			order_book book;
			Assert::IsTrue(book.size() == 0, L"Order book is not empty.");
		}

		TEST_METHOD(Test_OrderBook_add_remove)
		{
			order_item order(1, 1, 1);
			order_book book;
			book.add(order);
			Assert::IsTrue(book.size() == 1, L"Order book is empty.");
			book.remove(order.id(), 1);
			Assert::IsTrue(book.size() == 0, L"Order book is not empty.");
		}

		TEST_METHOD(Test_OrderBook_remove_from_empty)
		{
			try
			{
				order_book book;
				book.remove(1, 1);
				Assert::Fail(L"Exception missing.");
			}
			catch (const exception & e)
			{
				//
			}
		}

		TEST_METHOD(Test_OrderBook_remove_invalid_order)
		{
			try
			{
				order_item order(1, 1, 1);
				order_book book;
				book.add(order);
				book.remove(2, 1);
				Assert::Fail(L"Exception missing.");
			}
			catch (const exception & e)
			{
				//
			}
		}

		TEST_METHOD(Test_OrderBook_max_price_in_empty)
		{
			order_book book;
			Assert::IsTrue(book.max_price_order().price() == 0, L"Max price is not 0.");
		}

		TEST_METHOD(Test_OrderBook_add_same_order)
		{
			try
			{
				order_item order(1, 1, 1);
				order_book book;
				book.add(order);
				book.add(order);
				Assert::Fail(L"Exception missing.");
			}
			catch (const exception & e)
			{
				//
			}
		}

		TEST_METHOD(Test_OrderBook_max_price)
		{
			order_item order1(1, 1, 1);
			order_item order2(2, 2, 10);
			order_item order3(3, 3, 10);
			order_item order4(4, 4, 5);
			order_item order5(5, 5, 15);

			order_book book;
			book.add(order1);
			Assert::IsTrue(book.max_price_order().id() == 1, L"Max price order is not correct.");
			book.add(order2);
			Assert::IsTrue(book.max_price_order().id() == 2, L"Max price order is not correct.");
			book.add(order3);
			Assert::IsTrue(book.max_price_order().id() == 3, L"Max price order is not correct.");
			book.add(order4);
			Assert::IsTrue(book.max_price_order().id() == 3, L"Max price order is not correct.");
			book.add(order5);
			Assert::IsTrue(book.max_price_order().id() == 5, L"Max price order is not correct.");
		}
	};
}
