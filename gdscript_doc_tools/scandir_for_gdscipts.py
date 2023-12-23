from gdscript_doc_tools import *

def scandir_for_gdscipts(path : str, recursive = False , skip = [], scripts = []):
	obj = os.scandir(path)
	print("\nScaning \"% s\" for gdscripts:" % path)
	for entry in obj :
		if entry.is_file() and entry.name.endswith(".gd"):
			if entry.name in skip:
				continue

			print(entry.path)
			scripts.append(entry.path)

		if entry.is_dir():
			if entry.name in skip:
				continue

			if recursive:
				scandir_for_gdscipts(entry.path, True, skip, scripts)
			
	obj.close()
	return scripts