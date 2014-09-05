from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
from markdown.util import etree, AtomicString
from markdown import markdownFromFile
import bundle.resources

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
		return elem

class Style(Extension):
	def extendMarkdown(self, md, md_globals):
		style = StyleHelper(md, self.config["sheets"][0])
		md.treeprocessors.add('stylesheets', style, "_end")

class MarkdownProcessor:
	def __init__(self, bundle):
		self.__bundle = bundle

	def preprocess(self): pass
		#pull all the resources in
		#base64 encode images, insert data:image URL
		#inject stylesheet files

	def markdown(self, input_path, extensions=None):
		exts = ['abbr','fenced_code','footnotes','tables','codehilite','smarty','toc', 'attr_list','def_list'] if extensions==None else extensions
		style = ",".join(self.__bundle.stylesheets)
		styleext = Style(configs={"sheets":[style, "The stylesheet list"]})
		exts += [styleext]
		markdownFromFile(input_path, input_path + ".html", output_format="html5", extensions=extensions if exts==None else exts)

