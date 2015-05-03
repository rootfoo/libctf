import ctypes
import pkgutil
import json

JSON_FILE = 'shellcode.json'


def execute_shellcode(payload):
	"""
	Python equivelent of runasm. 
	Loads shellcode into executable memory page and calls it.
	Useful for testing shellcode.
	Will segfault after execution.
	"""
	memory = ctypes.create_string_buffer(payload, len(payload))
	shellcode = ctypes.cast(memory, ctypes.CFUNCTYPE(ctypes.c_void_p))
	shellcode()


class Shellcode(object):

	def __init__(self, fname=JSON_FILE):
		# try to load json data from installation directory
		if __package__:
			data = pkgutil.get_data(__package__, JSON_FILE)
			self.json = json.loads(data)
		
		# load json data from file
		else:
			with open(fname) as fh:
				self.json = json.load(fh)

	def pprint(self):
		for sc in self.json:
			print "{id}: {plat} - {quick}".format(id=sc['id'], plat=sc['platform'], quick=sc['quick'])

	def get(self, id):
		return self.json[id]['shellcode'].decode('base64')

	def execute(self, name):
		exec_shellcode(self.get(name))






