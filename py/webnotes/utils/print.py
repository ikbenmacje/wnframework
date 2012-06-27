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

	template = get_print_format(args.get('fmtname'))
	args = get_args(args)
	
	html = build_html(args, template)

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
	template = jenv.from_string(template)
	html = template.render(args)
	return html

def get_print_format(format_name):
	import webnotes
	res = webnotes.conn.sql("""\
		select html from `tabPrint Format`
		where name=%s and ifnull(is_template)=1""", format_name)
	return res and res[0][0] or ''
	
def get_args(args):
	if not(args.get('doctype') and args.get('name')):
		return args
	import webnotes
	from webnotes.model.doclist import DocList
	dl = DocList(args.get('doctype'), args.get('name'))
	args.update(dl.fields)
	return args