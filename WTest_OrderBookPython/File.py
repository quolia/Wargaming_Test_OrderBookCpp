
import OrderItem

	#/// <summary> Simple wrapper for a file of orders. </summary>
	class orders_file:

		ifstream _stream; #/// <summary> Stream to read. </summary>

	#public:

		#/// <summary> Dtor. </summary>
		def ~orders_file()
			close()

		#/// <summary> Close file if opened. </summary>
		def close():
			if (is_opened()):
				_stream.close()

		#/// <summary> Opens file for read. </summary>
		#/// <param name="file_name"> File name to open. </param>
		def open_for_read(file_name):

			close()

			_stream.open(file_name)
			if (!is_opened()):
				throw exception("Cannot open file.")

		#/// <summary> Reads and validates orders records. </summary>
		#/// <param name="record"> Reference to a record to write data in. </param>
		#/// <returns> Returns false if end of file reached, true otherwise. </returns>
		def read_order_record(order_record& record):

			if (!is_opened()):
				throw exception("File is not opened.")

			return _stream.eof() ? false : !!(_stream >> record)

		#/// <summary> Checks if file is opened. </summary>
		#/// <returns> Returns true if the file is in opened state. </returns>
		def is_opened():
			return _stream.is_open()