import PySimpleGUI as sg
from psgtray import SystemTray
from pdf2image import convert_from_path
import os
import subprocess
import winreg

# Función para obtener la ruta de la carpeta de descargas desde el Registro de Windows
def get_download_folder():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders') as key:
            return winreg.QueryValueEx(key, "{374DE290-123F-4565-9164-39C4925E467B}")[0]
    except Exception as e:
        return os.path.join(os.path.expanduser('~'), 'Downloads')

# Función para convertir PDF a PNG
def convert_pdf_to_png(pdf_path, tray):
    images = convert_from_path(pdf_path)
    output_folder = os.path.join(get_download_folder(), os.path.splitext(os.path.basename(pdf_path))[0] + '_images')
    os.makedirs(output_folder, exist_ok=True)

    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f'page_{i + 1}.png')
        image.save(image_path, 'PNG')

    tray.show_message('Conversión Completada', f'Los archivos PNG se han guardado en {output_folder}')
    subprocess.Popen(f'explorer {output_folder}')

# Diseño de la interfaz de usuario
layout = [
    [sg.Text('Seleccione un archivo PDF para convertir a PNG')],
    [sg.Input(), sg.FileBrowse(file_types=(("PDF Files", "*.pdf"),))],
    [sg.Button('Convertir'), sg.Button('Salir')]
]

# Crear la ventana
window = sg.Window('Convertidor PDF a PNG', layout, finalize=True)

# Crear el icono en la bandeja del sistema
tray = SystemTray(menu=['', ['Salir']], window=window, tooltip='Convertidor PDF a PNG')

# Event Loop
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Salir':
        break
    if event == 'Convertir':
        pdf_path = values[0]
        if pdf_path:
            convert_pdf_to_png(pdf_path, tray)
        else:
            sg.popup('Error', 'Por favor seleccione un archivo PDF.')

# Cerrar la bandeja del sistema y la ventana
tray.close()
window.close()
