import struct
import string

def pack(*args):
	return _pack(args, '<I')


def pack64(*args):
	return _pack(args, '<Q')


def _pack(packlist, fmt='<I'):
	"""
	Pack a heterogeneous list of strings and integers.
	All integers will be packed according to the struct format.
	Returns all items concatinated as a string.
	
	'<I' : 32-bit little endian
	'<Q' : 64-bit little endian
	"""
	packed = ""
	for x in packlist:
		if type(x) == int:
			packed += struct.pack(fmt, x)
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




