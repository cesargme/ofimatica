from PIL import ImageGrab, Image
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import pandas as pd
import pyperclip
import json


def get_base64_image_from_clipboard():
    try:
        # Obtener la imagen del portapapeles
        image = ImageGrab.grabclipboard()

        # Verificar si hay una imagen en el portapapeles
        if image is None:
            raise ValueError("No hay imagen en el portapapeles.")

        # Convertir la imagen a bytes
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        image_bytes = buffered.getvalue()

        # Codificar la imagen en base64
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        return image_base64
    except Exception as e:
        return str(e)


def show_image_from_base64(base64_image):
    try:
        # Decodificar la imagen base64
        image_bytes = base64.b64decode(base64_image)
        image = Image.open(BytesIO(image_bytes))

        # Mostrar la imagen usando matplotlib
        plt.imshow(image)
        plt.axis("off")  # Ocultar los ejes
        plt.show()
    except Exception as e:
        print("Error al mostrar la imagen:", e)


def copy_data_to_excel_clipboard(json_str):
    # Parsear la cadena JSON a una lista de diccionarios
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Error al parsear JSON: {e}")
        return

    # Convertir la lista de diccionarios en un DataFrame
    df = pd.DataFrame(data)

    # Convertir el DataFrame a un array de arrays (sin los encabezados)
    array_of_arrays = df.values.tolist()

    # Convertir el array de arrays a una cadena formateada para Excel (CSV)
    df_string = df.to_csv(index=False, header=False, sep="\t")

    # Copiar la cadena al portapapeles
    pyperclip.copy(df_string)

    print("La tabla ha sido copiada al portapapeles en formato adecuado para Excel.")
    print(array_of_arrays)


# Ejemplo de uso
# json_str = """[
#     {"Fecha": "2024-06-01", "Cuánto": 100.50, "Motivo": "Pago servicio", "Tarjeta": "BBVA, soles", "Transferencia": "VERDADERO"},
#     {"Fecha": "2024-06-02", "Cuánto": 50.00, "Motivo": "", "Tarjeta": "Pichincha", "Transferencia": "FALSO"},
#     {"Fecha": "2024-06-03", "Cuánto": 75.75, "Motivo": "para pagar a junta", "Tarjeta": "BN", "Transferencia": "VERDADERO"}
# ]"""

# copy_data_to_excel_clipboard(json_str)