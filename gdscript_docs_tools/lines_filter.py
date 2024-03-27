lines_filter : dict = {
	"extends": r"extends (.*)\n", 
	"class_name": r"class_name (\w+)\n",
	"var": r"^(@export.*\s*)?var (\w+)\s*:?(\s*\w+)?\s*(=\s*.+)?:?\n",
	"const": r"^const (\w+)\s*:?(\s*\w+)?\s*(=\s*.+)\n",
	"signal": r"^signal\s+(\w+)(\((.+)\))?",
	"func": r"^func\s+(\w+)\((.*)\)(\s*->\s*\w+)?\s*:\n",
	"comment": r"^## (.*)"
}