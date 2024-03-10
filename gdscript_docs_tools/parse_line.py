from gdscript_docs_tools import *

def parse_gds_line(line : str, doc_tree : dict, comments: list):
	if line.startswith("extends"):
		doc_tree["extends"] = line.split(" ")[1].removesuffix("\n")
		return
	
	if line.startswith("class_name"):
		doc_tree["class_name"] = line.split(" ")[1].removesuffix("\n")
		doc_tree["main_def"] = comments
		c = len(comments)
		return

	for type in lines_filter.keys():
		gen_doc_for(line, type, doc_tree, comments)