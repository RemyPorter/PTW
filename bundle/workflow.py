from . import bundle
from . import markdownstyle

def process(bun, destination="output", extensions=None):
	bp = bundle.BundleProcessor(bun)
	md = markdownstyle.MarkdownProcessor(bun.stylesheets)
	output = open(destination, "w") if isinstance(destination, str) else destination
	bp.merge_to(output)
	output.close()
	md.markdown(output.name, extensions)