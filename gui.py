import os
import sys
import PySimpleGUI as sg
from psgtray import SystemTray
import acciones
import logging
import updater
import gpt
import tempfile
from pathlib import Path

temp_dir = tempfile.gettempdir()  # Retorna el directorio temporal

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

# Variable global para la bandeja del sistema
tray = None

def verificar_actualizacion():
    latest_version = updater.get_latest_version()
    curr_version = updater.get_current_version()
    return latest_version != curr_version

def iniciar_actualizacion():
    updater.update_program(updater.get_latest_version())
    pass

def run_application():
    global tray

    menu = ['', ['Corregir ortografía', '⚙️ Abrir registro de errores', 'Salir']]
    tooltip = 'Aplicación de corrección ortográfica'

    layout = [[sg.Text('Corrección ortográfica')]]

    window = sg.Window('Corrección ortográfica', layout, finalize=True, enable_close_attempted_event=True)
    window.hide()

    tray = SystemTray(menu, single_click_events=False, window=window, tooltip=tooltip, icon='icono.ico')
    
    gpt.set_api_key()  # Llama a set_api_key()

    # Verificar actualizaciones
    if verificar_actualizacion():
        respuesta = sg.popup_yes_no('Hay una nueva actualización disponible. ¿Deseas actualizar el programa?', title='Actualización disponible')
        if respuesta == 'Yes': 
            iniciar_actualizacion()
            # Reiniciar el programa
            os.execv(sys.executable, ['python'] + sys.argv)

    while True:
        event, values = window.read(timeout=100)

        # Si es un evento de la bandeja del sistema, cambia el evento a lo que la bandeja envió
        if event == tray.key:
            event = values[0]

        if event in (sg.WIN_CLOSED, 'Salir'):
            break

        # Verifica la existencia del archivo de señalización
        signal_file = Path(temp_dir) / "corregir_ortografia.txt"

        if signal_file.exists() or event == "Corregir ortografía":
            try:
                sg.one_line_progress_meter('Corrección ortográfica', 20, 100, '↻ Procesando texto...', key="-PROG-",orientation='h')
                acciones.corregir_ortografia()
                sg.one_line_progress_meter_cancel(key="-PROG-")
                if signal_file.exists():
                    signal_file.unlink()
                tray.show_message('Corrección ortográfica', '😁👍 ¡Texto corregido con éxito!\n\nPuedes 📄 pegarlo.')
            except Exception as e:  # Atrapar excepciones generales
                tray.show_message('Corrección ortográfica', '❌ Ocurrió un error, reportar a 👨🏽 César:\n\n {}'.format(e))
                logging.exception("Ocurrió un error al corregir la ortografía")
            finally:
                sg.one_line_progress_meter_cancel(key="-PROG-")

        elif event == sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED:
            window.un_hide()
            window.bring_to_front()
        elif event == sg.WIN_CLOSE_ATTEMPTED_EVENT:
            window.hide()
            tray.show_icon()

        elif event == '⚙️ Abrir registro de errores':
            os.startfile('app.log')

    tray.close()
    window.close()

def main():
    try:
        run_application()
    except Exception as e:
        if tray is not None:
            tray.show_message("⚙️ Configuración necesaria", str(e))
        else:
            sg.popup_error("Error", str(e) + " Por favor, cierra el programa.")
        exit(1)

if __name__ == '__main__':
    main()

#TODO Reiniciar si es que hay una excepcion ( o poner en inicio app mia 
