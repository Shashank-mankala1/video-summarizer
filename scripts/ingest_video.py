import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.youtube_service import YouTubeService
from app.services.audio_service import AudioService
from app.services.stt_service import SpeechToTextService

YOUTUBE_URL = "https://www.youtube.com/watch?v=c7ZAceXakIE"

yt_service = YouTubeService(output_dir="data/raw_videos")
stt_service = SpeechToTextService(model_size="base")

audio_file = yt_service.download_audio(YOUTUBE_URL)

transcript_path = stt_service.transcribe(
    audio_path=audio_file,
    output_dir="data/transcripts"
)

print("Transcript saved at:", transcript_path)
