"""Pytest fixtures + lightweight mocks for heavy external libs.

This file ensures `gpt4all` and `whisper` are replaced with small, deterministic
fakes before `server.server` is imported so tests don't try to load large
models at import-time.

Provides:
- `client` fixture (FastAPI TestClient)
"""
import sys
import types
import pytest

# --- Mock gpt4all (prevent import-time model loading) ----------------------
gpt4all_mod = types.ModuleType("gpt4all")

class DummyGPT4All:
    def __init__(self, *args, **kwargs):
        self.last_prompt = None

    def generate(self, prompt, max_tokens=80, temp=0.3):
        self.last_prompt = prompt
        return "gpt4all-corrected: " + prompt.split(":")[-1].strip()

gpt4all_mod.GPT4All = DummyGPT4All
sys.modules["gpt4all"] = gpt4all_mod

# --- Mock whisper (avoid large model downloads during tests) --------------
whisper_mod = types.ModuleType("whisper")

def _fake_load_model(name):
    class _FakeModel:
        def transcribe(self, file_location):
            return {"text": "dummy transcription"}

    return _FakeModel()

whisper_mod.load_model = _fake_load_model
sys.modules["whisper"] = whisper_mod

# --- Import the FastAPI app (safe because mocks are in place) -------------
import server.server as server_app  # noqa: E402


@pytest.fixture
def client():
    from fastapi.testclient import TestClient

    return TestClient(server_app.app)
