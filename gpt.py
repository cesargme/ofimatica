import openai

import os

# Leer la variable de entorno
openai_api_key = os.environ.get('OPENAI_API_KEY')

openai.api_key = openai_api_key

# list models
models = openai.Model.list()

# print the first model's id
print(models.data[0].id)

def prompt(msg):
    # create a chat completion
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": msg}])

    # print the chat completion
    return chat_completion.choices[0].message.content
