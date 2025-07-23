from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import uuid
from iaModels.transcribir import transcribe_audio

app = FastAPI()

# Permitir frontend desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Reemplaza por el dominio real en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/transcribir-audio/")
async def transcribir_endpoint(file: UploadFile = File(...)):
    try:
        ext = os.path.splitext(file.filename)[-1]
        temp_filename = f"{uuid.uuid4()}{ext}"
        temp_path = os.path.join(UPLOAD_DIR, temp_filename)

        # Guardar temporalmente el audio
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Transcribir
        texto = transcribe_audio(temp_path)

        # Eliminar el archivo temporal
        os.remove(temp_path)

        return JSONResponse(content={"transcripcion": texto})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 🔥 Este bloque es CLAVE para que Render use el puerto correcto
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
