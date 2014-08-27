from pygit2 import *
import collections
import enum
from hashed.words import dehash, enhash
class NoRepoError(Exception) : pass

StatusEntry = collections.namedtuple("StatusEntry", "file statuses")

def statusforcode(code):
	statuses = []
	if code & GIT_STATUS_INDEX_NEW > 0 or code & GIT_STATUS_WT_NEW > 0:
		statuses += ["new"]
	if code & GIT_STATUS_INDEX_MODIFIED > 0 or code & GIT_STATUS_WT_MODIFIED > 0:
		statuses += ["modified"]
	if code & GIT_STATUS_INDEX_DELETED > 0 or code & GIT_STATUS_WT_DELETED > 0:
		statuses += ["deleted"]
	if code & GIT_STATUS_IGNORED > 0:
		statuses += ["ignored"]
	if len(statuses) == 0:
		statuses += ["current"]
	return statuses

class Repo:
	def __init__(self, directory, force=False):
		path = ""
		self.git = None
		try:
			path = discover_repository(directory)
			self.git = Repository(path) 
			self.__master = self.git
		except KeyError as err:
			print(err)
			if force:
				self.git = init_repository(directory)
			else:
				raise NoRepoError("{0} does not contain a repository.".format(directory))

	def status(self):
		return [StatusEntry(x[0], statusforcode(x[1])) for x in self.git.status().items()]

	def log_entries(self):
		last = self.git[self.git.head.target]
		for commit in self.git.walk(last.id, GIT_SORT_TIME):
			yield (dehash(str(commit.id)), commit)

	def get_object_by_words(self, sentence):
		hashed = enhash(sentence)
		return self.git.get(hashed)

	def __get_item__(self, index):
		return self.get_object_by_words(index)

	
