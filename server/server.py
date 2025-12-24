from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import whisper
import os
from server.rewrite_llm import rewrite_to_american_english

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}

# Absolute path inside server folder
UPLOAD_DIR = "server/temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/transcribe/")
async def transcribe(file: UploadFile = File(...)):
    try:
        # Save uploaded file
        file_location = f"{UPLOAD_DIR}/{file.filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())

        # Process with Whisper
        model = whisper.load_model("base") 
        result = model.transcribe(file_location)
        original_text = result["text"]
        
        # Ensure text is a string
        if isinstance(original_text, list):
            original_text = " ".join(original_text)

        # Rewrite to American English
        corrected_text = rewrite_to_american_english(original_text)

        return {"original": original_text, "corrected": corrected_text}
    except Exception as e:
        return {"error": str(e)}