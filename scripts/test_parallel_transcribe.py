import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.stt_service import SpeechToTextService

stt = SpeechToTextService()

out = stt.transcribe_parallel(
    audio_path="data/file_example_WAV_5MG.wav",
    output_dir="data/transcripts_test",
    chunk_duration_sec=30,
    max_workers=4
)

print("Transcript saved at:", out)
