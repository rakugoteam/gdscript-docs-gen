def add_arr_if_needed(d:dict, arry_name:str):
	if arry_name not in d.keys():
		d[arry_name] = []