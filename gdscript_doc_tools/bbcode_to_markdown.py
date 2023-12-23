from gdscript_doc_tools import *

def bbcode_to_markdown(bbcode):
	# Define mapping of BBCode to Markdown
	bbcode_to_markdown = {
		"[b]": "**",
		"[/b]": "**",
		"[i]": "*",
		"[/i]": "*",
		"[u]": "__",
		"[/u]": "__",
		"[url]": "[",
		"[/url]": "]",
		"[code]": "`",
		"[/code]": "`",
		"[codeblock]": "```gdscript\n",
		"[/codeblock]": "\n```",
	}

	# Use regular expressions to replace BBCode with Markdown
	for bbcode_tag, markdown_tag in bbcode_to_markdown.items():
		bbcode = re.sub(re.escape(bbcode_tag), markdown_tag, bbcode)

	return bbcode