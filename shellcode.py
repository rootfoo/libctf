#!/usr/bin/python
import json
import ctypes
import pkgutil

JSON_FILE = 'shellcode.json'


def exec_shellcode(payload):
	"""Python equivelent of runasm. Will segfault after execution."""
	memory = ctypes.create_string_buffer(payload, len(payload))
	shellcode = ctypes.cast(memory, ctypes.CFUNCTYPE(ctypes.c_void_p))
	shellcode()


class ShellcodeDB(object):

	def __init__(self, fname=None):
		# load json data from file
		if fname:
			with open(fname) as fh:
				self.json = json.load(fh)
		
		# try to load json data from installation directory
		elif __package__:
			data = pkgutil.get_data(__package__, JSON_FILE)
			self.json = json.loads(data)

	def list(self):
		names = sorted([name for name in self.json])
		return names

	def get(self, name):	
		return self.json[name]['shellcode'].decode('base64')

	def execute(self, name):
		exec_shellcode(self.get(name))




if __name__=='__main__':
	# just print the list
	for x in ShellcodeDB(JSON_FILE).list():
		print x


