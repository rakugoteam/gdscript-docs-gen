lines_filter : dict = {
	"extends": "", 
	"class_name": "",
	"var": r"^(@export.*\s*)?var (\w+)\s*:?=?\s*(.+)\s*:?\n",
	"const": r"^const (\w+)\s*=\s*(.+)\n",
	"signal": r"^singal (\w+)(.*)?\n",
	"func": r"^func (\w+)(.*)?:",
	"comment": r"^## (.*)"
}