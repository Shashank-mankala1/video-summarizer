import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.rag.chunking import TranscriptChunker
from app.utils.helpers import save_chunks

TRANSCRIPT_PATH = "data/transcripts/c7ZAceXakIE.json"
OUTPUT_PATH = "data/transcripts/c7ZAceXakIE_chunks.json"

chunker = TranscriptChunker(max_words=200)
chunks = chunker.chunk_transcript(TRANSCRIPT_PATH)

save_chunks(chunks, OUTPUT_PATH)

print(f"Created {len(chunks)} chunks")
