def write_to_md(mdt:dict, path:str):
	lines = []
	if "class_name" in mdt.keys():
		lines += mdt["class_name"]
	
	else:
		lines.append("# " + os.path.basename(path).removesuffix(".md"))

	lines += mdt["extends"]

	if "main" in mdt.keys():
		lines += mdt["main"]
	
	lines += mdt["toc"]

	if "const" in mdt.keys():
		lines += mdt["consts"]
	
	if "vars" in mdt.keys():
		lines += mdt["vars"]
	
	if "signals" in mdt.keys():
		lines += mdt["signals"]
	
	if "funcs" in mdt.keys():
		lines += mdt["funcs"]

	file = open(path, "w")
	for l in lines:
		file.write(l + "\n")

	file.close()
	color_message(bcolors.OKBLUE, f"Written to file: {path}")