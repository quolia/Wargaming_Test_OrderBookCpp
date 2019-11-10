import sys
sys.path.append('..')
import unittest
from items import OrderItem


class OrderTestCase(unittest.TestCase):
	def test_Order_compare(self):
		o1 = OrderItem.from_id(1, 1, 1)
		o2 = OrderItem.from_id(2, 2, 2)
		o3 = OrderItem.from_id(3, 3, 2)
		o4 = OrderItem.from_id(4, 3, 2)
		self.assertTrue(o1 < o2, 'Incorrect compare 1.')
		self.assertTrue(o2 < o3, 'Incorrect compare 2.')
		self.assertTrue(o3 < o4, 'Incorrect compare 3.')
		self.assertFalse(o4 < o4, 'Incorrect compare 4.')


if __name__ == '__main__':
	unittest.main()
