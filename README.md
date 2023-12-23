# gdscript-docs-tools
Library and Simple Python scripts for Markdown and GDScript docs.

## Tools
- [check_gds_docs](#check-gdscript-docs)
- [gds_docs2md](#gdscript-docs-2-md)

### Check GDScript Docs
It is a simple python tool that checks gdscript doc comments.
It will show you which const, vars, signals and funcs are missing docs comments.

#### Example of usage
`python check_gds_docs -ir gds_source -s plugin.gd`

#### Flags
```
-h, --help		will display this message
-i, --input		you give dir sources of gdscript script to scan
-r, --recursive		scan input recursively
-s, --skip		files and dirs to skip from input
```

### GDScript Docs 2 MD
It is a simple python tool that generates markdown from gdscript doc comments.

#### Example of usage
`gds_docs2md -o output -ir gds_source -s plugin.gd`

#### Flags
```
-h, --help		will display this message
-i, --input		you give dir sources of gdscript script to scan
-r, --recursive		scan input recursively
-s, --skip		files and dirs to skip from input
```