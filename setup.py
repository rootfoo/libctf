#!/usr/bin/env python

from distutils.core import setup

setup(name='libctf',
	version='0.2',
	description='CTF framework by meta',
	author='Marcus Hodges',
	author_email='0xmeta@gmail.com',
	url='http://rootfoo.org',
	license="http://www.opensource.org/licenses/BSD-3-Clause",
	package_dir={'libctf':''},
	package_data={'libctf': ['shellcode.json']},
	packages=['libctf'],
	scripts=['ctf-payload']
	)

