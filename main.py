import os
import sys
from functions.get_files_info import get_files_info

from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

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

chat_completion = client.chat.completions.create(
    # messages should be assigend to messageContextArr later to store context.
    messages=[ 
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": UserPrompt,
        }
    ],
    model="llama-3.1-8b-instant",
)

print(chat_completion.choices[0].message.content)
print(messageContextArr)