import os
import sys
import json

from groq import Groq
from dotenv import load_dotenv
from functions.run_functions import run_tool_calls
from prompts import controllerPrompt,toolCallerSystemPrompt

load_dotenv()
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

with open("functionsSchema.json") as f:
    toolSchema = json.load(f)

if(len(sys.argv)) < 2:
    print("Please enter a prompt")
    sys.exit(1)
else :
    UserPrompt =  str(sys.argv[1])

# MessageContextArr should store the context of the conversation.
messageContextArr = []
messageContextArr.append(
    {
    "role" : "user",
    "content" : UserPrompt
    }
)

# Step 1: Controller breaks down the user request into steps
controllerChatCompletion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": controllerPrompt
        },
        {
            "role": "user",
            "content": UserPrompt
        }
    ],
    model="llama-3.1-8b-instant",
)
controllerMessage = controllerChatCompletion.choices[0].message
controllerSteps = controllerMessage.content

print("Controller Steps:")
print(controllerSteps)
print("\n" + "="*50 + "\n")

# Step 2: Tool caller takes the steps and makes tool calls
toolCallerChatCompletion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": toolCallerSystemPrompt
        },
        {
            "role": "user",
            "content": f"Execute the following steps:\n{controllerSteps}"
        }
    ],
    tools=toolSchema,
    tool_choice="auto",
    model="llama-3.1-8b-instant",
)

tool_calls = toolCallerChatCompletion.choices[0].message.tool_calls

if tool_calls:
    results = run_tool_calls(tool_calls)
    print("Tool Call Results:")
    
    
    for t in tool_calls : 
        print(t)
        print("\n") 