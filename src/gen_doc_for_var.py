def gen_doc_for_var(found, doc_tree : dict, comments : list):
	var_name = found.group(2)
	if var_name.startswith("_"):
		return
	
	vars = doc_tree["vars"]
	vars[var_name] = {}

	c = 0
	if len(comments) > 0:
		vars[var_name]["comments"] = comments.copy()
		c = len(comments)
		comments.clear()
	
	comments_message("var", var_name, c)

	if found.group(3):
		vars[var_name]["default value"] = found.group(3)