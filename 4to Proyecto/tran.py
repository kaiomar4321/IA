import whisper
import os

def transcribe_file(input_path, output_path="texto2.txt", model_size="base"):
    """
    Transcribe un archivo de audio o video usando Whisper.
    
    Args:
        input_path (str): Ruta del archivo de entrada (audio o video).
        output_path (str): Ruta del archivo donde se guardará la transcripción.
        model_size (str): Tamaño del modelo Whisper ("tiny", "base", "small", "medium", "large").
    """
    # Cargar el modelo de Whisper
    print(f"Cargando el modelo Whisper ({model_size})...")
    model = whisper.load_model(model_size)

    # Verificar si el archivo existe
    if not os.path.exists(input_path):
        print(f"El archivo {input_path} no existe.")
        return

    print(f"Transcribiendo el archivo: {input_path}...")
    result = model.transcribe(input_path)

    # Guardar la transcripción en un archivo de texto
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result["text"])
    
    print(f"Transcripción completada. Guardada en: {output_path}")

# RUTA DEL ARCHIVO LOCAL (audio o video)
input_path = "C:/Users/omar_/Videos/chisme.mkv"  # Cambia esto a la ruta del archivo local
output_path = "texto2.txt"  # Archivo de salida

# LLAMAR A LA FUNCIÓN
transcribe_file(input_path, output_path, model_size="base")  # Puedes cambiar el modelo según tu hardware
