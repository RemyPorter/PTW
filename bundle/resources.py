import base64
import io
import re
import os.path

def __fixpath(path):
	return os.path.expandvars(os.path.expanduser(path))

def get_style(file_path):
	f = open(__fixpath(file_path), "r")
	css = f.read()
	f.close()
	return replace_inline(css)

def datauri(sourcefilepath, encoded):
	_, ext = os.path.splitext(sourcefilepath)
	return "data:image/{0};base64,{1}".format(ext[1:], encoded)

def get_resource(file_path):
	try:
		with open(__fixpath(file_path), "rb") as f:
			data = f.read()
			return base64.b64encode(data).decode("utf8")
	except Exception as error:
		return ""

__url = re.compile(".*url\([\"'](.+)[\"']\).*")
def css_paths(css_text):
	return __url.findall(css_text)

def replace_inline(css_text):
	paths = css_paths(css_text)
	newtext = css_text
	for p in paths:
		uri = datauri(p, get_resource(p))
		newtext = newtext.replace(p, uri)
	return newtext