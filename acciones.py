import pyperclip
import gpt

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