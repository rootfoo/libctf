import sys

uppercase = [chr(x) for x in xrange(65, 91)]
lowercase = [chr(x) for x in xrange(97, 123)]
digits = [str(x) for x in xrange(0, 10)]


def pattern_gen(length):
	"""
	Generate a pattern of a given length up to a maximum
	of 20280 - after this the pattern would repeat
	"""
	# Credit: patterm code adapted from Eugene Ching
	# https://github.com/eugeneching/exploit-pattern
	pattern = ''
	for upper in uppercase:
		for lower in lowercase:
			for digit in digits:
				if len(pattern) < length:
					pattern += upper+lower+digit
				else:
					return pattern[:length]



def pattern_search(search_pattern):
	"""
	Search for search_pattern in pattern.  Convert from hex if needed
	Looking for needle in haystack
	"""
	# Credit: patterm code adapted from Eugene Ching
	# https://github.com/eugeneching/exploit-pattern
	needle = search_pattern
	try:
		if needle.startswith('0x'):
			# Strip off '0x', convert to ASCII and reverse
			needle = needle[2:].decode('hex')
			needle = needle[::-1]
	except TypeError as e:
		sys.stderr.write('Unable to convert hex input: {e}\n'.format(e=e))
		sys.exit(1)

	haystack = ''
	for upper in uppercase:
		for lower in lowercase:
			for digit in digits:
				haystack += upper+lower+digit
				found_at = haystack.find(needle)
				if found_at > -1:
					return found_at

	#sys.stderr.write("Couldn't find {p} ({n}) anywhere in the pattern.".format(p=search_pattern, n=needle))
	return -1


