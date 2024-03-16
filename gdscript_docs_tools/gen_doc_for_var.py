from gdscript_docs_tools import *

def gen_doc_for_var(found, doc_tree : dict, comments : list):
	# r"(@export.*\s*)?var (\w+)\s*:?(\s*\w+)?\s*(=\s*.+)?:?"
	# group 2: capture var name
	# group 3: capture var type
	# group 4: capture var default value
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
		# we need to remove spaces from the type
		vars[var_name]["type"] = found.group(3).strip()
		
	if found.group(4):
		# we need to remove `=` from the default value
		default_value = found.group(4).replace("=", "").strip()

		if default_value.startswith("[") \
			or default_value.startswith("{") \
			or default_value.startswith("("):
			if default_value not in ("[]", "{}") \
				or not default_value.endswith(")"):
				# we don't support multi-line default value yet
				color_message(bcolors.WARNING,
					"We don't support multi-line default values yet: %s" % var_name)

		vars[var_name]["default value"] = default_value

		if not "type" in vars[var_name]:
			vars[var_name]["type"] = "Variant"
			# we check if `:=` is used, if so,
			# we can use the default value to infer the type
			if ":=" in found.string.strip():
				infer_type(vars, var_name)
			
		else:
			# we can't infer the type if the type so we print a warning
			color_message(bcolors.WARNING, "Can't infer type for var %s" % var_name)

