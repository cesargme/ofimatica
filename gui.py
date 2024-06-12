import os
import sys
import PySimpleGUI as sg
from psgtray import SystemTray
import acciones_todas
import logging
import updater
import gpt
from pathlib import Path
import keyboard
import queue
import pygetwindow as gw

event_queue = queue.Queue()

def handle_hotkey(accion):
    event_queue.put(accion)

SIGNAL_FILES_DIR = os.path.expanduser('~/ofimatica/signals')
if not os.path.exists(SIGNAL_FILES_DIR):
    os.makedirs(SIGNAL_FILES_DIR)

logging.basicConfig(
    filename="app.log", filemode="w", format="%(name)s - %(levelname)s - %(message)s"
)

# Variable global para la bandeja del sistema
tray = None


def verificar_actualizacion():
    return updater.check_git_diff()


def iniciar_actualizacion():
    updater.update_program(updater.get_latest_version())
    pass


class Accion:
    def __init__(self, nombre, archivo_signal, funcion, mensajes, usar_clipboard_decorator=False, hotkey=None):
        self.nombre = nombre
        self.archivo_signal = Path(SIGNAL_FILES_DIR) / archivo_signal
        self.funcion = funcion
        self.mensajes = mensajes
        self.usar_clipboard_decorator = usar_clipboard_decorator
        self.hotkey = hotkey  # Tecla rápida opcional

    def intentar_ejecutar(self, event, delay):
        if self.usar_clipboard_decorator:
            self.funcion_decorada = acciones_todas.clipboard_decorator(self.ejecutar, delay)
        else:
            self.funcion_decorada = self.ejecutar

        if self.archivo_signal.exists() or event == self.nombre or (self.hotkey and event == self.hotkey):
            self.funcion_decorada()

    def ejecutar(self):
        curr_signal_file = Path(self.archivo_signal)
        active_window_before = gw.getActiveWindow()  # Almacena la ventana activa antes de iniciar el medidor de progreso
        try:
            sg.one_line_progress_meter(
                self.mensajes["titulo"],
                20,
                100,
                self.mensajes["progreso"],
                key="-PROG-",
                orientation="h",
                keep_on_top=True,
                no_titlebar=False,
                no_button=True,
            )
            # Ejecuta la función asignada
            self.funcion()
            sg.one_line_progress_meter_cancel(key="-PROG-")
            if active_window_before:  # Verifica si se ha almacenado una ventana
                active_window_before.activate()  # Restaura el foco a la ventana original
            if curr_signal_file.exists():
                curr_signal_file.unlink()
            tray.show_message(self.mensajes["titulo"], self.mensajes["exito"])
        except Exception as e:
            tray.show_message(self.mensajes["titulo"], self.mensajes["error"].format(e))
            logging.exception("Error during action execution")
        finally:
            sg.one_line_progress_meter_cancel(key="-PROG-")
            if active_window_before:  # Verifica de nuevo por si acaso
                active_window_before.activate()  # Restaura el foco a la ventana original


