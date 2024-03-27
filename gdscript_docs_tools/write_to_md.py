from gdscript_docs_tools import *

def write_to_md(mdt:dict, path:str):
	lines = []
	if "class_name" in mdt.keys():
		lines += mdt["class_name"]
	
	else:
		script_name = os.path.basename(path)
		script_name = script_name.removesuffix(".md")
		script_name = snake_case_to_camel_case(script_name)
		lines.append("# %s" % script_name)

	lines += mdt["extends"]

	if "main_def" in mdt.keys():
		lines += mdt["main_def"]
	
	lines += ["## Table of Contents\n"]
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