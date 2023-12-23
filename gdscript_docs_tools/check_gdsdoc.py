from gdscript_docs_tools import *

def check_gdsdoc(script_path : str):
	text = []
	print("\nGenerating docs for %s:" % script_path)
	with open(script_path, "r") as f:
		text = f.readlines()
	
	doc_tree : dict = {}
	doc_tree["vars"] = {}
	doc_tree["consts"] = {}
	doc_tree["singals"] = {}
	doc_tree["funcs"] = {}

	comments : list = []

	for l in text:
		parse_line(l, doc_tree, comments)
	
	return doc_tree