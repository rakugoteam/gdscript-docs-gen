from gdscript_docs_tools import *

def gen_doc_for_signal(found, doc_tree : dict, comments : list):
	#  r"^singal\s+(\w+)\((.*)\)\n"
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
		