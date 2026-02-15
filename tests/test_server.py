import os
import server.server as app_module


def test_health_endpoint(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_transcribe_endpoint_returns_expected_fields(client, monkeypatch):
    class FakeModel:
        def transcribe(self, file_location):
            return {"text": "hello world"}

    # override whisper.load_model used inside the endpoint
    monkeypatch.setattr(app_module.whisper, "load_model", lambda name: FakeModel())

    files = {"file": ("sample.wav", b"fake-audio-bytes", "audio/wav")}
    r = client.post("/transcribe/", files=files)
    assert r.status_code == 200

    data = r.json()
    assert data["original"] == "hello world"
    assert data["corrected"].startswith("gpt4all-corrected:")

    saved = os.path.join("server", "temp", "sample.wav")
    assert os.path.exists(saved)
    os.remove(saved)


def test_transcribe_handles_list_texts(client, monkeypatch):
    class FakeModel2:
        def transcribe(self, file_location):
            return {"text": ["one", "two"]}

    monkeypatch.setattr(app_module.whisper, "load_model", lambda name: FakeModel2())

    files = {"file": ("sample2.wav", b"audio", "audio/wav")}
    r = client.post("/transcribe/", files=files)
    assert r.status_code == 200
    assert r.json()["original"] == "one two"

    saved = os.path.join("server", "temp", "sample2.wav")
    assert os.path.exists(saved)
    os.remove(saved)


def test_transcribe_missing_file_returns_422(client):
    r = client.post("/transcribe/", data={})
    assert r.status_code == 422
