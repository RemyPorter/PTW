"""
A module to create a friendly representation of an underlying hash object. Uses all.padded as its source data.

all.padded is a UTF-16 encoded file with one string every bytes.

>>> dehash("21046fd2f17ac0f30c88190393568045256866f2")
'cassareep irascibly upbrought scorched atheized bourtrees oloroso manful chobdar hornbook'
"""
import inspect
from mmap import mmap
from collections import namedtuple
import os.path
import gzip
import json

def default():
	return None

__file = None
__mapped = None
__index = None

def __init__():
	global __file, __mapped, __index
	__base = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
	__file = open(__base + "/" + "all.padded", "r+b")
	__mapped = mmap(__file.fileno(),0)
	__index = None
	with gzip.open(__base + "/" + "index", "rb") as f:
		data = f.read()
		__index = json.loads(data.decode("UTF8"))

__init__()

def dehash(hash):
	"""Given a string containing hexadecimal digits, returns a FriendlyHash tuple containing the original string and a "friendly" version
	from mappedhash. Depends on the contents of all.padded.

	>>> dehash("3bc491b57f3a4d1a91da3daae16dfa0052aff75f")
	'disbowel obi magnetises famous oblivious divulgence thickened welders foiningly votresses'
	>>> dehash("bff2cdc22f22b79fee98bfa3205a0b12912fabd0")
	'scatology solen courtier retrofit unmasking scantling carjacks arrestors nunship puffball'
	"""
	return mappedhash(hash)

def get_at_address(line, line_size, character_size):
	address = line_size * character_size * line-line_size*character_size
	word = __mapped[address:address+line_size*character_size]
	return word.decode("UTF16").strip()

def mappedhash(hash, address_size=4, line_size=15, character_size=2):
	"""
	Returns a string that uniquely identifies an input hash. Depends on the contents of all.padded, which is the data file.
	>>> mappedhash("3bc491b57f3a4d1a91da3daae16dfa0052aff75f")
	'disbowel obi magnetises famous oblivious divulgence thickened welders foiningly votresses'
	"""
	global __file, __mapped
	words = []
	f = __file
	mapped = __mapped
	for i in range(0, len(hash), address_size):
		hx = "00"
		try:
			hx = hash[i:i+address_size]
		except IndexError as err:
			hx = hash[-address_size:0]

		line = int(hx, 16)
		word = get_at_address(line, line_size, character_size)
		words += [word]
	return " ".join(words)

def enhash(words, address_size=4):
	"""
	Given a word string, containing only words in all.padded, return the hash that it comes from. This assumes that the supplied 
	wordlist only contains "valid" words, off the all.padded list. It may enter an infinite loop otherwise. (I will fix that, probably)
	>>> enhash('disbowel obi magnetises famous oblivious divulgence thickened welders foiningly votresses')
	'3bc491b57f3a4d1a91da3daae16dfa0052aff75f'
	>>> enhash('scatology solen courtier retrofit unmasking scantling carjacks arrestors nunship puffball')
	'bff2cdc22f22b79fee98bfa3205a0b12912fabd0'
	"""
	l = words.split(" ")
	test = ""
	hsh = ""
	for word in l:
		(bottom,top) = __index[word[:3]]
		mid = (top - bottom) // 2 + bottom

		while True:
			test = get_at_address(mid, 15,2)
			if test == word:
				break
			elif test < word:
				bottom = mid
				mid = (top - bottom) // 2 + bottom
			elif test > word:
				top = mid
				mid = (top - bottom) // 2 + bottom

		hsh += hex(mid)[2:].rjust(address_size, "0")
	return hsh

def get_index():
	return __index


FriendlyHash = namedtuple("FriendlyHash", "hash friendly")

if __name__ == "__main__":
    import doctest
    doctest.testmod()


