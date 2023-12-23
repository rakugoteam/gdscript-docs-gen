import ast
import os

def extract_functions(file_content):
	# Parse the Python script
	tree = ast.parse(file_content)

	functions = []
	for node in ast.walk(tree):
		if isinstance(node, ast.FunctionDef):
			functions.append(node)

	return functions

def split_script_by_functions(script_path):
	with open(script_path, 'r') as file:
		script_content = file.read()

	functions = extract_functions(script_content)

	for function in functions:
		# Extract function name
		function_name = function.name

		# Extract function code
		function_code = ast.get_source_segment(script_content, function)

		# Create a new file for each function
		new_file_path = f"src/{function_name}.py"
		with open(new_file_path, 'w') as new_file:
			new_file.write(function_code)

		print(f"Function '{function_name}' extracted to '{new_file_path}'")

if __name__ == "__main__":
	# Specify the path to the Python script you want to split
	script_path = "gen_docs_src.py"

	# Check if the script exists
	if os.path.exists(script_path):
		split_script_by_functions(script_path)
	else:
		print(f"Error: The specified script '{script_path}' does not exist.")
