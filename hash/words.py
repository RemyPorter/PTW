import linecache
import math
from mmap import mmap
from collections import namedtuple
import os.path
import inspect

__base = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
__file = open(__base + "/" + "all.padded", "r+b")
__mapped = mmap(__file.fileno(),0)

def dehash(hash):
	return FriendlyHash(hash, mappedhash(hash))


def mappedhash(hash, address_size=4, line_size=15, character_size=2):
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

def wordhash(hash, wordlist="all.short", address_size=4):
	words = []
	for i in range(0, len(hash), address_size):
		hx = "00"
		try:
			hx = hash[i:i+address_size]
		except IndexError as err:
			hx = hash[-address_size:0]

		line = int(hx, 16)
		word = linecache.getline(wordlist, line).strip()
		words += [word]

	return " ".join(words)

FriendlyHash = namedtuple("FriendlyHash", "hash friendly")




