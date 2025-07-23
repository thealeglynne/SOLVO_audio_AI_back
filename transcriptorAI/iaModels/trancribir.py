# transcriptorAI/iaModels/transcribir.py

import whisper
import os

def transcribe_audio(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")

    model = whisper.load_model("base")
    result = model.transcribe(file_path)

    return result["text"]
