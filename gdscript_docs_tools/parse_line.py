from gdscript_docs_tools import *

def parse_gds_line(line : str, doc_tree : dict, comments: list):
	item_name = ""
	
	if line.startswith("extends"):
		doc_tree["extends"] = item_name
		return
	
	if line.startswith("class_name"):
		# get name of the class
		# from eg. `class_name MyClass` - we get `MyClass`
		item_name = line.split(" ")[1].strip()
		doc_tree["class_name"] = item_name
		doc_tree["main_def"] = comments
		c = len(comments)
		return

	for type in lines_filter.keys():
		gen_doc_for(line, type, doc_tree, comments)