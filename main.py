import os
import sys

from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

if(len(sys.argv)) < 2:
    print("Please enter a prompt")
    sys.exit(1)
else :
    UserPrompt =  str(sys.argv[1])


chat_completion = client.chat.completions.create(
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