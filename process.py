from subprocess import Popen, PIPE
import fcntl
import os
import time
import signal

class Process(object):
	"""
	open a process with non-blocking stdin
	unlike commuinicate() will allow interactive communication without
	waiting for the process to exit
	"""

	def __init__(self, exe):
		self.exe = exe
		self.process = Popen(exe, stdout=PIPE, stdin=PIPE, stderr=PIPE)
		self._set_non_blocking(self.process.stdout)	

	def _set_non_blocking(self, handle):
		fd = handle.fileno()
		fl = fcntl.fcntl(fd, fcntl.F_GETFL)
		fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

	def read(self):
		try:
			return self.process.stdout.read()
		except:
			return ""

	def write(self, data):
		self.process.stdin.write(data)


	def run(self, sleep=.5):
		r = self.process.poll()
		time.sleep(sleep)
		if self.process.returncode == -signal.SIGSEGV:
			print "SIGSEGV"
		else:
			print self.process.returncode
		return r

	def attach_gdb(self):
		raw_input("attach gdb now: \n  $ gdb -p {pid}\n  (gdb) attach {pid}\n".format(pid=self.process.pid))


