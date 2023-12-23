def prepare(text: dict, space: str, header: str):
	add_arr_if_needed(text, "toc")

	if header not in text["toc"]:
		text["toc"].append(header)
	
	if space not in text.keys():
		text[space] = [header]