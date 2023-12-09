import os, re, sys

lines_filter : dict = {
	"extends": "", 
	"class_name": "",
	"var": r"^(@export.*\s*)?var (\w+)\s*:?=?\s*(.+)\s*:?",
	"const": r"^const (\w+)\s*=\s*(.+)",
	"signal": r"^singal (\w+)(.*)?",
	"func": r"^func (\w+)(.*)?:",
	"comment": r"^## (.*)"
}

def scandir_for_gdscipts(path : str, skip = [], scripts = []):
	obj = os.scandir(path)
	print("\nScaning '% s' for gdscripts:" % path)
	for entry in obj :
		if entry.is_file() and entry.name.endswith(".gd"):
			if entry.name in skip:
				continue

			scripts.append(entry.path)
		
		if entry.is_file():
			print(entry.path)
		
		if entry.is_dir():
			if entry.path in skip:
				continue

			scandir_for_gdscipts(entry.path, skip, scripts)

	obj.close()
	return scripts

def gen_docs(scripts : list):
	for script in scripts:
		gen_doc(script)

def gen_doc(script_path : str):
	lines = []
	print("\nGenerating docs for %s:" % script_path)
	with open(script_path, 'r') as f:
		lines = f.readlines()
	
	doc_tree : dict = {}
	doc_tree["vars"] = {}
	doc_tree["consts"] = {}
	doc_tree["singals"] = {}
	doc_tree["funcs"] = {}

	comments : list = []

	for l in lines:
		parse_line(l, doc_tree, comments)
	
	# print(doc_tree)

def parse_line(line : str, doc_tree : dict, comments: list):
	if line.startswith("extends"):
		doc_tree["extends"] = line.split(" ")[1]
		return
		
	if line.startswith("class_name"):
		doc_tree["class_name"] = line.split(" ")[1]
		doc_tree["main_def"] = comments
	
		return

	for type in lines_filter.keys():
		gen_doc_for(line, type, doc_tree, comments)

def gen_doc_for_var(found, doc_tree : dict, comments : list):
	var_name = found.group(2)
	vars = doc_tree["vars"]
	vars[var_name] = {}

	if len(comments) > 0:
		vars[var_name]["comments"] = comments.copy()
		comments.clear()

	if found.group(3):
		vars[var_name]["default value"] = found.group(3)
	
	print_debug("var:", var_name, vars[var_name])

def gen_doc_for_const(found, doc_tree : dict, comments : list):
	const_name = found.group(1)
	consts = doc_tree["consts"]
	consts[const_name] = {}
	
	if len(comments) > 0:
		consts[const_name]["comments"] = comments.copy()
		comments.clear()

	if found.group(2):
		consts[const_name]["value"] = found.group(2)
	
	print_debug("const:", const_name, consts[const_name])

def gen_doc_for_signal(found, doc_tree : dict, comments : list):
	signal_name = found.group(1)
	signals = doc_tree["signals"]
	signals[signal_name] = {}

	if len(comments) > 0:
		signals[signal_name]["comments"] = comments.copy()
		comments.clear()

	if found.group(2):
		signals[signal_name]["args"] = found.group(2)

	print_debug("signal:", signal_name, signals[signal_name])

def gen_doc_for_func(found, doc_tree : dict, comments : list):
	func_name = found.group(1)
	funcs = doc_tree["funcs"]
	funcs[func_name] = {}

	if len(comments) > 0:
		funcs[func_name]["comments"] = comments.copy()
		comments.clear()

	if found.group(2):
		funcs[func_name]["args"] = found.group(2)

	print_debug("func:", func_name, funcs[func_name])

def print_debug(message:str, x_name:str, doc: dict):
	print("\n%s" % message, x_name)
	for k in doc:
		
		if k == "comments":
			print("\t%s:" % k)
			for c in doc[k]:
				print("\t\t%s:" %c)
			
			continue

		print("\t%s:" % k, doc[k])

def gen_doc_for(line : str, type : str, doc_tree : dict, comments : list):
	found = re.search(lines_filter[type], line)
	if not found: return

	match type:
		case "var":
			gen_doc_for_var(found, doc_tree, comments)
		
		case "const":
			gen_doc_for_const(found,  doc_tree, comments)

		case "signal":
			gen_doc_for_signal(found, doc_tree, comments)

		case "func":
			gen_doc_for_func(found, doc_tree, comments)
		
		case "comment":
			comment = found.group(1)
			comments.append(comment)

def get_argv(args: dict):
	active_flag = "-h"
	
	for arg in sys.argv:
		match arg:
			case "-o" | "--output":
				active_flag = "output"
				args["output"] = ""

			case "-i" | "--input" | "-ir":
				active_flag = "input"
				args["input"] = []
				args["input_r"] = arg == "-ir"
			
			case "-s" | "--skip" | "-sr":
				active_flag = "skip"
				args["skip"] = []
				args["skip_r"] = arg == "-sr"
	
			case _:
				get_argv_value(arg, active_flag, args)

def get_argv_value(value: str, active_flag: str, args: dict):
	match active_flag:
		case "output":
			args[active_flag] = value

		case "skip" | "input":
			if value in ("-r", "--recurvise"):
				switch_to_r(active_flag, value, args)
				return

			args[active_flag].append(value)

def switch_to_r(active_flag: str, value: str, args: dict):
		match active_flag:
			case "input":
				args["input_r"] = True
			
			case "skip":
				args["skip_r"] = True

if __name__ == "__main__":
	args = {}
	get_argv(args)
	print(args)
	scripts = scandir_for_gdscipts("gd_src/", ["plugin.gd"])
	gen_docs(scripts)