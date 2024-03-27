from gdscript_docs_tools import *

def prepare(text: dict, space: str):
	add_arr_if_needed(text, "toc")

	h = space.capitalize()
	header = "- [**%s**](#%s)" % (h, h.lower())
	if header not in text["toc"]:
		text["toc"].append(header)
	
	if space not in text.keys():
		header = "\n## %s" % h
		text[space] = [header]