import os
from pydub import AudioSegment
import speech_recognition as sr

def convert_to_wav(input_path: str, output_path: str) -> None:
    audio = AudioSegment.from_file(input_path)
    audio.export(output_path, format="wav")

def transcribe_audio(file_path: str) -> str:
    if not file_path.lower().endswith('.wav'):
        raise ValueError("El archivo debe estar en formato WAV para SpeechRecognition.")

    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)

    try:
        return recognizer.recognize_google(audio, language="es-ES")
    except sr.UnknownValueError:
        return "No se pudo entender el audio."
    except sr.RequestError as e:
        return f"Error al conectarse a Google Speech Recognition: {e}"
