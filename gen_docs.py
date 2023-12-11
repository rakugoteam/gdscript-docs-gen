import os, re, sys

lines_filter : dict = {
	"extends": "", 
	"class_name": "",
	"var": r"^(@export.*\s*)?var (\w+)\s*:?=?\s*(.+)\s*:?\n",
	"const": r"^const (\w+)\s*=\s*(.+)\n",
	"signal": r"^singal (\w+)(.*)?\n",
	"func": r"^func (\w+)(.*)?:",
	"comment": r"^## (.*)"
}

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def scandir_for_gdscipts(path : str, recursive = False , skip = [], scripts = []):
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

			if recursive:
				scandir_for_gdscipts(entry.path, True, skip, scripts)

	obj.close()
	return scripts

def gen_docs(scripts : list):
	for script in scripts:
		gen_doc(script)

def gen_doc(script_path : str):
	text = []
	print("\nGenerating docs for %s:" % script_path)
	with open(script_path, 'r') as f:
		text = f.readlines()
	
	doc_tree : dict = {}
	doc_tree["vars"] = {}
	doc_tree["consts"] = {}
	doc_tree["singals"] = {}
	doc_tree["funcs"] = {}

	comments : list = []

	for l in text:
		parse_line(l, doc_tree, comments)
	
	to_md(doc_tree)

def add_arr_if_needed(d:dict, arry_name:str):
	if arry_name not in d.keys():
		d[arry_name] = []

def prepare(text: dict, space: str, header: str):
	add_arr_if_needed(text, "toc")

	if header not in text["toc"]:
		text["toc"].append(header)
	
	if space not in text.keys():
		text[space] = [header]

def add_comments_to_text(part:dict, text_part:dict):
	if "comments" not in part.keys():
		return
	
	for c in part["comments"]:
		text_part.append("%s\n" % c)

def to_md(doc_tree: dict):
	text = {}
	for element in doc_tree:
		match element:
			case "class_name":
				context = doc_tree[element]
				add_arr_if_needed(text, "main")
				text["main"].append("# %s\n" % context)
			
			case "extends":
				context = doc_tree[element]
				add_arr_if_needed(text, "main")
				text["main"].append("Extends **%s**\n" % context)
			
			case "main_def":
				add_arr_if_needed(text, "main")
				for line in doc_tree[element]:
					# convert bbc2md
					text["main"].append("%s\n" % c)
			
			case "consts":
				prepare(text, "consts", "## Consts")
				consts = doc_tree[element]

				for con in consts:
					v = consts[con]["value"]
					text["toc"].append(" - const **%s** -> %s" % (con, v))
					text["consts"].append("### const %s" % con)
					text["consts"].append("*value* : `%s`\n" % v)
					add_comments_to_text(consts[con], text["consts"])

			case "vars":
				prepare(text, "vars", "## Vars")
				vars = doc_tree[element]

				for v in vars:
					text["toc"].append(" - var **%s**" % v)
					text["vars"].append("### var %s" % v)
					if "default value" in vars[v]:
						dv = vars[v]["default value"]
						text["vars"].append("*default value* : `%s`\n" % dv)
					
					add_comments_to_text(vars[v], text["vars"])

			case "singals":
				prepare(text, "signals", "## Signals")
				signals = doc_tree[element]

				for s in signals:
					args = ""
					if "args" in signals[s].keys():
						args = signals[s]["args"]
					
					text["toc"].append(" - signal **%s**(%s) " % (s, args))
					text["signals"].append("### signal %s(%s)" % (s, args))
					add_comments_to_text(signals[s], text["signals"])
			
			case "funcs":
				funcs = doc_tree[element]
				prepare(text, "funcs", "## Funcs")

				for f in funcs:
					args = ""
					if "args" in funcs[f].keys():
						args = funcs[f]["args"]
					
					text["toc"].append(" - func **%s**(%s) " % (f, args))
					text["funcs"].append("### func %s(%s)" % (f, args))
					add_comments_to_text(funcs[f], text["funcs"])
	
	# print_text_tree(text)

def print_text_tree(text:dict): 
	print("\ntext tree:\n")
	for k in text.keys():
		print("%s:\n" % k)
		for kx in text[k]:
			print("%s" % kx)
		
		print("\n")

def parse_line(line : str, doc_tree : dict, comments: list):
	if line.startswith("extends"):
		doc_tree["extends"] = line.split(" ")[1].removesuffix("\n")
		return
		
	if line.startswith("class_name"):
		doc_tree["class_name"] = line.split(" ")[1].removesuffix("\n")
		doc_tree["main_def"] = comments
	
		return

	for type in lines_filter.keys():
		gen_doc_for(line, type, doc_tree, comments)

def zero_comments_waring(type: str, xname: str):
	print(f"{bcolors.WARNING} 0 comments for {type}: {xname}{bcolors.ENDC}")

def gen_doc_for_var(found, doc_tree : dict, comments : list):
	var_name = found.group(2)
	vars = doc_tree["vars"]
	vars[var_name] = {}

	if len(comments) > 0:
		vars[var_name]["comments"] = comments.copy()
		comments.clear()
	
	else:
		zero_comments_waring("var", var_name)

	if found.group(3):
		vars[var_name]["default value"] = found.group(3)
	
	# print_debug("var:", var_name, vars[var_name])

def gen_doc_for_const(found, doc_tree : dict, comments : list):
	const_name = found.group(1)
	consts = doc_tree["consts"]
	consts[const_name] = {}
	
	if len(comments) > 0:
		consts[const_name]["comments"] = comments.copy()
		comments.clear()
	
	else:
		zero_comments_waring("const", const_name)

	if found.group(2):
		consts[const_name]["value"] = found.group(2)
	
	# print_debug("const:", const_name, consts[const_name])

def gen_doc_for_signal(found, doc_tree : dict, comments : list):
	signal_name = found.group(1)
	signals = doc_tree["signals"]
	signals[signal_name] = {}

	if len(comments) > 0:
		signals[signal_name]["comments"] = comments.copy()
		comments.clear()
	
	else:
		zero_comments_waring("signal", signal_name)

	if found.group(2):
		signals[signal_name]["args"] = found.group(2)

	# print_debug("signal:", signal_name, signals[signal_name])

def gen_doc_for_func(found, doc_tree : dict, comments : list):
	func_name = found.group(1)
	funcs = doc_tree["funcs"]
	funcs[func_name] = {}

	if len(comments) > 0:
		funcs[func_name]["comments"] = comments.copy()
		comments.clear()
	
	else:
		zero_comments_waring("func", func_name)

	if found.group(2):
		funcs[func_name]["args"] = found.group(2)

	# print_debug("func:", func_name, funcs[func_name])

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
				args["recursive"] = arg == "-ir"
			
			case "-s" | "--skip" :
				active_flag = "skip"
				args["skip"] = []

			case _:
				get_argv_value(arg, active_flag, args)

def get_argv_value(value: str, active_flag: str, args: dict):
	match active_flag:
		case "output":
			args[active_flag] = value

		case "input":
			if value in ("-r", "--recurvise"):
				args["recursive"] = True
				return
			
			args[active_flag].append(value)
		
		case "skip":
			args[active_flag].append(value)

if __name__ == "__main__":
	args = {}
	get_argv(args)
	# print(args)

	for i in args["input"]:
		scripts = scandir_for_gdscipts(
			i, args["recursive"], args["skip"]
		)
	gen_docs(scripts)