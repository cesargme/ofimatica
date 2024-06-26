import pyperclip
import util.gpt as gpt
from datetime import date, datetime
from functools import wraps
import re
import time
import keyboard
import FreeSimpleGUI as sg
from pdf2image import convert_from_path
import os
import subprocess
import util.myclipboard_util as myclipboard_util
import util.audio_processing as audio_processing
import util.my_ollama as my_ollama
from pathlib import Path


def seleccionar_archivo_mkv(func):
    def wrapper(*args, **kwargs):
        layout = [
            [sg.Text("Selecciona el archivo .mkv")],
            [sg.Input(), sg.FileBrowse(file_types=(("MKV Files", "*.mkv"),))],
            [sg.OK(), sg.Cancel()]
        ]

        window = sg.Window("Seleccionar Archivo", layout)
        
        event, values = window.read()
        window.close()

        if event == "OK":
            ruta_mkv = values[0]
            if ruta_mkv.endswith('.mkv'):
                return func(ruta_mkv, *args, **kwargs)
            else:
                sg.popup_error("Debe seleccionar un archivo .mkv")
        else:
            sg.popup("Operación cancelada")
    
    return wrapper

def obtener_desde_clipboard(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        texto = pyperclip.paste()  # Pega el texto copiado
        resultado = func(
            texto, *args, **kwargs
        )  # Llama a la función original con el texto del portapapeles
        pyperclip.copy(resultado)  # Copia el resultado al portapapeles
        print(resultado)  # Imprime el resultado para depuración
        return resultado

    return wrapper


@obtener_desde_clipboard
def corregir_ortografia(texto=None):

    # corregir texto
    texto_corregido = gpt.prompt(
        f"Texto original (speech to text): {texto}\ntexto con mejor ortografía y ligeramente arreglado(con extrema prudencia): "
    )
    print(texto_corregido)

    return texto_corregido


def extraer_info_transaccion_financiera(texto=None):
    # Leer el contenido del archivo prompt_transaccion.txt
    with open("prompts/prompt_transaccion.txt", "r") as archivo:
        prompt = archivo.read().strip()

    
    ocrd_image = myclipboard_util.ocr_from_clipboard_image()

    respuesta = my_ollama.prompt(prompt + ocrd_image, serve=True)

    clipboard = myclipboard_util.copy_data_to_excel_clipboard(respuesta)
    print(clipboard)

    return clipboard

@seleccionar_archivo_mkv #TODO, que sea en el mismo explorador, seleccionándolo ahí mismito
def transcribir_reunión(ruta_mkv):
    ruta_mkv_str= ruta_mkv
    ruta_mkv = Path(ruta_mkv)

    audio_processing.convertir_mkv_a_mp3(ruta_mkv_str, "temp_audio.mp3")
    audio_processing.dividir_audio_en_chunks("temp_audio.mp3", duracion_minutos=10, carpeta_salida="reu")
    gpt.transcribir_y_unificar_chunks("reu",ruta_mkv.parent / (ruta_mkv.stem + ".txt") )


def notas_reunion():
    # Captura el texto seleccionado
    texto = pyperclip.paste()  # Pega el texto copiado

    # Utiliza la API de GPT para corregir el texto
    texto_corregido = gpt.prompt(
        f"""Transformar el siguiente texto en un formato ordenado y estructurado para una reunión en OneNote. Utilizar markdown, bulletpoints, casillas y otros elementos para organizar las ideas, preguntas y notas de manera clara y concisa.
Texto proporcionado: {texto}
Por favor, organizar de la siguiente manera:
	• Ideas principales en bulletpoints.
	• Preguntas en una lista numerada.
Notas adicionales en casillas."""
    )

    # Reemplaza el texto seleccionado con el texto corregido
    pyperclip.copy(texto_corregido)

    # Imprime el texto corregido en la consola para depuración
    print(texto_corregido)


def cie10():
    texto = pyperclip.paste()  # Pega el texto copiado

    # Utiliza la API de GPT para corregir el texto
    texto_corregido = gpt.prompt(
        f"""Dada la siguiente lista de diagnósticos, por favor devuelve únicamente los códigos CIE-10 correspondientes:
texto: {texto}
códigos: """
    )

    # Reemplaza el texto seleccionado con el texto corregido
    pyperclip.copy(texto_corregido)

    # Imprime el texto corregido en la consola para depuración
    print(texto_corregido)


def pacpart_extraer_fechas_horas():
    texto = pyperclip.paste()  # Pega el texto copiado

    # Utiliza la API de GPT para corregir el texto
    texto_corregido = gpt.prompt(
        f"""Dado el siguiente texto, por favor extrae todas las fechas y horas. Si encuentras palabras como "hoy", asume que se refieren a la fecha actual ({date.today()}) y preséntalas en el siguiente formato
Fecha: [Fecha en formato DD-MM-AAAA]
Hora de inicio: [Hora de inicio en formato HH:MM am/pm]
Hora de fin: [Hora de finalización en formato HH:MM am/pm]

texto: {texto}
extracción: """
    )

    # Reemplaza el texto seleccionado con el texto corregido
    pyperclip.copy(texto_corregido)

    # Imprime el texto corregido en la consola para depuración
    print(texto_corregido)


@obtener_desde_clipboard
def obtener_y_calcular_edad(msg):
    def calcular_edad(fecha_nacimiento):
        hoy = datetime.now()
        edad = hoy.year - fecha_nacimiento.year

        if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
            edad -= 1

        return edad

    def obtener_fecha_con_gpt(msg):
        prompt = f"Por favor, extrae la fecha de nacimiento del siguiente mensaje y formátela como YYYY-MM-DD: '{msg}'"
        respuesta_gpt = gpt.prompt(
            prompt
        )  # Aquí recibirías el resultado del modelo GPT
        fecha_match = re.search(r"\d{4}-\d{2}-\d{2}", respuesta_gpt)
        if fecha_match:
            return fecha_match.group(0)
        else:
            return None  # O manejar el error de alguna otra manera

    fecha_str = obtener_fecha_con_gpt(msg)
    fecha_nacimiento = datetime.strptime(fecha_str, "%Y-%m-%d")
    edad_actual = calcular_edad(fecha_nacimiento)

    return f"Edad: {edad_actual} Años"


def clipboard_decorator(func, delay):
    def wrapper(*args, **kwargs):
        # Inicialización
        time.sleep(delay)

        paperclip_cache = pyperclip.paste()
        keyboard.send("ctrl+c")
        time.sleep(0.8)

        # Llama a la función decorada
        func(*args, **kwargs)
        time.sleep(0.8)

        # Pega el texto corregido
        keyboard.send("ctrl+v")
        time.sleep(0.8)

        # Restaura el portapapeles original
        pyperclip.copy(paperclip_cache)

    return wrapper


def convertir_pdf_a_png():
    # Crear un diálogo para seleccionar el archivo PDF
    layout = [
        [sg.Text("Seleccione un archivo PDF para convertir a PNG")],
        [sg.Input(), sg.FileBrowse(file_types=(("PDF Files", "*.pdf"),))],
        [sg.Button("Convertir"), sg.Button("Cancelar")],
    ]

    window = sg.Window("Convertidor PDF a PNG", layout)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Cancelar"):
            break

        if event == "Convertir":
            pdf_path = values[0]
            if pdf_path and os.path.exists(pdf_path):
                # Procesar el archivo PDF
                images = convert_from_path(pdf_path)
                output_folder = os.path.join(
                    os.path.dirname(pdf_path),
                    os.path.splitext(os.path.basename(pdf_path))[0] + "_images",
                )
                os.makedirs(output_folder, exist_ok=True)

                for i, image in enumerate(images):
                    image_path = os.path.join(output_folder, f"page_{i + 1}.png")
                    image.save(image_path, "PNG")

                # Abrir la carpeta de salida
                subprocess.Popen(f"explorer {os.path.realpath(output_folder)}")
            break

    window.close()


if __name__ == "__main__":
    import FreeSimpleGUI as sg

    res = corregir_ortografia(
        "me preocupa un poco su capacidad de soporte, como los otros percheros que hemos tenido."
    )
    sg.popup(res)
