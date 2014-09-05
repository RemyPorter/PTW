from markdown.treeprocessors import Treeprocessor
from markdown.util import etree
from markdown import markdownFromFile
import resources

class StyleExtension(Treeprocessor):
	def __init__(*args, **kwargs):
		super().__init__(*args, **kwargs)

	def run(self, root):
		sheets = self.config["sheets"][0].split(",")
		for sheet in sheets:
			elem = etree.Element("link")
			elem.set("rel", "stylesheet")
			elem.set("type", "text/css")
			elem.set("href=", sheet)
			root.insert(0,elem)
		return elem

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
		styleext = markdownstyle.StyleExtension(configs={"sheets":[style, "The stylesheet list"]})
		exts += [styleext]
		markdownFromFile(input_path, input_path + ".html", output_format="html5", extensions=extensions if exts==None else exts)

