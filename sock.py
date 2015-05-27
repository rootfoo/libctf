import socket
import select
import sys
from data import hexdump


class Sock(object):

	"""
	wrapper for a socket that's smart
	functions for pretty printing the dialog
	read_until_string
	read_all (for slow connections)
	"""
	def __init__(self, host, port, family=socket.AF_INET, stype=socket.SOCK_STREAM, timeout=.2, verbose=False):
		self.socket = socket.socket(family, stype)
		self.socket.settimeout(timeout)
		self.socket.connect((host,port))
		self._family = family
		self._stype = stype
		self._host = host
		self._port = port
		self.history = []
		self.verbose = verbose


	def read(self, count=None):
		data = ''
		if count:
			data = self._read(count)
		else:
			data = self._readall()
		if self.verbose:
			print hexdump(data)
		return data


	def recv(self, count=None):
		return self.read(count)


	def _read(self, count=4096):
		data = ''
		try:
			data = self.socket.recv(count)
			self.history.append(('>',data))

		except socket.timeout:
			# timeout doesn't necesarily mean the connection is closed
			pass

		return data

	def _readall(self):
		# read all data from sock
		data = ""
		chunk = ""
		flag = True
		while flag:
			try:
				chunk = self.socket.recv(1024)
			except socket.timeout:
				chunk = ""
			finally:
				if len(chunk) > 0:
					data += chunk
					chunk = ""
				else:
					flag = False

		self.history.append(('>',data))
		return data


	def send(self, data):
		self.write(data)

	def sr(self, data=''):
		"""send(data) && return recv()"""
		if data:
			self.write(data)
		return self.read()


	def write(self, data):
		try:
			self.socket.send(data)
			self.history.append(('<',data))
			
			if self.verbose:
				print hexdump(data)
			return data

		except Exception as e:
			self.socket.close()
			self._closed = True


	def close(self):
		self.socket.close()

	def reconnect(self):
		self.socket.close()
		self.socket = socket.socket(self._family, self._stype)
		self.socket.settimeout(2)
		self.socket.connect((self._host,self._port))


	def interact(self, newline="\n"):

		while True:
			try:
				# It would be nice to have a prompt, but it's tricky to add
				#sys.stdout.write('$> ')
				#sys.stdout.flush()

				# Wait for input from stdin & socket
				input_ready,output_ready,except_ready = select.select([sys.stdin, self.socket], [],[])

				# loop over the file handles with input
				for i in input_ready:
					if i == sys.stdin:
						data = sys.stdin.readline()
						# patch up newlines
						if not data.endswith(newline):
							data = data.strip('\n') + newline

						if data:
							self.history.append(('<', data))
							self.socket.send(data)
					elif i == self.socket:
						data = self.socket.recv(1024)
						if data:
							self.history.append(('>', data))
							sys.stdout.write(data)
							sys.stdout.flush()

			except KeyboardInterrupt:
				break

			except socket.error as msg:
				print msg
				break





