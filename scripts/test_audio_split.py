import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.audio_utils import split_audio

chunks = split_audio(
    audio_path="data/file_example_WAV_5MG.wav",  # use any audio you already have
    chunk_duration_sec=30
)

print(len(chunks))
print(chunks[0])
