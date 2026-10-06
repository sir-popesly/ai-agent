import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
	try:
		working_dir_abs = os.path.abspath(working_directory)
		target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
		valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
		if valid_target_dir is False:
			return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
		if not os.path.isdir(target_dir):
			return f'Error: {directory} is not a directory'
		target_dir_contents = os.listdir(target_dir)
		contents_string = ""
		for file in target_dir_contents:
			entry_path = os.path.join(target_dir, file)
			name = file
			size = os.path.getsize(entry_path)
			is_dir = os.path.isdir(entry_path)
			contents_string += f"-{name}: file_size={size}, is_dir={is_dir}\n"
		return contents_string
	except Exception as e:
		return f"Error: {e}"

schema_get_files_info = {
	"type": "function",
	"function": {
		"name": "get_files_info",
		"description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
		"parameters": {
			"type": "object",
			"propertes": {
				"directory": {
					"type": "string",
					"description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
				},
			},
		},
	},
}
