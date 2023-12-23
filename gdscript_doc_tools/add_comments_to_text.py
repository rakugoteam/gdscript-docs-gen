from gdscript_doc_tools import *

def add_comments_to_text(part:dict, text_part:dict):
	if "comments" not in part.keys():
		return
	
	for c in part["comments"]:
		md = bbcode_to_markdown(c)
		text_part.append("%s\n" % md)