def gen_doc_for(line : str, type : str, doc_tree : dict, comments : list):
	found = re.search(lines_filter[type], line)
	if not found: return

	match type:
		case "var":
			gen_doc_for_var(found, doc_tree, comments)
		
		case "const":
			gen_doc_for_const(found, doc_tree, comments)

		case "signal":
			gen_doc_for_signal(found, doc_tree, comments)

		case "func":
			gen_doc_for_func(found, doc_tree, comments)
		
		case "comment":
			comment = found.group(1)
			comments.append(comment)