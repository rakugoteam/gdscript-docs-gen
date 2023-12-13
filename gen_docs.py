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

			print(entry.path)
			scripts.append(entry.path)

		if entry.is_dir():
			if entry.name in skip:
				continue

			if recursive:
				scandir_for_gdscipts(entry.path, True, skip, scripts)
			
	obj.close()
	return scripts

def gen_docs(scripts : list, output: str, check: bool):
	for script in scripts:
		gen_doc(script, output, check)

def gen_doc(script_path : str, output: str, check :bool):
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
	
	if check:
		return
	
	script_name = os.path.basename(script_path).removesuffix(".gd")
	path = os.path.join(output, script_name + ".md")
	write_to_md(md_tree(doc_tree), path)

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

def md_tree(doc_tree: dict):
	text = {}
	for element in doc_tree:
		match element:
			case "class_name":
				context = doc_tree[element]
				add_arr_if_needed(text, "class_name")
				text["class_name"].append("# %s\n" % context)
			
			case "extends":
				context = doc_tree[element]
				add_arr_if_needed(text, "extends")
				text["extends"].append("\nExtends **%s**\n" % context)
			
			case "main_def":
				if len(doc_tree[element]) == 0:
					continue

				add_arr_if_needed(text, "main")
				for line in doc_tree[element]:
					# convert bbc2md
					text["main"].append("%s\n" % c)
			
			case "consts":
				if len(doc_tree[element]) == 0:
					continue
				
				prepare(text, "consts", "\n## Consts")
				consts = doc_tree[element]

				for con in consts:
					v = consts[con]["value"]
					text["toc"].append(" - [**%s**](#%s) -> %s" % (con, con, v))
					text["consts"].append("### const %s" % con)
					text["consts"].append("*value* : `%s`\n" % v)
					add_comments_to_text(consts[con], text["consts"])

			case "vars":
				if len(doc_tree[element]) == 0:
					continue
				
				prepare(text, "vars", "\n## Vars")
				vars = doc_tree[element]

				for v in vars:
					text["toc"].append(" - [**%s**](#%s)" % (v, v))
					text["vars"].append("### %s" % v)
					if "default value" in vars[v]:
						dv = vars[v]["default value"]
						text["vars"].append("*default value* : `%s`\n" % dv)
					
					add_comments_to_text(vars[v], text["vars"])

			case "singals":
				if len(doc_tree[element]) == 0:
					continue

				prepare(text, "signals", "\n## Signals\n")
				signals = doc_tree[element]

				for s in signals:
					args = ""
					if "args" in signals[s].keys():
						args = signals[s]["args"]
					
					text["toc"].append(" - [**%s**%s](#%s)" % (s, args, s))
					text["signals"].append("### %s%s" % (s, args))
					add_comments_to_text(signals[s], text["signals"])
			
			case "funcs":
				if len(doc_tree[element]) == 0:
					continue
				
				funcs = doc_tree[element]
				prepare(text, "funcs", "\n## Funcs")

				for f in funcs:
					args = ""
					if "args" in funcs[f].keys():
						args = funcs[f]["args"]
					
					text["toc"].append(" - [**%s**%s](#%s)" % (f, args, f))
					text["funcs"].append("### %s%s" % (f, args))
					add_comments_to_text(funcs[f], text["funcs"])
	
	# print_text_tree(text)
	return text

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
		c = len(comments)
		return

	for type in lines_filter.keys():
		gen_doc_for(line, type, doc_tree, comments)

def color_message(color: str, message: str):
	print(f"{color}{message}{bcolors.ENDC}")

def comments_message(type: str, xname: str, comments_len : int):
	message_color = bcolors.OKGREEN
	if comments_len == 0:
		message_color = bcolors.WARNING
	
	color_message(message_color,
		f"Found {comments_len} comments for {type}: {xname}")

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
	
	# print_debug("var:", var_name, vars[var_name])

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
	
	# print_debug("const:", const_name, consts[const_name])

def gen_doc_for_signal(found, doc_tree : dict, comments : list):
	signal_name = found.group(1)
	if signal_name.startswith("_"):
		return
	
	signals = doc_tree["signals"]
	signals[signal_name] = {}

	c = 0
	if len(comments) > 0:
		signals[signal_name]["comments"] = comments.copy()
		c = len(comments)
		comments.clear()
	
	comments_message("signal", signal_name, c)

	if found.group(2):
		signals[signal_name]["args"] = found.group(2)

	# print_debug("signal:", signal_name, signals[signal_name])

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
			gen_doc_for_const(found, doc_tree, comments)

		case "signal":
			gen_doc_for_signal(found, doc_tree, comments)

		case "func":
			gen_doc_for_func(found, doc_tree, comments)
		
		case "comment":
			comment = found.group(1)
			comments.append(comment)

def get_argv(args: dict):
	active_flag = "help"
	args["help"] = True
	args["check only"] = False
	args["recursive"] = False
	args["output"] = ""
	args["input"] = []
	args["skip"] = []

	for arg in sys.argv:
		match arg:
			case "-h" | "--help":
				active_flag = "help"
				args["help"] = True

			case "-o" | "--output":
				active_flag = "output"

			case "-i" | "--input" | "-ir" :
				active_flag = "input"
				args["recursive"] = arg == "-ir"
			
			case "-s" | "--skip" :
				active_flag = "skip"
			
			case "-c" | "--check-only" :
				active_flag = "check"
				args["check"] = True

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

	if args["help"]:
		print(
			"""
			XX version YY
			XX is a simple python tool that generates markdown from gdscript doc comments.

			Example of usage:
				python XX.py -o output -ir gds_source -s plugin.gd
				python XX.py -c -ir gds_source -s plugin.gd

			Flags:
				-h, --help		will display this message
				-i, --input		you give dir sources of gdscript script to scan
				-r, --recursive		scan input recusivly
				-s, --skip		files and dirs to skip from input
				-c, --check-only	will only check and print out how many doc comments you have
			"""
		)
		exit()

	for i in args["input"]:
		scripts = scandir_for_gdscipts(
			i, args["recursive"], args["skip"]
		)
	
	gen_docs(scripts, args["output"], args["check"])