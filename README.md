# AI Coding Agent (CLI) in Python

A terminal-based AI coding assistant built from scratch in Python.

The project currently includes:
- A simple CLI chat entry point in [main.py](main.py)
- Secure file-system helper functions for local tool-style operations:
	- [functions/get_files_info.py](functions/get_files_info.py)
	- [functions/get_files_content.py](functions/get_files_content.py)
- A small calculator subproject used for testing and local file operations

## Goals

This project is being developed toward a Claude Code–style terminal agent that can:
- read project files,
- understand user prompts,
- call local helper functions safely,
- and return useful coding assistance directly in the terminal.

## Current Status

### What works now
- CLI prompt input and LLM response generation via Groq in [main.py](main.py)
- Environment variable loading with `python-dotenv`
- Basic file info listing with directory boundary checks in [functions/get_files_info.py](functions/get_files_info.py)
- Basic file reading with working-directory boundary checks and max content cap in [functions/get_files_content.py](functions/get_files_content.py)

### In progress / limitations
- Conversation memory is runtime-only (`messageContextArr` is reset on restart)
- Function-calling/tool orchestration is not yet fully wired into the model loop
- Error handling and truncation messaging can be improved further

## Project Structure

- [main.py](main.py): CLI entrypoint for model interaction
- [functions/get_files_info.py](functions/get_files_info.py): list files/directories with metadata
- [functions/get_files_content.py](functions/get_files_content.py): read file content safely within a working directory
- [test_get_files_info.py](test_get_files_info.py): manual test script for `get_files_info()`
- [test_get_files_content.py](test_get_files_content.py): manual test script for `get_files_content()`
- [calculator/main.py](calculator/main.py): sample calculator CLI app
- [calculator/pkg/calculator.py](calculator/pkg/calculator.py): calculator logic
- [calculator/pkg/render.py](calculator/pkg/render.py): JSON output formatting
- [calculator/test.py](calculator/test.py): unit tests for calculator logic

## Requirements

- Python `>= 3.12`
- Dependencies from [pyproject.toml](pyproject.toml):
	- `groq`
	- `python-dotenv`

## Setup

1. Create and activate a virtual environment.
2. Install dependencies.
3. Create a `.env` file in the project root with:

	 ```
	 GROQ_API_KEY=your_api_key_here
	 ```

## Usage

Run the CLI agent:

```
python main.py "Explain how to refactor my parser"
```

Run helper-function test scripts:

```
python test_get_files_info.py
python test_get_files_content.py
```

Run calculator demo:

```
python calculator/main.py "3 * 4 + 5"
```

Run calculator tests:

```
python calculator/test.py
```

## Security Notes

The file helper functions are designed to restrict access to the configured working directory using path checks. This is important for building safe terminal agents that should not read arbitrary system files.

## Roadmap

- Persist conversation history across runs
- Add robust tool-calling loop (model decides when to call helper functions)
- Add structured command/response schema for tools
- Improve test coverage and convert manual scripts into formal test suites
- Add richer terminal UX (streaming output, better formatting, command history)

## License

Add a license file (e.g., MIT) if you plan to distribute this project publicly.
