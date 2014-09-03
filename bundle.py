from pyparsing import *
import os.path as pth
from collections import namedtuple
import collections
from markdown import markdownFromFile

Entry = namedtuple("Entry", "description path section")

def loadguard(function):
	def wrapper(*args, **kwargs):
		if not args[0].loaded:
			args[0].load()
		return function(*args, **kwargs)
	return wrapper

class Bundle(collections.Iterable):
	def __init__(self, bundleFile):
		self.bundleFile = bundleFile
		self.__loaded = False
		self.__lines = []
		self.__instance = Entry(None, None, None)
		self.__currentsection = None
		self.__buildgrammar()

	def __buildgrammar(self):
		PATH = CharsNotIn(",\n")("Path")
		DESCRIPTION = Suppress(",") + restOfLine("Description")
		ENTRY = Combine(PATH + Optional(DESCRIPTION))("entry").setParseAction(self.__entry)
		SECTION = Combine(Suppress("#") + restOfLine("Section")).setParseAction(self.__section)
		LINE = SECTION | ENTRY
		BUNDLE = ZeroOrMore(LINE)
		self.BUNDLE = BUNDLE
		self.LINE = LINE
		self.ENTRY = ENTRY
		self.SECTION = SECTION

	
	def __section(self, section):
		self.__currentsection = section.Section

	def __entry(self, x):
		return Entry(x.entry.Description.replace('"', ""), x.entry.Path.replace('"', ""), self.__currentsection)

	def load(self):
		self.__currentsection = None
		parsed = self.BUNDLE.parseFile(self.bundleFile)
		self.__lines = [x for x in parsed if type(x) == type(self.__instance)]
		self.__loaded = True

	@property
	def loaded(self):
		return self.__loaded

	@loadguard
	def __getitem__(self, item):
		return self.__lines[item]

	@loadguard
	def __setitem__(self, item, value):
		self.__lines[item] = value

	@loadguard
	def __iter__(self):
		for i in self.__lines:
			yield i

	@loadguard
	def append(self, item):
		self.__lines += [item]

	@loadguard
	def prepend(self, item):
		self.__lines = [item] + self.__lines

	def __entrystring(self, entry):
		if entry.description:
			return '{0.path},{0.description}'.format(entry)
		else:
			return entry.path

	@loadguard
	def write(self, destination=None):
		if destination == None:
			destination = self.bundleFile
		currentSection = None
		with open(destination, "w") as output:
			for l in self.__lines:
				if currentSection != l.section:
					output.write("#" + l.section + "\n")
					currentSection = l.section
				output.write(self.__entrystring(l) + "\n")

class BundleProcessor:
	def __init__(self, bundle):
		self.__bundle = bundle

	def __get(self, path):
		expath = pth.expanduser(path)
		expath = pth.expandvars(expath)
		try:
			with open(expath) as file:
				for l in file:
					yield l
		except Exception as err:
			print("Failed to open file: {0}".format(err))

	def markdown(self, output_path, exts=None):
		extensions = ['abbr','fenced_code','footnotes','tables','codehilite','smarty','toc', 'attr_list','def_list']
		markdownFromFile(output_path, output_path + ".html", output_format="html5", extensions=extensions if exts==None else exts)

	def merge_to(self, output_path, markdown=False, exts=None):
		lastSection = ""
		try:
			with open(output_path, "w") as output:
				for input in self.__bundle:
					if lastSection != input.section and input.section != "":
						output.write("# {0}\n".format(input.section))
						lastSection = input.section
					if input.description != "":
						output.write("## {0}\n".format(input.description))
					for line in self.__get(input.path):
						output.write(line + "\n")
			if markdown:
				self.markdown(output_path)
		except Exception as err:
			print("Error writing: {0}".format(err))