def comments_message(type: str, xname: str, comments_len : int):
	message_color = bcolors.OKGREEN
	if comments_len == 0:
		message_color = bcolors.WARNING
	
	color_message(message_color,
		f"Found {comments_len} comments for {type}: {xname}")