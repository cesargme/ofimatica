import pyperclip
import gpt
from datetime import date

def corregir_ortografia():
    # Captura el texto seleccionado
    # keyboard.send('ctrl+c')  # Copia el texto seleccionado al portapapeles
    # time.sleep(0.1)  # Espera un momento para que el texto se copie correctamente
    texto = pyperclip.paste()  # Pega el texto copiado

    # Utiliza la API de GPT para corregir el texto
    texto_corregido = gpt.prompt(f"corrige este texto con buena ortografía: {texto}")

    # Reemplaza el texto seleccionado con el texto corregido
    pyperclip.copy(texto_corregido)
    # keyboard.send('ctrl+v')  # Pega el texto corregido

    # Imprime el texto corregido en la consola para depuración
    print(texto_corregido)


def notas_reunion():
        # Captura el texto seleccionado
    texto = pyperclip.paste()  # Pega el texto copiado

    # Utiliza la API de GPT para corregir el texto
    texto_corregido = gpt.prompt(f"""Transformar el siguiente texto en un formato ordenado y estructurado para una reunión en OneNote. Utilizar markdown, bulletpoints, casillas y otros elementos para organizar las ideas, preguntas y notas de manera clara y concisa.
Texto proporcionado: {texto}
Por favor, organizar de la siguiente manera:
	• Ideas principales en bulletpoints.
	• Preguntas en una lista numerada.
Notas adicionales en casillas.""")

    # Reemplaza el texto seleccionado con el texto corregido
    pyperclip.copy(texto_corregido)

    # Imprime el texto corregido en la consola para depuración
    print(texto_corregido)

def cie10():
    texto = pyperclip.paste()  # Pega el texto copiado

    # Utiliza la API de GPT para corregir el texto
    texto_corregido = gpt.prompt(f"""Dada la siguiente lista de diagnósticos, por favor devuelve únicamente los códigos CIE-10 correspondientes:
{texto}""")

    # Reemplaza el texto seleccionado con el texto corregido
    pyperclip.copy(texto_corregido)

    # Imprime el texto corregido en la consola para depuración
    print(texto_corregido)

def pacpart_extraer_fechas_horas():
    texto = pyperclip.paste()  # Pega el texto copiado

    # Utiliza la API de GPT para corregir el texto
    texto_corregido = gpt.prompt(f"""Dado el siguiente texto, por favor extrae todas las fechas y horas. Si encuentras palabras como "hoy", asume que se refieren a la fecha actual ({date.today()}) y preséntalas en el siguiente formato
Fecha: [Fecha en formato DD-MM-AAAA]
Inicia: [Hora de inicio en formato HH:MM am/pm]
Finaliza: [Hora de finalización en formato HH:MM am/pm]

{texto}""")

    # Reemplaza el texto seleccionado con el texto corregido
    pyperclip.copy(texto_corregido)

    # Imprime el texto corregido en la consola para depuración
    print(texto_corregido)