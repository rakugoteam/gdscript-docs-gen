from gdscript_docs_tools import *

def get_argv(args: dict):
	active_flag = "help"
	args["help"] = False
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

			case _:
				get_argv_value(arg, active_flag, args)