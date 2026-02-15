# AccentAppServer

⚡️ Lightweight speech-transcription + American‑English rewrite service (local-first).

- Transcribes audio with OpenAI Whisper (local) and rewrites the transcript to American English using a local GPT4All model by default.

---

## Contents
- Features
- Requirements
- Quick start
- API
- Configuration & behavior
- Development notes
- Troubleshooting

---

## Features ✅
- Single HTTP endpoint to upload audio and receive: `original` (raw transcription) and `corrected` (American‑English rewrite).
- Uses `openai-whisper` for accurate local transcription.
- Uses `gpt4all` (local GGUF model) for rewrite; a simple rule-based fallback exists in `server/rewrite.py`.

---

## Requirements 🔧
- Python 3.10+ (create a venv recommended)
- See `requirements.txt` for exact packages (Whisper, FastAPI, GPT4All, Torch, etc.)
- A GPT4All GGUF model file placed in `./models` when using `rewrite_llm.py` (the repo sets `allow_download=False`).

---

## Quick start (local, Windows / macOS / Linux)
1. Create & activate virtualenv

   Windows (PowerShell):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   macOS / Linux:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure models are available
   - Whisper model `base` will be downloaded on first run by `openai-whisper`.
   - GPT4All model expected: `Llama-3.2-1B-Instruct-Q5_K_M.gguf` (place in `./models`) or set `allow_download=True` in `server/rewrite_llm.py`.

4. Run server
   ```bash
   uvicorn server.server:app --host 0.0.0.0 --port 8000 --reload
   ```

---

## API 📡
- Health
  - GET `/` → `{ "status": "ok" }`

- Transcribe & rewrite
  - POST `/transcribe/`
  - Content-Type: `multipart/form-data` with field name `file` (audio file)
  - Response example:
    ```json
    { "original": "...transcribed text...", "corrected": "...rewritten text..." }
    ```

cURL example:
```bash
curl -X POST "http://localhost:8000/transcribe/" -F "file=@./audio/sample.wav"
```

Python example (requests):
```python
import requests
r = requests.post('http://localhost:8000/transcribe/', files={'file': open('sample.wav','rb')})
print(r.json())
```

---

## Configuration & implementation details 🔍
- Entry point: `server/server.py` (loads Whisper model `base` and calls `rewrite_to_american_english`).
- Rewrite implementations:
  - LLM-based: `server/rewrite_llm.py` (uses `gpt4all`); model loaded at import time.
  - Rule-based: `server/rewrite.py` (simple replacements) — useful when no local GGUF model is available.
- Upload directory: `server/temp` (files are saved there; currently not auto-deleted).
- Adjust LLM threads in `rewrite_llm.py` via `n_threads`.

To use the rule-based rewrite instead of GPT4All, update the import in `server/server.py`:
```py
# from server.rewrite_llm import rewrite_to_american_english
from server.rewrite import rewrite_to_american_english
```

---

## Troubleshooting & tips ⚠️
- If the server crashes at startup: check `rewrite_llm.py` — the GPT4All model must exist in `./models` or `allow_download` must be enabled.
- Slow or out-of-memory during transcription/LLM inference: reduce `n_threads` or use smaller models.
- File uploads: ensure `server/temp` is writable. Consider adding a cleanup routine for temporary files.

## Testing 🧪
- Tests are implemented with `pytest` and live under the `tests/` directory. The suite includes a `conftest.py` that mocks heavy external dependencies (`whisper`, `gpt4all`) so tests run quickly without downloading large models.

Setup & run:

```bash
pip install -r requirements.txt
pip install pytest
pytest -q
```

What the tests cover:
- `tests/test_server.py` — FastAPI endpoints (health + `/transcribe/`), file saving and edge-cases
- `tests/test_rewrite.py` — rule-based rewrite logic
- `tests/test_rewrite_llm.py` — LLM prompt + model-integration behavior (uses a dummy GPT4All)

CI suggestion:
- Add a GitHub Actions workflow to run `pytest` on push/PR. If you want, I can add a ready-to-use workflow file.

---

## Contributing & license
- PRs welcome — modify `rewrite.py` / `rewrite_llm.py` for different rewriting strategies.
- License: none

---

If you'd like, I can add example unit tests, a Dockerfile, or switch the server to use the rule-based rewrite as a fallback — tell me which you'd prefer. ✨
