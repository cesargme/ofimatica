import openai
from openai import OpenAI
import os
import base64

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


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def prompt_with_image(msg, base64_image):
    client = OpenAI()

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": msg},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/jpg;base64,{base64_image}"}
                }]
                
            }
        ],
        model="gpt-4o",
    )

    return chat_completion.choices[0].message.content


#TODO
# crear accion pa mi
# TODO optimizar costos con el uso de assistant, threads y files
