# Introduction

Libctf is a CTF framework written by meta of the Neg9 CTF team. The framework is a collection of tools and python libraries to simplify exploit development and many of the other tasks frequently performed during a CTF.

# Example

	from libctf import *
	shelldb = ShellcodeDB()
	print shelldb.list()
	shellcode = shelldb.get('linux x86 execve 1')
	sock = Sock('localhost',9090)
	payload = 'A'*100 + pack32(0x11223344) + shellcode 
	sock.send(payload)
	sock.interact()

# Installation

To install to your home directory (~/.local/lib/python2.7/site-packages/):

	python setup.py install --user

To install for all users (/usr/local/lib/python2.7/dist-packages/):
	
	sudo python setup.py install




