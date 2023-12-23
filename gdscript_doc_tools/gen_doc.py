from gdscript_doc_tools import *

def gen_doc(script_path : str, output: str):
	doc_tree = check_gdsdoc(script_path)
	script_name = os.path.basename(script_path).removesuffix(".gd")
	path = os.path.join(output, script_name + ".md")
	write_to_md(md_tree(doc_tree), path)