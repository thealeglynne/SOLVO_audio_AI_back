import os
import sys
import time
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Agrega el subdirectorio 'iaModels' al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'iaModels'))

# Importar función de transcripción
from transcribir import transcribe_audio

# Inicializar app
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

# ✅ Ruta base para Render (evita el 404 en "/")
@app.get("/")
def root():
    return {"status": "Servidor de transcripción activo ✅"}

# Endpoint POST para transcribir audio
@app.post("/transcribir-audio/")
async def transcribir_audio_endpoint(file: UploadFile = File(...)):
    try:
        os.makedirs("uploads", exist_ok=True)

        safe_filename = file.filename.replace(" ", "_").replace("..", "")
        temp_path = os.path.join("uploads", safe_filename)

        # Guardar archivo temporal
        with open(temp_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Transcribir
        texto = transcribe_audio(temp_path)

        # Eliminar archivo
        os.remove(temp_path)

        return {"transcripcion": texto}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al transcribir: {e}")

# Permitir correr desde CLI
def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <archivo_audio.mp3>")
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.exists(path):
        print(f"❌ El archivo {path} no existe.")
        sys.exit(1)

    print("⏳ Transcribiendo audio...")
    try:
        texto = transcribe_audio(path)
        print("✅ Transcripción completada:\n")
        print(texto)
    except Exception as e:
        print(f"❌ Error al transcribir: {e}")

# 🚀 Iniciar servidor si es llamado como app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render usa este valor
    uvicorn.run(app, host="0.0.0.0", port=port)
