from gdscript_docs_tools import *

def gen_doc_for_func(found, doc_tree : dict, comments : list):
	# r"^func\s+(\w+)\((.*)\)(\s*->\s*\w+)?\s*:\n",
	func_name = found.group(1)
	if func_name.startswith("_"):
		return
	
	funcs = doc_tree["funcs"]
	funcs[func_name] = {}

	c = 0
	if len(comments) > 0:
		funcs[func_name]["comments"] = comments.copy()
		c = len(comments)
		comments.clear()
	
	comments_message("func", func_name, c)

	if found.group(2):
		funcs[func_name]["args"] = found.group(2)
	
	if found.group(3):
		funcs[func_name]["returns"] = found.group(3)