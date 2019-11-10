import sys
import unittest
from app import Application

sys.path.append('..')


class AppTestCase(unittest.TestCase):

	def test_App_invalid_init(self):
		app = Application()
		with self.assertRaises(Exception):
			app.init(['path'])

	def test_App_invalid_args(self):
		app = Application()
		with self.assertRaises(Exception):
			app.init(None)

	def test_App_file_not_exists(self):
		app = Application()
		with self.assertRaises(Exception):
			app.init(['path', 'test.txt'])

	def test_App_file_not_inited(self):
		app = Application()
		with self.assertRaises(Exception):
			app.run()

	def test_App_file_not_inited2(self):
		app = Application()
		with self.assertRaises(Exception):
			app.average_highest_price()

	def test_App_App_valid_file(self):
		app = Application()
		app.init(['path', 'TestOrders/valid10.5.txt'])
		app.run()
		self.assertTrue(app.average_highest_price() == 10.5, 'Incorrect result.')


if __name__ == '__main__':
	unittest.main()
