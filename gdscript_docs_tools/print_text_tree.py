def print_text_tree(text:dict): 
	print("\ntext tree:\n")
	for k in text.keys():
		print("%s:\n" % k)
		for kx in text[k]:
			print("%s" % kx)
		
		print("\n")