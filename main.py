import os
import sys
import json

from groq import Groq
from dotenv import load_dotenv
from functions.run_functions import run_tool_calls

load_dotenv()
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

with open("functionsSchema.json") as f:
    toolSchema = json.load(f)

# At the moment this array will reset ever time the program run's again. and hence no actual context is stored but during runtime this can be changed so that the array appends the current giving prompt to the messageContextArr.
# Another feat can be added such that to give a fix length to the messageConetextArr and pop the first message when the length increases and append the most recent one to ensure consistency.

messageContextArr = []

if(len(sys.argv)) < 2:
    print("Please enter a prompt")
    sys.exit(1)
else :
    UserPrompt =  str(sys.argv[1])

messageContextArr.append(
    {
    "role" : "user",
    "content" : UserPrompt
    }
)


SystemPrompt = """You are a coding assistant that helps users create, edit, and run code files on their local machine.

When a user asks you to:
- "write a function", "create a function", "make a script" → use write_files_content to create a file
- "run", "execute", "test" something → use run_files
- "show me", "what's in", "read" a file → use get_files_content
- "list", "show files", "what files" → use get_files_info

Always infer intent:
- If the user says "write a function to X", create a Python file implementing that function.
- If no filename is mentioned, use a sensible default.
- Use . as the working directory unless the user specifies otherwise.

Never ask clarifying questions. Always attempt the most reasonable interpretation and act."""


chat_completion = client.chat.completions.create(
    # messages should be assigend to messageContextArr later to store context.
    messages=[ 
        {
            "role": "system",
            "content": SystemPrompt
        },
        {
            "role": "user",
            "content": UserPrompt
        }
    ],
    tools=toolSchema,
    tool_choice="auto",
    model="llama-3.1-8b-instant",
)
message = chat_completion.choices[0].message

if message.tool_calls:
    results = run_tool_calls(message.tool_calls)
    # `run_tool_calls` already prints per-tool results; `results` contains the return values