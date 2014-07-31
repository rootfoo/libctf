from sock import * 
from data import *
from shellcode import * 

try:
	# Try to import the ipython interactive shell
	from IPython import embed as ipython # drop to interactive shell
except ImportError as e:
	import sys
	sys.stderr.write('Warning: IPython embed could not be imported')

