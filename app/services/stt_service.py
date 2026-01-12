import whisper
import os
import json

from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from app.utils.audio_utils import split_audio
from app.utils.transcript_utils import deduplicate_segments
import subprocess
class SpeechToTextService:
    def __init__(self, model_name: str = "base"):
        self.model = whisper.load_model(model_name)

    # ---------- helper ----------
    def _get_audio_duration(self, audio_path: str) -> float:
        cmd = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            audio_path
        ]
        return float(subprocess.check_output(cmd).decode().strip())

    # ---------- single transcription ----------
    def transcribe_single(self, audio_path: str, output_dir: str) -> str:
        os.makedirs(output_dir, exist_ok=True)

        result = self.model.transcribe(audio_path, verbose=False)

        transcript_path = os.path.join(
            output_dir,
            os.path.basename(audio_path).replace(".mp3", ".json")
        )

        with open(transcript_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        return transcript_path

    # ---------- parallel transcription ----------
    def transcribe_parallel(
        self,
        audio_path: str,
        output_dir: str,
        chunk_duration_sec: int = 60,
        overlap_sec: int = 2,
        max_workers: int = 2
    ) -> str:
        def is_valid_chunk(path: str) -> bool:
            try:
                duration = self._get_audio_duration(path)
                return duration > 1.0  # at least 1 second of audio
            except Exception:
                return False


        chunks = split_audio(
            audio_path=audio_path,
            chunk_duration_sec=chunk_duration_sec,
            overlap_sec=overlap_sec
        )

        all_segments = []

        def transcribe_chunk(chunk):
            print(f"DEBUG: Processing chunk {chunk['start_time']}...")
            try:
                if not is_valid_chunk(chunk["path"]):
                    print(f"DEBUG: Skipping empty chunk {chunk['start_time']}")
                    return
                
                result = self.model.transcribe(chunk["path"], language="en", verbose=False)
                for seg in result["segments"]:
                    seg["start"] += chunk["start_time"]
                    seg["end"] += chunk["start_time"]
                    all_segments.append(seg)
                
                print(f"DEBUG: Finished chunk {chunk['start_time']}")
            except Exception as e:
                print(f"ERROR: Chunk {chunk['start_time']} failed: {e}")
                raise e

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(transcribe_chunk, c) for c in chunks]
            for _ in as_completed(futures):
                pass

        all_segments.sort(key=lambda x: x["start"])
        all_segments = deduplicate_segments(all_segments)

        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "transcript_parallel.json")

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump({"segments": all_segments}, f, indent=2)

        return output_path

    # ---------- AUTO SWITCH (STEP 2D) ----------
    def transcribe(self, audio_path: str, output_dir: str) -> str:
        duration = self._get_audio_duration(audio_path)
        print(f"DEBUG: Audio duration: {duration} seconds")
        print(f"[DEBUG] Transcription mode: {'PARALLEL' if duration > 300 else 'SINGLE'}")

        # 5 minutes threshold
        return self.transcribe_single(audio_path, output_dir)

        # THRESHOLD = 300
        # if duration > THRESHOLD:
        #     try:
        #         print(f"DEBUG: Duration {duration}s > {THRESHOLD}s. 🚀 Starting PARALLEL transcription...")
        #         return self.transcribe_parallel(audio_path, output_dir)
        #     except Exception as e:
        #         print(f"ERROR: Parallel transcription failed: {e}")
        #         return self.transcribe_single(audio_path, output_dir)
        # else:
        #     print(f"DEBUG: Duration {duration}s <= {THRESHOLD}s. 🐢 Starting SINGLE transcription...")
        #     return self.transcribe_single(audio_path, output_dir)