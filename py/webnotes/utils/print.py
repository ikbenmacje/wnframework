import webnotes

@webnotes.whitelist()
def get(args=None):
	"""Generate html of a print format"""
	if not args:
		args = webnotes.form_dict

	template_str = get_print_format(args.get('fmtname'))
	args = get_data(args)
	
	html = build_html(args, template_str)

	return html

def build_html(args, template_str):
	"""html build using jinja2 templates"""
	import webnotes
	import os

	from jinja2 import Environment
	template = Environment().from_string(template_str)
	html = template.render(args)
	return html

def get_print_format(format_name):
	import webnotes
	res = webnotes.conn.sql("""\
		select html from `tabPrint Format`
		where name=%s and ifnull(is_template, 0)=1""", format_name)
	return res and res[0][0] or ''
	
def get_data(args):
	"""from doclist, get data"""
	if not(args.get('doctype') and args.get('name')):
		return args
		
	import webnotes
	from webnotes.model.doclist import DocList
	dl = DocList(args.get('doctype'), args.get('name'))

	# arrange children as a dict of child types
	children = {}
	for d in dl.children:
		children.setdefault(d.doctype, []).append(d.fields)

	args.update({
		'parent': dl.doc.fields,
		'child': children
	})
	
	return args