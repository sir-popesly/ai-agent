import os
import subprocess

def run_python_file(
	working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
	try:
		working_dir_abs = os.path.abspath(working_directory)
		target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
		valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
		if not valid_target_file:
			return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
		if not os.path.isfile(target_file):
			return f'Error: "{file_path}" does not exist or is not a regular file'
		if not target_file.endswith(".py"):
			return f'Error: "{file_path}" is not a Python file.'
		command = ["python", target_file]
		if args is not None:
			command.extend(args)
		result = subprocess.run(
			command,
			cwd=working_directory,
			capture_output=True,
			text=True,
			timeout=30
)
		if result.returncode != 0:
			return f'Process exited with code {result.returncode}'
		if result.stdout is None:
			return "No output produced"
		return f'STDOUT: {result.stdout}\nSTDERR: {result.stderr}'

	except Exception as e:
		return f'Error: executing Python file: {e}'

schema_run_python_file = {
	"type": "function",
	"function": {
		"name": "run_python_file",
		"description": "Verifies whether the target file is within the working directory and is a valid Python file, then runs the contents of the file using the provided arguments",
		"parameters": {
			"type": "object",
			"properties": {
				"file_path": {
				"type": "string",
				"description": "Path to the target file, relative to the working directory"
					},
				"args": {
					"type": "list",
					"description": "An optional list of arguments to be used in the execution of the file (or None is no arguments are provided)"
					},
				},
			"required": [
				"file_path",
				],
			},
		},
	}
