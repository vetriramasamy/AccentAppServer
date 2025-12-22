from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import whisper
import os

app = FastAPI()

model = whisper.load_model("base")  # Load Whisper model once

# Absolute path inside server folder
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "temp")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/transcribe/")
async def transcribe(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save uploaded file
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Process with Whisper
    result = model.transcribe(file_path)
    transcription = result["text"]

    return JSONResponse(content={"text": transcription})
