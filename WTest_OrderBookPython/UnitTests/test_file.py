import sys
import unittest
from file import OrdersFile
from items import OrderRecord

sys.path.append('..')


class FileTestCase(unittest.TestCase):
	def test_File_file_not_exists(self):
		file = OrdersFile()
		with self.assertRaises(Exception):
			file.open_for_read('not_exists.txt')

	def test_File_file_not_opened(self):
		file = OrdersFile()
		try:
			file.open_for_read('not_exists.txt')
		except FileNotFoundError:
			self.assertFalse(file.is_opened(), 'File is opened.')

	def test_File_file_read_from_not_opened(self):
		file = OrdersFile()
		record = OrderRecord()
		with self.assertRaises(Exception):
			file.read_order_record(record)

	def test_File_file_open_and_close(self):
		file = OrdersFile()
		file.open_for_read('TestOrders/valid10.5.txt')
		file.close()
		self.assertFalse(file.is_opened(), 'File is still opened.')

	def test_File_file_read_from_invalid(self):
		file = OrdersFile()
		file.open_for_read('TestOrders/invalid.txt')
		record = OrderRecord()
		with self.assertRaises(Exception):
			file.read_order_record(record)

	def test_File_file_read_from_empty(self):
		file = OrdersFile()
		file.open_for_read('TestOrders/empty.txt')
		record = OrderRecord()
		self.assertFalse(file.read_order_record(record), 'Read from empty.')


if __name__ == '__main__':
	unittest.main()
