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
    # create a completion
    completion = openai.Completion.create(
        model="gpt-3.5-turbo-instruct", 
        prompt=msg, 
        max_tokens=512
    )

    # print the completion
    return completion.choices[0].text

