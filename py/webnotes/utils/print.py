import webnotes

@webnotes.whitelist()
def get(args=None):
	"""Generate html of a print format"""
	if not args:
		args = webnotes.form_dict
	#webnotes.errprint(args)
	
	# check if args has doctype and name
	
		# DocList -- doc and doclist
		
		# template -- jinja2

		# on template apply doclist values

	html = build_html(args, 'page.html')

	return html

def build_html(args, template):
	"""html build using jinja2 templates"""
	import webnotes
	import os
	webnotes_path = os.path.join(os.path.abspath(webnotes.__file__))
	py_path = os.path.dirname(os.path.dirname(webnotes_path))
	path = os.path.join(py_path, 'core', 'templates')
	webnotes.errprint(path)
	#return ''
	from jinja2 import Environment, FileSystemLoader
	jenv = Environment(loader = FileSystemLoader(path))
	html = jenv.get_template(template).render(args)
	return html
