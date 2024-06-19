
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
import os

def convertir_mkv_a_mp3(ruta_mkv, ruta_mp3_temp):
    # Convertir el archivo .mkv a .mp3
    video = VideoFileClip(ruta_mkv)
    audio = video.audio
    audio.write_audiofile(ruta_mp3_temp)
    video.close()  # Cerrar el VideoFileClip
    return ruta_mp3_temp

def dividir_audio_en_chunks(ruta_mp3, duracion_minutos, carpeta_salida):
    # Usar el archivo .mp3 temporal con pydub
    meeting_audio = AudioSegment.from_mp3(ruta_mp3)

    # PyDub maneja el tiempo en milisegundos
    duracion_ms = duracion_minutos * 60 * 1000

    # Crear la carpeta de salida si no existe
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    # Dividir el audio en fragmentos
    for i in range(0, len(meeting_audio), duracion_ms):
        chunk = meeting_audio[i:i + duracion_ms]
        chunk_name = os.path.join(carpeta_salida, f"chunk_{i // duracion_ms + 1}.mp3")
        chunk.export(chunk_name, format="mp3")

    # Limpiar el archivo temporal
    os.remove(ruta_mp3)
