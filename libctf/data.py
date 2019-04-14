import struct
import string


def pack64(num):
	"""struct.pack 64-bit int"""
	return struct.pack('<Q', num) if (num > 0) else struct.pack('<q', num)

def pack32(num):
	"""struct.pack 32-bit int"""
	return struct.pack('<I', num) if (num > 0) else struct.pack('<i', num)

def unpack64(data):
	"""struct.unpack 64-bit unsigned int"""
	return struct.unpack('<Q', data)[0]

def unpack32(data):
	"""struct.unpack 32-bit unsigned int"""
	return struct.unpack('<I', data)[0]


def rop(*args):
	"""Alias for rop64"""
	return rop64(args)


def rop32(*args):
	"""
	Pack a heterogeneous list of strings and integers for ROP payload.
	Negative integers packed as signed values, and positive packed as signed. 
	"""
	packed = ""
	for x in args:
		if type(x) == int or type(x) == long:
			packed += pack32(x)
		else:
			packed += x
	return packed


def rop64(*args):
	"""
	Pack a heterogeneous list of strings and integers for ROP payload.
	Negative integers packed as signed values, and positive packed as signed. 
	"""
	packed = ""
	for x in args:
		if type(x) == int or type(x) == long:
			packed += pack64(x)
		else:
			packed += x
	return packed


def bits(data):
	"""return bit string represntation of data"""
	return [format(ord(c),'08b') for c in data]


def hexdump(data, columns=4, blocksize=4):
	"""get a printable hexdump display of the data"""
	blocks = splitevery(data, blocksize)

	# calculate number of rows given columns
	row_count,remain = divmod(len(blocks), columns)
	if remain > 0:
		row_count += 1

	rows = []
	# row length includes 2 chars for hex and 1 for spaces
	rowlen = columns*(2*blocksize+1) 
	# printable chars, in this context, dont include whitespace
	printable = string.digits + string.letters + string.punctuation 

	for i in range(0, row_count):
		start = i*columns
		ascii_string = ''
		row = ''
		# add the hex
		for block in blocks[start:start+columns]:
			row += block.encode('hex') + ' '
			ascii_string += ''.join([x if x in printable else ' ' for x in block])
		# pad last row with spaces so ascii strings align
		rows.append(row.ljust(rowlen) + ascii_string)

	return '\n'.join(rows)


def partition(data, indecies):
	"""partitions the data into a list split at every index in indecies"""
	splitdata = [data[:indecies[0]]]
	splitdata += [data[indecies[i-1]:indecies[i]] for i in range(1,len(indecies))]
	splitdata.append(data[indecies[-1]:])
	return splitdata


def splitevery(s, n):
	"""splits a string every num chars and return the list"""
	return [s[x:x+n] for x in range(0,len(s), n)]




