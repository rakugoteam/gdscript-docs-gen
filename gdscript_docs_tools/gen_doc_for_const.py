from gdscript_docs_tools import *

def gen_doc_for_const(found, doc_tree : dict, comments : list):
	# r"^const (\w+)\s*:?(\s*\w+)?\s*(=\s*.+)\n"
	# group 1: capture const name
	# group 2: capture const type
	# group 3: capture const value
	const_name = found.group(1)
	if const_name.startswith("_"):
		return

	consts = doc_tree["consts"]
	consts[const_name] = {}
	
	c = 0
	if len(comments) > 0:
		consts[const_name]["comments"] = comments.copy()
		c = len(comments)
		comments.clear()
	
	comments_message("const", const_name, c)

	if found.group(2):
		consts[const_name]["type"] = found.group(2).strip()

	if found.group(3):
		consts[const_name]["value"] = found.group(3).replace("=", "")

		if not "type" in consts[const_name]:
			infer_type(consts, const_name)
