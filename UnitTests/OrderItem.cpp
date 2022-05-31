#include "pch.h"
#include "CppUnitTest.h"
#include "../WTest_OrderBook/OrderItem.h"

using namespace WG_ORDERBOOK;
using namespace Microsoft::VisualStudio::CppUnitTestFramework;

namespace UnitTests
{
	TEST_CLASS(Test_Order)
	{
	public:

		TEST_METHOD(Test_Order_compare)
		{
			order_comparer less;
			order_item o1(1, 1, 1);
			order_item o2(2, 2, 2);
			order_item o3(3, 3, 2);
			order_item o4(4, 3, 2);

			Assert::IsTrue(less(o1, o2), L"Incorrect compare 1.");
			Assert::IsTrue(less(o2, o3), L"Incorrect compare 2.");
			Assert::IsTrue(less(o3, o4), L"Incorrect compare 3.");
			Assert::IsFalse(less(o4, o4), L"Incorrect compare 4.");
		}
	};
}
