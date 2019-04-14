#!/usr/bin/env python

from distutils.core import setup

setup(name='libctf',
	version='0.2',
	description="lightweight CTF and exploit development framework",
	author='Marcus Hodges',
	author_email='0xmeta@gmail.com',
	url='http://rootfoo.org',
	license="MIT",
    packages=['libctf'], 
	package_data={'libctf': ['data/shellcode.json']},
	scripts=['bin/ctf-payload', 'bin/ctf-run']
	)
