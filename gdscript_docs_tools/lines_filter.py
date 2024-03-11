lines_filter : dict = {
	"extends": r"extends (.*)\n", 
	"class_name": r"class_name (\w+)\n",
	"var": r"^(@export.*\s*)?var (\w+)\s*:?=?\s*(.+)\s*:?\n",
	"const": r"^const (\w+)\s*=\s*(.+)\n",
	"signal": r"^singal (\w+)(.*)?\n",
	"func": r"^func (\w+)(.*)?:",
	"comment": r"^## (.*)"
}