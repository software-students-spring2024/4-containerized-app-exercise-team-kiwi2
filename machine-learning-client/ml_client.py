import openai

openai.my_api_key = "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"

location = "New York City"
messages = [ {"role": "system", "content":"You are an intelligent assistant."},
            {"role": "user", "content":"List the 5 best things to do in " + location} ]
chat = openai.chat.completions.create(messages=messages, model="gpt-3.5-turbo")
reply = chat.choices[0].message.content
print(reply)
messages.append({"role": "assistant", "content": reply}) 

