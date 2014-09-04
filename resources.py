import base64
import StringIO
import re

def get(file_path):
	with StringIO.StringIO() as buff:
		with open(file_path, "r") as f:
			base64.encode(f, buff)
		return buff.getvalue()

__url = re.compile("url\(\"(.+)\"\)")
def css_paths(css_text):
	return url.match(css_text).groups()