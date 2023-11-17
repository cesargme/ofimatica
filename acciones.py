import pyperclip
import gpt
from datetime import date, datetime
from functools import wraps
import re

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

def obtener_desde_clipboard(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        texto = pyperclip.paste()  # Pega el texto copiado
        resultado = func(texto, *args, **kwargs)  # Llama a la función original con el texto del portapapeles
        pyperclip.copy(resultado)  # Copia el resultado al portapapeles
        print(resultado)  # Imprime el resultado para depuración
        return resultado
    return wrapper


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
        respuesta_gpt = gpt.prompt(prompt)  # Aquí recibirías el resultado del modelo GPT
        fecha_match = re.search(r'\d{4}-\d{2}-\d{2}', respuesta_gpt)
        if fecha_match:
            return fecha_match.group(0)
        else:
            return None  # O manejar el error de alguna otra manera

    fecha_str = obtener_fecha_con_gpt(msg)
    fecha_nacimiento = datetime.strptime(fecha_str, '%Y-%m-%d')
    edad_actual = calcular_edad(fecha_nacimiento)
    
    return f"Edad: {edad_actual} Años"
