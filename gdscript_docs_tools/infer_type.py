from gdscript_docs_tools import *

def infer_type(vars : dict, var_name : str, x : str = "default value"):
	default_value = vars[var_name][x]
	# if value is a "string"
	if default_value.startswith("\"") \
		and default_value.endswith("\""):
		vars[var_name]["type"] = "String"
	
	# if value is a "bool"
	elif default_value == "true" \
		or default_value == "false":
		vars[var_name]["type"] = "bool"
	
	# if value is a "int"
	elif default_value.isdigit():
		vars[var_name]["type"] = "int"
	
	# if value is a "float"
	elif default_value.replace(".", "").isdigit():
		vars[var_name]["type"] = "float"
	
	# if value is a array
	elif default_value.startswith("["):
		vars[var_name]["type"] = "Array"
	
	# if value is a dictionary
	elif default_value.startswith("{"):
		vars[var_name]["type"] = "Dictionary"