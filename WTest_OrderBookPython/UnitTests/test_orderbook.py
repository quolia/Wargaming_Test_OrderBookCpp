import sys
sys.path.append('..')
import unittest
from items import OrderItem
from orderbook import OrderBookFactory


class OrderBookTestCase(unittest.TestCase):
	def test_OrderBook_add(self):
		order = OrderItem()
		book = OrderBookFactory.get()
		self.assertTrue(book.size() == 0, 'Order book is not empty.')

	def test_OrderBook_add_remove(self):
		order = OrderItem.from_id(1, 1, 1)
		book = OrderBookFactory.get()
		book.add(order)
		self.assertTrue(book.size() == 1, 'Order book is empty.')
		book.remove(order.id())
		self.assertTrue(book.size() == 0, 'Order book is not empty.')

	def test_OrderBook_remove_from_empty(self):
		book = OrderBookFactory.get()
		with self.assertRaises(Exception):
			book.remove(1)

	def test_OrderBook_remove_invalid_order(self):
		order = OrderItem.from_id(1, 1, 1)
		book = OrderBookFactory.get()
		with self.assertRaises(Exception):
			book.remove(2)

	def test_OrderBook_max_price_in_empty(self):
		book = OrderBookFactory.get()
		self.assertTrue(book.max_price_order().price() == 0, 'Max price is not 0.')

	def test_OrderBook_add_same_order(self):
		order = OrderItem.from_id(1, 1, 1)
		book = OrderBookFactory.get()
		book.add(order)
		with self.assertRaises(Exception):
			book.add(order)

	def test_OrderBook_add_same_price_and_time(self):
		o1 = OrderItem.from_id(1, 1, 1)
		o2 = OrderItem.from_id(2, 1, 1)
		book = OrderBookFactory.get()
		book.add(o1)
		book.add(o2)

	def test_OrderBook_max_price(self):
		o1 = OrderItem.from_id(1, 1, 1)
		o2 = OrderItem.from_id(2, 2, 10)
		o3 = OrderItem.from_id(3, 3, 10)
		o4 = OrderItem.from_id(4, 4, 5)
		o5 = OrderItem.from_id(5, 5, 15)
		book = OrderBookFactory.get()
		book.add(o1)
		self.assertTrue(book.max_price_order().id() == 1, 'Max price order is not correct 1.')
		book.add(o2)
		self.assertTrue(book.max_price_order().id() == 2, 'Max price order is not correct 2.')
		book.add(o3)
		self.assertTrue(book.max_price_order().id() == 3, 'Max price order is not correct 3.')
		book.add(o4)
		self.assertTrue(book.max_price_order().id() == 3, 'Max price order is not correct 4.')
		book.add(o5)
		self.assertTrue(book.max_price_order().id() == 5, 'Max price order is not correct 5.')


if __name__ == '__main__':
	unittest.main()
