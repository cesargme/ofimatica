import subprocess
import time
import ollama
import util.myclipboard_util as myclipboard_util
import psutil

# Iniciar el servidor de Ollama
def start_ollama_server():
    try:
        # Iniciar el servidor en segundo plano
        process = subprocess.Popen(["ollama", "serve"])
        print("Servidor de Ollama iniciado.")
        # Esperar unos segundos para asegurarse de que el servidor está completamente iniciado
        time.sleep(5)
        return process
    except Exception as e:
        print(f"Error al iniciar el servidor de Ollama: {e}")

# Detener el servidor de Ollama
def stop_ollama_server(process):
    try:
        # Obtener el proceso por su nombre
        for proc in psutil.process_iter(['pid', 'name']):
            if 'ollama_llama_server' in proc.info['name']:
                proc.terminate()
                proc.wait()
                print("Servidor de Ollama detenido.")
    except Exception as e:
        print(f"Error al detener el servidor de Ollama: {e}")


def prompt(msg, serve:bool):

    try:
        server_process = start_ollama_server()
        response = ollama.generate(model="llama3", prompt=msg, format="json")
        return response["response"]
    finally:
        if serve:
            stop_ollama_server(server_process)