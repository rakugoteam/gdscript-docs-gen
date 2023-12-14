def gen_doc(script_path : str, output: str, check :bool):
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
	
	if check:
		return
	
	script_name = os.path.basename(script_path).removesuffix(".gd")
	path = os.path.join(output, script_name + ".md")
	write_to_md(md_tree(doc_tree), path)