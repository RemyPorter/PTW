import linecache
import math

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