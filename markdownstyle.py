from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
from markdown.util import etree, AtomicString
from markdown import Markdown
from markdown.inlinepatterns import Pattern
import bundle.resources
import re

class StyleHelper(Treeprocessor):
	def __init__(self, md, sheets):
		super().__init__(md)
		self.sheets = sheets

	def run(self, root):
		sheets = self.sheets.split(",")
		for sheet in sheets:
			css = bundle.resources.get_style(sheet)
			elem = etree.Element("style")
			elem.text = AtomicString(css)
			root.insert(0,elem)
		return root

class ImagePattern(Pattern):
	def __splitter(self):
		try:
			if self.__split == None:
				self.__split = re.compile('(.+?)="(.+?)"')
		except:
			self.__split = re.compile('(.+?)="(.+?)"')
		return self.__split

	def handleMatch(self, m):
		global __splitattr
		img = etree.Element("img")
		print(m.groups())
		path = m.groups()[1]
		attrs = m.groups()[2]
		data = bundle.resources.datauri(path, bundle.resources.get_resource(path))
		img.set("src", data)
		for attr in self.__splitter().findall(attrs):
			img.set(attr[0], attr[1])
		return img


class MdStyle(Extension):
	def extendMarkdown(self, md, md_globals):
		style = StyleHelper(md, self.config["sheets"][0])
		md.treeprocessors.add('stylesheets', style, "_end")
		images = ImagePattern("\[\$img \"(.+?)\"(.*)\]")
		md.inlinePatterns.add('images', images, "_begin")

class MarkdownProcessor:
	def __init__(self, stylesheets=[]):
		self.__sheets = stylesheets

	def markdown(self, input_path, extensions=None):
		exts = ['abbr','fenced_code','footnotes','tables','codehilite','smarty','toc', 'attr_list','def_list'] if extensions==None else extensions
		style = ",".join(self.__sheets)
		styleext = MdStyle(configs={"sheets":[style, "The stylesheet list"]})
		exts += [styleext]
		md = Markdown(extensions=exts, output_format="html5")
		md.stripTopLevelTags = False
		md.reset().convertFile(input=input_path, output=input_path + ".html")