acciones_lista = [
    Accion(
        "Extraer info de transacción financiera",
        "transaccion.txt",
        acciones_todas.extraer_info_transaccion_financiera,
        {
            "titulo": "Extrayendo info de imagen financiera",
            "progreso": "↻ Procesando texto...",
            "exito": "😁👍 Listo! Puedes pegarlo en Excel",
            "error": "❌ Ocurrió un error, reportar a 👨🏽 César:\n\n {,}"
        },
        usar_clipboard_decorator=False,
    ),
    Accion(
        "Corregir ortografía",
        "corregir_ortografia.txt",
        acciones_todas.corregir_ortografia,
        {
            "titulo": "Corrección ortográfica",
            "progreso": "↻ Procesando texto...",
            "exito": "😁👍 ¡Texto corregido con éxito!",
            "error": "❌ Ocurrió un error, reportar a 👨🏽 César:\n\n {,}"
        },
        usar_clipboard_decorator=True,
    ),
    Accion(
        "CIE-10",
        "cie10.txt",
        acciones_todas.cie10,
        {
            "titulo": "Obteniendo códigos CIE-10",
            "progreso": "↻ Procesando diagnósticos...",
            "exito": "😁👍 ¡Códigos CIE-10 obtenidos con éxito!\n\nPuedes 📄 pegarlos.",
            "error": "❌ Ocurrió un error, reportar a 👨🏽 César:\n\n {,}"
        },
        usar_clipboard_decorator=True,
    ),
    Accion(
        "PacPart: Extraer Fechas y Horas",
        "pac_part_extraer_fechas_horas.txt",
        acciones_todas.pacpart_extraer_fechas_horas,
        {
            "titulo": "Extrayendo fechas y horas",
            "progreso": "↻ Procesando texto para encontrar fechas y horas...",
            "exito": "😁👍 ¡Fechas y horas extraídas con éxito!\n\nPuedes 📄 pegarlas en el formato deseado.",
            "error": "❌ Ocurrió un error, reportar a 👨🏽 César:\n\n {,}"
        },
        usar_clipboard_decorator=True,
    ),
    Accion(
        "Calcular Edad",
        "calcular_edad.txt",
        acciones_todas.obtener_y_calcular_edad,
        {
            "titulo": "Cálculo de Edad",
            "progreso": "↻ Procesando fecha de nacimiento...",
            "exito": "😁👍 ¡Edad calculada con éxito!\n\nPuedes 📄 pegar el resultado.",
            "error": "❌ Ocurrió un error, reportar a 👨🏽 César:\n\n {,}"
        },
        usar_clipboard_decorator=True,
    ),

    Accion(
    "Convertir PDF a PNG",
    "convertir_pdf_a_png.txt",  # Nombre del archivo de señal, si es necesario
    acciones_todas.convertir_pdf_a_png,
    {
        'titulo': "Conversión de PDF a PNG",
        'progreso': "↻ Convirtiendo...",
        'exito': "😁👍 ¡Conversión completada con éxito!",
        'error': "❌ Ocurrió un error: {}"
    },
    usar_clipboard_decorator=False  # Suponiendo que no necesitas el decorador aquí
)

]


def run_application():
    global tray

    menu_items = [accion.nombre for accion in acciones_lista]
    menu = ["", menu_items + ["⚙️ Abrir registro de errores", "Salir"]]

    tooltip = "Aplicación de corrección ortográfica"

    layout = [[sg.Text("Ofimática")]]

    window = sg.Window(
        "Ofimática", layout, finalize=True, enable_close_attempted_event=True
    )
    window.hide()

    tray = SystemTray(
        menu,
        single_click_events=False,
        window=window,
        tooltip=tooltip,
        icon="buho.ico",
    )

    gpt.set_api_key()  # Llama a set_api_key()

    # Verificar actualizaciones
    if verificar_actualizacion():
        respuesta = sg.popup_yes_no(
            "Hay una nueva actualización disponible. ¿Deseas actualizar el programa?",
            title="Actualización disponible",
        )
        if respuesta == "Yes":
            iniciar_actualizacion()
            # Reiniciar el programa
            os.execv(sys.executable, ["python"] + sys.argv)

    # Configuración de hotkeys para las acciones
    for accion in acciones_lista:
        if accion.hotkey:
            keyboard.add_hotkey(accion.hotkey, lambda accion=accion: handle_hotkey(accion))

    while True:
        try:
            accion = event_queue.get_nowait()  # Intenta obtener un evento de la cola
            accion.intentar_ejecutar(accion.nombre, delay=5)
        except queue.Empty:
            pass  # No hay eventos en la cola

        event, values = window.read(timeout=100)

        # Si es un evento de la bandeja del sistema, cambia el evento a lo que la bandeja envió
        if event == tray.key:
            event = values[0]

        if event in (sg.WIN_CLOSED, "Salir"):
            break

        for accion in acciones_lista:
            if event in [accion.nombre] or Path(accion.archivo_signal).exists():
                delay = 0.8 if Path(accion.archivo_signal).exists() else 5
                accion.intentar_ejecutar(event, delay=delay)

        if event == sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED:
            window.un_hide()
            window.bring_to_front()
        elif event == sg.WIN_CLOSE_ATTEMPTED_EVENT:
            window.hide()
            tray.show_icon()

        elif event == "⚙️ Abrir registro de errores":
            os.startfile("app.log")

    tray.close()
    window.close()

    # Remover hotkeys cuando la aplicación se cierre
    for accion in acciones_lista:
        if accion.hotkey:
            keyboard.remove_hotkey(accion.hotkey)


def main():
    try:
        run_application()
    except Exception as e:
        if tray is not None:
            tray.show_message("⚙️ Configuración necesaria", str(e))
        else:
            sg.popup_error("Error", str(e) + " Por favor, cierra el programa.")
        exit(1)


if __name__ == "__main__":
    main()

# TODO Reiniciar si es que hay una excepcion ( o poner en inicio app mia
# TODO ver por qué hay excepccion al usar el extractor de imagen info financiera
