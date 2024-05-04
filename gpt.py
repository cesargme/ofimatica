import openai
from openai import OpenAI
import os

def set_api_key():
    openai_api_key = os.getenv('OPENAI_API_KEY')

    if openai_api_key is None:
        raise Exception("No se encontró la variable de entorno 'OPENAI_API_KEY'. Por favor informa a 👨🏽 César.")

    openai.api_key = openai_api_key

def prompt(msg):

    client = OpenAI()

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": msg,
            }
        ],
        model="gpt-4-turbo",
    )

    return chat_completion.choices[0].message.content

