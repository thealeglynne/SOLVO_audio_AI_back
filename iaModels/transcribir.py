import whisper
import os
import sys

def transcribe_audio(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")

    model = whisper.load_model("base")
    result = model.transcribe(file_path)

    return result["text"]

# Agrega este bloque
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python transcribir.py <archivo.mp3>")
        sys.exit(1)

    path = sys.argv[1]

    try:
        texto = transcribe_audio(path)
        print("\n📝 Transcripción:\n")
        print(texto)
    except Exception as e:
        print(f"⚠️ Error al transcribir: {e}")
