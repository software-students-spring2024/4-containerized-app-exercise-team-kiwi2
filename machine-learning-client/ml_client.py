"""Module to get AI generated recommendations"""

import os
import openai

openai.my_api_key = os.environ.get("OPENAI_API_KEY")  # api key goes here

LOCATION = "New York City"
messages = [
    {"role": "system", "content": "You are an intelligent assistant."},
    {"role": "user", "content": "List the 5 best things to do in " + LOCATION},
]
chat = openai.chat.completions.create(messages=messages, model="gpt-3.5-turbo")
reply = chat.choices[0].message.content
print(reply)
messages.append({"role": "assistant", "content": reply})
