import openai
import os

openai.my_api_key = "temp" # api key goes here

location = "New York City"
messages = [ {"role": "system", "content":"You are an intelligent assistant."},
            {"role": "user", "content":"List the 5 best things to do in " + location} ]
chat = openai.chat.completions.create(messages=messages, model="gpt-3.5-turbo")
reply = chat.choices[0].message.content
print(reply)
messages.append({"role": "assistant", "content": reply}) 

