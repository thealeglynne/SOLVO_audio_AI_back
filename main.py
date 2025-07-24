import os
import uuid
import sys
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Asegurarse de poder importar desde iaModels
sys.path.append(os.path.join(os.path.dirname(__file__), "iaModels"))
from transcribir import convert_to_wav, transcribe_audio

# Inicializar FastAPI
app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://solvo-audio-ai.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/transcribir-audio/")
async def transcribir_audio_endpoint(file: UploadFile = File(...)):
    try:
        os.makedirs("uploads", exist_ok=True)

        # Guardar archivo temporal
        ext = file.filename.split('.')[-1]
        unique_name = f"{uuid.uuid4().hex}.{ext}"
        input_path = os.path.join("uploads", unique_name)

        with open(input_path, "wb") as f:
            f.write(await file.read())

        # Convertir si es necesario
        if not input_path.endswith(".wav"):
            wav_path = input_path.rsplit(".", 1)[0] + ".wav"
            convert_to_wav(input_path, wav_path)
        else:
            wav_path = input_path

        # Transcribir
        texto = transcribe_audio(wav_path)

        # Eliminar archivos temporales
        os.remove(input_path)
        if os.path.exists(wav_path) and wav_path != input_path:
            os.remove(wav_path)

        return {"transcripcion": texto}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
