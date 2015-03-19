import struct

def pack(data):
	"""pack 32-bit little-endian"""
	return struct.pack('<I', data)

def unpack(data):
	"""unpack 32-bit little-endian"""
	return struct.unpack('<I', data)

def pack64(data):
	"""pack 64-bit little-endian"""
	return struct.pack('<Q', data)

def unpack64(data):
	"""unpack 64-bit little-endian"""
	return struct.unpack('<Q', data)

def bits(data):
	"""return bit string represntation of data"""
	return [format(ord(c),'08b') for c in data]


def hexdump(data, offsets=True, columns=8, blocksize=4):                                  
	"""get a printable hexdump display of the data"""                                     
	# dynamic format string                                                               
	fprefix = '\n%%0%sx ' % (2*blocksize)                                                 
	# represent data as list of blocks of given size in hex                               
	blocks = [data[i:i+blocksize].encode('hex') for i in xrange(0,len(data),blocksize)]   
	# calculate number of rows given columns                                              
	rows = divisor = (len(blocks) / columns) + 1                                          
	if len(blocks) % columns == 0:                                                        
		rows = rows -1                                                                    
	# insert \n and optional offset prefix before every row                               
	for i in xrange(0, rows):                                                             
		index = i*(columns+1)                                                             
		offset = i*columns*2                                                              
		prefix = "\n"                                                                     
		if offsets:                                                                       
			prefix = fprefix % offset                                                     
		blocks.insert(index, prefix)                                                      
	return " ".join(blocks)                                                               


def partition(data, indecies):                                                            
	"""partitions the data into a list split at every index in indecies"""                
	splitdata = [data[:indecies[0]]]                                                      
	splitdata += [data[indecies[i-1]:indecies[i]] for i in range(1,len(indecies))]        
	splitdata.append(data[indecies[-1]:])                                                 
	return splitdata                                                                      


def splitevery(s, n):                                                                     
	"""splits a string every num chars and return the list"""                             
	return [s[x:x+n] for x in xrange(0,len(s), n)]                                        




