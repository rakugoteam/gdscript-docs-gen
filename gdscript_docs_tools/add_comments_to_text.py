from gdscript_docs_tools import *

def add_comments_to_text(part:dict, text_part:dict, args:dict = {}):
	if "comments" not in part:
		return
	
	if args:
		# we can split args by `,``
		args = args.split(",")
		
		for a in args:
			# we make a md points list
			text_part.append(" - %s" % a)

	for c in part["comments"]:
		md = bbcode_to_markdown(c)
		text_part.append(md)