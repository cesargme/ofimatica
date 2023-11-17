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
    return updater.check_git_diff()

def iniciar_actualizacion():
    updater.update_program(updater.get_latest_version())
    pass

def ejecutar_accion(accion_func, signal_file_name, process_title, progress_message, success_message, error_message):

    # Check if the signal file exists
    curr_signal_file = Path(signal_file_name)
    
    try:
        # Display progress meter
        sg.one_line_progress_meter(process_title, 20, 100, progress_message, key="-PROG-", orientation='h')
        
        # Perform the provided action
        accion_func()
        
        # Close progress meter
        sg.one_line_progress_meter_cancel(key="-PROG-")
        
        # Unlink the signal file if it exists
        if curr_signal_file.exists():
            curr_signal_file.unlink()
        
        # Display success message
        tray.show_message(process_title, success_message)
    except Exception as e:  # Catch general exceptions
        tray.show_message(process_title, error_message.format(e))
        logging.exception("Error during action execution")
    finally:
        sg.one_line_progress_meter_cancel(key="-PROG-")

# Note: The function still references some global entities like `tray`, which should be available in the environment where the function is run.


def run_application():
    global tray

    menu = ['', ['Corregir ortografía', 'Notas de Reunion',"CIE-10", "PacPart: Extraer Fechas y Horas", "Calcular Edad", '⚙️ Abrir registro de errores', 'Salir']]
    tooltip = 'Aplicación de corrección ortográfica'

    layout = [[sg.Text('Ofimatica')]]

    window = sg.Window('Ofimatica', layout, finalize=True, enable_close_attempted_event=True)
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
        signal_files = {
            "corregir_ortografia": Path(temp_dir) / "corregir_ortografia.txt",
            "notas_de_reunion": Path(temp_dir) / "notas_de_reunion.txt",
            "cie10" : Path(temp_dir) / "cie10.txt",
            "pac_part_extraer_fechas_horas" : Path(temp_dir) / "pac_part_extraer_fechas_horas.txt",
            "calcular_edad" : Path(temp_dir) / "calcular_edad.txt",
        }

        curr_signal_file = signal_files['corregir_ortografia']
        if curr_signal_file.exists() or event == "Corregir ortografía":
            ejecutar_accion(
                accion_func=acciones.corregir_ortografia,
                signal_file_name=curr_signal_file,
                process_title="Corrección ortográfica",
                progress_message="↻ Procesando texto...",
                success_message="😁👍 ¡Texto corregido con éxito!\n\nPuedes 📄 pegarlo.",
                error_message="❌ Ocurrió un error, reportar a 👨🏽 César:\n\n {}"
            )

        curr_signal_file = signal_files['notas_de_reunion']
        if curr_signal_file.exists() or event == "Notas de Reunion":
            ejecutar_accion(
                accion_func=acciones.notas_reunion,
                signal_file_name=curr_signal_file,
                process_title="📄 Notas de Reunion",
                progress_message="↻ Procesando texto...",
                success_message="😁👍 ¡Se han hecho las notas de reunion con éxito!\n\nPuedes 📄 pegarlo.",
                error_message="❌ Ocurrió un error, reportar a 👨🏽 César:\n\n {}"
            )

        curr_signal_file = signal_files['cie10']
        if curr_signal_file.exists() or event == "CIE-10":
            ejecutar_accion(
                accion_func=acciones.cie10,
                signal_file_name=curr_signal_file,
                process_title="Obteniendo códigos CIE-10",
                progress_message="↻ Procesando diagnósticos...",
                success_message="😁👍 ¡Códigos CIE-10 obtenidos con éxito!\n\nPuedes 📄 pegarlos.",
                error_message="❌ Ocurrió un error, reportar a 👨🏽 César:\n\n {}"
            )

        curr_signal_file = signal_files['pac_part_extraer_fechas_horas']
        if curr_signal_file.exists() or event == "PacPart: Extraer Fechas y Horas":
            ejecutar_accion(
                accion_func=acciones.pacpart_extraer_fechas_horas,
                signal_file_name=curr_signal_file,
                process_title="Extrayendo fechas y horas",
                progress_message="↻ Procesando texto para encontrar fechas y horas...",
                success_message="😁👍 ¡Fechas y horas extraídas con éxito!\n\nPuedes 📄 pegarlas en el formato deseado.",
                error_message="❌ Ocurrió un error, reportar a 👨🏽 César:\n\n {}"
            )

        curr_signal_file = signal_files['calcular_edad']
        if curr_signal_file.exists() or event == "Calcular Edad":
            ejecutar_accion(
                accion_func=acciones.obtener_y_calcular_edad,
                signal_file_name=curr_signal_file,
                process_title="Cálculo de Edad",
                progress_message="↻ Procesando fecha de nacimiento...",
                success_message="😁👍 ¡Edad calculada con éxito!\n\nPuedes 📄 pegar el resultado.",
                error_message="❌ Ocurrió un error, reportar a 👨🏽 César:\n\n {}"
            )



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
