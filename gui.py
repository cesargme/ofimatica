import os
import sys
import PySimpleGUI as sg
from psgtray import SystemTray
import acciones
import logging
import updater

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


def verificar_actualizacion():
    latest_version = updater.get_latest_version()
    curr_version = updater.get_current_version()
    return latest_version != curr_version

def iniciar_actualizacion():
    updater.update_program(updater.get_latest_version())
    pass

def main():
    menu = ['', ['Corregir ortografía', '⚙️ Abrir registro de errores', 'Salir']]
    tooltip = 'Aplicación de corrección ortográfica'

    layout = [[sg.Text('Corrección ortográfica')]]

    window = sg.Window('Corrección ortográfica', layout, finalize=True, enable_close_attempted_event=True)
    window.hide()

    tray = SystemTray(menu, single_click_events=False, window=window, tooltip=tooltip, icon='icono.ico')

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
        if os.path.exists('corregir_ortografia.txt') or event == "Corregir ortografía":
            try:
                sg.one_line_progress_meter('Corrección ortográfica', 20, 100, '↻ Procesando texto...', key="-PROG-",orientation='h')
                acciones.corregir_ortografia()
                sg.one_line_progress_meter_cancel(key="-PROG-")
                if os.path.exists('corregir_ortografia.txt'):
                    os.remove('corregir_ortografia.txt')
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

if __name__ == '__main__':
    main()