import linecache
import math
from mmap import mmap

def mappedhash(hash, wordlist="all.padded", address_size=4, line_size=15, character_size=2):
	words = []
	f = open(wordlist, "r+b")
	mapped = mmap(f.fileno(), 0)
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
		
class FriendlyHash(str):
	def __new__(cls, value, worder=wordhash):
		instance = super().__new__(cls, value)
		instance.__friendly = False
		instance.__text = ""
		return instance

	@property
	def friendly(self):
		if not self.__friendly:
			self.__text = wordhash(self)
			self.__friendly = True
		return self.__text