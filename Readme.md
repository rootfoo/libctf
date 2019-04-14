# Introduction

Libctf is a CTF framework written by meta of the Neg9 CTF team. The framework is a collection of tools and python libraries to simplify exploit development and many of the other tasks frequently performed during a CTF.

# Example

	from libctf import *
	shelldb = ShellcodeDB()
	print shelldb.list()
	shellcode = shelldb.get('linux x86 execve 1')
	sock = Sock('localhost',9090)
	sock.verbose = True
	payload = pack('A'*100, 0x11223344, shellcode)
	print hexdump(payload)
	sock.recv()
	sock.send(payload)
	sock.interact()


# Install

## From outside the project directory
```
sudo pip install libctf
```

## From the directory containing setup.py
```
sudo pip install .
```

## Verify
```
pip show photorg
```

## Uninstall
```
sudo pip uninstall photorg
```

## Developer install, add project folder to python path
```
sudo pip install -e .
```

## Developer uninstall

Remove path entry from
```
/usr/local/lib/python2.7/dist-packages/easy-install.pth
```
Delete link file
```
rm /usr/local/lib/python2.7/dist-packages/libctf.egg-link
```
