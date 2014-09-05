import base64
import io
import re
import os.path

def get_style(file_path):
	f = open(file_path, "r")
	css = f.read()
	f.close()
	paths = set(css_paths(css))
	for p in paths:
		res = get_resource(p)
		css.replace(p, datauri(p, res))

def datauri(sourcefilepath, encoded):
	_, ext = os.path.splitext(sourcefilepath)
	return "data:img/{0},{1}".format(ext[1:], encoded)

def get_resource(file_path):
	with open(file_path, "rb") as f:
		data = f.read()
		return base64.urlsafe_b64encode(data)

__url = re.compile("url\(\"(.+)\"\)")
def css_paths(css_text):
	return url.match(css_text).groups()

def replace_inline(css_text, path, data):
	pass