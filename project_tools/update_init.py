import os
import ast

def extract_functions(file_content):
	tree = ast.parse(file_content)
	functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
	return functions

def update_init_file(directory):
	init_file_path = os.path.join(directory, "__init__.py")

	# Collect existing imports from __init__.py
	existing_imports = set()
	if os.path.exists(init_file_path):
		with open(init_file_path, 'r') as init_file:
			for line in init_file:
				if line.startswith("from .") or line.startswith("import "):
					existing_imports.add(line.strip())

	# Scan script files in the directory
	script_files = [f for f in os.listdir(directory) if f.endswith(".py") and f != "__init__.py"]

	# Update __init__.py with proper imports
	with open(init_file_path, 'a') as init_file:
		for script_file in script_files:
			script_path = os.path.join(directory, script_file)
			with open(script_path, 'r') as script:
				functions = extract_functions(script.read())
				for function in functions:
					import_statement = f"from .{os.path.splitext(script_file)[0]} import {function}\n"
					if import_statement not in existing_imports:
						init_file.write(import_statement)
						existing_imports.add(import_statement)

if __name__ == "__main__":
	directory_path = "src"  # Change this to the directory containing your script files
	update_init_file(directory_path)
