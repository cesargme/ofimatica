import os
import pytest
from audio_processing import convertir_mkv_a_mp3, dividir_audio_en_chunks

def test_convertir_mkv_a_mp3():
    ruta_mkv = "longvideo_test.mkv"
    ruta_mp3_temp = "temp_audio.mp3"
    
    # Crear un archivo .mkv de prueba
    # Aquí deberías agregar código para crear un archivo .mkv de prueba
    
    convertir_mkv_a_mp3(ruta_mkv, ruta_mp3_temp)
    
    assert os.path.exists(ruta_mp3_temp)
    
    # Limpiar archivo temporal después de la prueba
    # os.remove(ruta_mp3_temp)

def test_dividir_audio_en_chunks():
    ruta_mp3_temp = "temp_audio.mp3"
    carpeta_salida = "chunks_audio"
    duracion_minutos = 10

    # Crear un archivo .mp3 de prueba
    # Aquí deberías agregar código para crear un archivo .mp3 de prueba

    dividir_audio_en_chunks(ruta_mp3_temp, duracion_minutos, carpeta_salida)
    
    # Verificar que se hayan creado los fragmentos
    chunks = os.listdir(carpeta_salida)
    assert len(chunks) > 0  # Asegurarse de que se hayan creado archivos

    # Limpiar archivos temporales y la carpeta de salida después de la prueba
    for chunk in chunks:
        os.remove(os.path.join(carpeta_salida, chunk))
    os.rmdir(carpeta_salida)
    # os.remove(ruta_mp3_temp)

# Llama a pytest.main() para ejecutar las pruebas si este archivo se ejecuta directamente
if __name__ == "__main__":
    pytest.main()
