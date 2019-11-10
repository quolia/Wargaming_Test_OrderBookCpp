import sys
sys.path.append('..')
import unittest
import random
from accumulator import Accumulator
from items import OrderItem
from orderbook import OrderBookFactory


def rand():
	return random.randrange(1, 65000)


class AccumulatorTestCase(unittest.TestCase):
	def test_Accumulator_not_init_add(self):
		acc = Accumulator()
		order = OrderItem()
		with self.assertRaises(Exception):
			acc.add_order(order)

	def test_Accumulator_not_init_remove(self):
		acc = Accumulator()
		order = OrderItem()
		with self.assertRaises(Exception):
			acc.remove_order(1, 1)

	def test_Accumulator_init(self):
		acc = Accumulator()
		order_book = OrderBookFactory.get()
		acc.init(order_book)
		order = OrderItem()
		acc.add_order(order)

	def test_Accumulator_remove_from_empty(self):
		acc = Accumulator()
		order_book = OrderBookFactory.get()
		acc.init(order_book)
		with self.assertRaises(Exception):
			acc.remove_order(1, 1)

	def test_Accumulator_remove_invalid_order(self):
		acc = Accumulator()
		order_book = OrderBookFactory.get()
		acc.init(order_book)
		order = OrderItem.from_id(1, 1, 1)
		acc.add_order(order)
		with self.assertRaises(Exception):
			acc.remove_order(2, 1)

	def test_Accumulator_default_average(self):
		acc = Accumulator()
		order_book = OrderBookFactory.get()
		acc.init(order_book)
		self.assertTrue(acc.average_highest_price() == 0)

	def test_Accumulator_result(self):
		acc = Accumulator()
		order_book = OrderBookFactory.get()
		acc.init(order_book)
		order = OrderItem.from_id(1, 1000, 10)
		acc.add_order(order)
		acc.remove_order(order.id(), 2000)
		self.assertTrue(acc.average_highest_price() == 10)

	def test_Accumulator_result2(self):
		acc = Accumulator()
		order_book = OrderBookFactory.get()
		acc.init(order_book)

		o1 = OrderItem.from_id(1, 1000, 10)
		acc.add_order(o1)

		o2 = OrderItem.from_id(2, 2000, 20)
		acc.add_order(o2)

		acc.remove_order(o2.id(), 3000)
		acc.remove_order(o1.id(), 4000)

		self.assertTrue(acc.average_highest_price() == 40000 / 3000)

	def test_Accumulator_result3(self):
		acc = Accumulator()
		order_book = OrderBookFactory.get()
		acc.init(order_book)

		o1 = OrderItem.from_id(1, 1000, 20)
		o2 = OrderItem.from_id(2, 2000, 10)

		acc.add_order(o1)
		acc.add_order(o2)

		acc.remove_order(o2.id(), 3000)
		acc.remove_order(o1.id(), 4000)

		self.assertTrue(acc.average_highest_price() == 60000 / 3000)

	def test_Accumulator_result4(self):
		acc = Accumulator()
		order_book = OrderBookFactory.get()
		acc.init(order_book)

		o1 = OrderItem.from_id(1, 1000, 10)
		o2 = OrderItem.from_id(2, 2000, 20)

		acc.add_order(o1)
		acc.add_order(o2)

		acc.remove_order(o1.id(), 3000)
		acc.remove_order(o2.id(), 4000)

		self.assertTrue(acc.average_highest_price() == 50000 / 3000)

	def test_Accumulator_result5(self):
		acc = Accumulator()
		order_book = OrderBookFactory.get()
		acc.init(order_book)

		o1 = OrderItem.from_id(1, 1000, 20)
		o2 = OrderItem.from_id(2, 2000, 10)

		acc.add_order(o1)
		acc.add_order(o2)

		acc.remove_order(o1.id(), 3000)
		acc.remove_order(o2.id(), 4000)

		self.assertTrue(acc.average_highest_price() == 50000 / 3000)

	def test_Accumulator_add_n_orders(self):
		acc = Accumulator()
		order_book = OrderBookFactory.get()
		acc.init(order_book)

		for i in range(10):
			order = OrderItem.from_id(i+1, 1000*i, 10)
			acc.add_order(order)

		for i in range(10):
			acc.remove_order(i+1, 10000 + 1000*i)

		self.assertTrue(acc.average_highest_price() == 10)

	def test_Accumulator_add_n_orders2(self):
		acc = Accumulator()
		order_book = OrderBookFactory.get()
		acc.init(order_book)

		for i in range(10):
			order = OrderItem.from_id(i+1, 1000*i, 10)
			acc.add_order(order)

		for i in range(10):
			acc.remove_order(i+1, 10000)

		self.assertTrue(acc.average_highest_price() == 10)

	def test_Accumulator_add_n_orders3(self):
		acc = Accumulator()
		order_book = OrderBookFactory.get()
		acc.init(order_book)

		o1 = OrderItem.from_id(1, 1000, 10)
		o2 = OrderItem.from_id(2, 1000, 20)

		acc.add_order(o1)
		acc.add_order(o2)

		acc.remove_order(o1.id(), 2000)
		acc.remove_order(o2.id(), 2000)

		self.assertTrue(acc.average_highest_price() == 20)

	def test_Accumulator_result_gap(self):
		acc = Accumulator()
		order_book = OrderBookFactory.get()
		acc.init(order_book)

		o1 = OrderItem.from_id(1, 1000, 20)
		acc.add_order(o1)
		acc.remove_order(o1.id(), 2000)

		# 1000 msec gap.
		# "There may be periods when there are no orders (in this case, such periods should not be considered)."

		o2 = OrderItem.from_id(2, 3000, 10)
		acc.add_order(o2)
		acc.remove_order(o2.id(), 4000)

		self.assertTrue(acc.average_highest_price() == 30000 / 2000)

	def test_Accumulator_result_gap2(self):
		acc = Accumulator()
		order_book = OrderBookFactory.get()
		acc.init(order_book)

		o1 = OrderItem.from_id(1, 1000, 20)
		acc.add_order(o1)
		acc.remove_order(o1.id(), 2000)

		# 1000 msec gap.
		# "There may be periods when there are no orders (in this case, such periods should not be considered)."

		o2 = OrderItem.from_id(2, 3000, 10)
		acc.add_order(o2)
		acc.remove_order(o2.id(), 4000)

		# 1000 msec gap.

		o3 = OrderItem.from_id(2, 5000, 10)
		acc.add_order(o3)
		acc.remove_order(o3.id(), 6000)

		self.assertTrue(acc.average_highest_price() == 40000 / 3000)

	def test_Accumulator_load_test(self):
		acc = Accumulator()
		order_book = OrderBookFactory.get()
		acc.init(order_book)

		count = 100000
		time = 0

		for i in range(count):
			time += rand() % 5000
			order = OrderItem.from_id(i+1, time, rand() / 100)
			acc.add_order(order)

		for i in range(count):
			time += rand() % 5000
			acc.remove_order(i+1, time)


if __name__ == '__main__':
	unittest.main()
