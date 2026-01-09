import json
from typing import List, Dict

class TranscriptChunker:
    def __init__(self, max_words: int = 200):
        self.max_words = max_words

    def chunk_transcript(self, transcript_path: str) -> List[Dict]:
        with open(transcript_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        segments = data["segments"]

        chunks = []
        current_chunk = []
        current_word_count = 0

        chunk_start = None

        for seg in segments:
            text = seg["text"].strip()
            words = text.split()

            if not words:
                continue

            if chunk_start is None:
                chunk_start = seg["start"]

            current_chunk.append(text)
            current_word_count += len(words)

            if current_word_count >= self.max_words:
                chunks.append({
                    "text": " ".join(current_chunk),
                    "start_time": chunk_start,
                    "end_time": seg["end"]
                })

                current_chunk = []
                current_word_count = 0
                chunk_start = None

        if current_chunk:
            chunks.append({
                "text": " ".join(current_chunk),
                "start_time": chunk_start,
                "end_time": segments[-1]["end"]
            })

        return chunks
