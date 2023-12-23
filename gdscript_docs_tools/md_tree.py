from gdscript_docs_tools import *

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