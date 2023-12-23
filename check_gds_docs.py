
from gdscript_docs_tools import *

if __name__ == "__main__":
	args = {}
	get_argv(args)
	# print(args)

	if args["help"]:
		print(
			"""
			check_gds_docs.py version 1.0
			It is a simple python tool that checks gdscript doc comments.
			It will show you which const, vars, signals and funcs are missing docs comments.

			Example of usage:
				python check_gds_docs.py -ir gds_source -s plugin.gd

			Flags:
				-h, --help		will display this message
				-i, --input		you give dir sources of gdscript script to scan
				-r, --recursive		scan input recusivly
				-s, --skip		files and dirs to skip from input
			"""
		)
		exit()

	for i in args["input"]:
		scripts = scandir_for_gdscipts(
			i, args["recursive"], args["skip"]
		)
	
	check_gds_docs(scripts)