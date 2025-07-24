import os
import sys
import time  # <- necesario si quieres usar timestamp luego
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Agregar iaModels al sys.path para poder importar el módulo
sys.path.append(os.path.join(os.path.dirname(__file__), 'iaModels'))

# Ahora sí puedes importar el transcribe_audio
from transcribir import transcribe_audio

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

# Endpoint POST para recibir y transcribir un archivo de audio
@app.post("/transcribir-audio/")
async def transcribir_audio_endpoint(file: UploadFile = File(...)):
    try:
        # Asegurar que la carpeta 'uploads' exista
        os.makedirs("uploads", exist_ok=True)

        # Reemplazar espacios en el nombre del archivo
        safe_filename = file.filename.replace(" ", "_")
        temp_path = f"uploads/{safe_filename}"

        # Guardar archivo temporalmente
        with open(temp_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Transcribir usando Whisper
        texto = transcribe_audio(temp_path)

        # Eliminar el archivo temporal
        os.remove(temp_path)

        return {"transcripcion": texto}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Permitir ejecutar desde la terminal también
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # 8000 solo por si corres local
    uvicorn.run(app, host="0.0.0.0", port=port)
