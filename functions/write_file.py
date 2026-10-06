import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
	try:
		working_dir_abs = os.path.abspath(working_directory)
		target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
		valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
		if not valid_target_file:
			return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
		if os.path.isdir(target_file):
			return f'Error: Cannot write to "{file_path}" as it is a directory'
		os.makedirs(os.path.dirname(target_file), exist_ok=True)
		with open(target_file, "w") as f:
			f.write(content)
		return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
	except Exception as e:
		return f'Error:{e}'


schema_write_file = {
	"type": "function",
	"function": {
		"name": "write_file",
		"description": "Verifies the target file is within the working directory and is a valid file, then replaces the content of the file with the provided content argument",
		"parameters": {
			"type": "object",
			"properties": {
				"file_path": {
					"type": "string",
					"description": "Relative path to the target file"
					},
				"content": {
					"type": "string",
					"description": "A string provided to replace the existing content of the target file"
					},
				},
			"required": [
				"file_path",
				"content",
				],
			},
		},
	}
