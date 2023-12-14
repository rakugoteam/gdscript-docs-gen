def gen_doc_for_const(found, doc_tree : dict, comments : list):
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
		consts[const_name]["value"] = found.group(2)