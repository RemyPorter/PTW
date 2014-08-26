"""
A module to create a friendly representation of an underlying hash object. Uses all.padded as its source data.

all.padded is a UTF-16 encoded file with one string every bytes.

>>> dehash("21046fd2f17ac0f30c88190393568045256866f2")
FriendlyHash(hash='21046fd2f17ac0f30c88190393568045256866f2', friendly='cassareep irascibly upbrought scorched atheized bourtrees oloroso manful chobdar hornbook')
"""
import inspect
from mmap import mmap
from collections import namedtuple
import os.path

__base = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
__file = open(__base + "/" + "all.padded", "r+b")
__mapped = mmap(__file.fileno(),0)

def dehash(hash):
	"""Given a string containing hexadecimal digits, returns a FriendlyHash tuple containing the original string and a "friendly" version
	from mappedhash. Depends on the contents of all.padded.

	>>> dehash("3bc491b57f3a4d1a91da3daae16dfa0052aff75f")
	FriendlyHash(hash='3bc491b57f3a4d1a91da3daae16dfa0052aff75f', friendly='disbowel obi magnetises famous oblivious divulgence thickened welders foiningly votresses')
	"""
	return FriendlyHash(hash, mappedhash(hash))


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
		address = line_size * character_size * line-line_size*character_size
		word = mapped[address:address+line_size*character_size]
		words += [word.decode("UTF" + str(character_size*8)).strip()]
	return " ".join(words)

FriendlyHash = namedtuple("FriendlyHash", "hash friendly")

if __name__ == "__main__":
    import doctest
    doctest.testmod()


