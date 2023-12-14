def gen_doc_for_func(found, doc_tree : dict, comments : list):
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