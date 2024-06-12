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


def get_transcription(audio_file):
    client = OpenAI()

    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    return transcription.text

def transcribir_y_unificar_chunks(carpeta_chunks, archivo_unificado):
    transcripciones = []

    # Iterar sobre los archivos de audio en la carpeta
    for archivo in sorted(os.listdir(carpeta_chunks)):
        if archivo.endswith(".mp3"):
            ruta_audio = os.path.join(carpeta_chunks, archivo)
            with open(ruta_audio, "rb") as audio_file:
                transcripcion = get_transcription(audio_file)
                # Guardar la transcripción en un archivo .txt separado
                archivo_txt = ruta_audio.replace(".mp3", ".txt")
                with open(archivo_txt, "w") as f:
                    f.write(transcripcion)
                transcripciones.append(transcripcion)

    # Unificar todas las transcripciones en un único archivo .txt
    with open(archivo_unificado, "w") as archivo_final:
        for transcripcion in transcripciones:
            archivo_final.write(transcripcion + "\n")