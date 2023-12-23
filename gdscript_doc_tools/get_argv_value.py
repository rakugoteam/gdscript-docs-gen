def get_argv_value(value: str, active_flag: str, args: dict):
	match active_flag:
		case "output":
			args[active_flag] = value

		case "input":
			if value in ("-r", "--recurvise"):
				args["recursive"] = True
				return
			
			args[active_flag].append(value)
		
		case "skip":
			args[active_flag].append(value)