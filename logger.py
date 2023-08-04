import os
import pickle
import collections
import logging

# La ruta del archivo de log
log_file = 'app.log'

# Cargar la cola de registros de excepciones
try:
    with open(log_file, 'rb') as f:
        exception_queue = pickle.load(f)
except (FileNotFoundError, EOFError):
    exception_queue = collections.deque(maxlen=5)

# Configurar el logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.ERROR)

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
        logger.exception("Ocurrió un error al corregir la ortografía")
        
        # Agregar la excepción a la cola
        exception_queue.append(e)
        
        # Guardar la cola de excepciones
        with open(log_file, 'wb') as f:
            pickle.dump(exception_queue, f)
    finally:
        sg.one_line_progress_meter_cancel(key="-PROG-")
