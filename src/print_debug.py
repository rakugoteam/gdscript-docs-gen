def print_debug(message:str, x_name:str, doc: dict):
	print("\n%s" % message, x_name)
	for k in doc:
		
		if k == "comments":
			print("\t%s:" % k)
			for c in doc[k]:
				print("\t\t%s:" %c)
			
			continue

		print("\t%s:" % k, doc[k])