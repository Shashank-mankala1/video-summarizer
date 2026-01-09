import whisper
import os
import json

class SpeechToTextService:
    def __init__(self, model_size: str = "base"):
        self.model = whisper.load_model(model_size)

    def transcribe(self, audio_path: str, output_dir: str) -> str:
        os.makedirs(output_dir, exist_ok=True)

        result = self.model.transcribe(
            audio_path,
            verbose=False
        )

        transcript_path = os.path.join(
            output_dir,
            os.path.basename(audio_path).replace(".mp3", ".json")
        )

        with open(transcript_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        return transcript_path
