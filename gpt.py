import openai
import os

def set_api_key():
    openai_api_key = os.getenv('OPENAI_API_KEY')

    if openai_api_key is None:
        raise Exception("No se encontró la variable de entorno 'OPENAI_API_KEY'. Por favor informa a 👨🏽 César.")

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
