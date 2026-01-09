
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from app.services.embedding_service import EmbeddingService
from app.db.vector_db import VectorDB

CHUNKS_PATH = "data/transcripts/c7ZAceXakIE_chunks.json"
INDEX_PATH = "data/vector_store/c7ZAceXakIE.index"

with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
    chunks = json.load(f)

texts = [c["text"] for c in chunks]

embedding_service = EmbeddingService()
embeddings = embedding_service.embed_texts(texts)

vector_db = VectorDB(dim=len(embeddings[0]), index_path=INDEX_PATH)

metadatas = [
    {
        "text": c["text"],
        "start_time": c["start_time"],
        "end_time": c["end_time"]
    }
    for c in chunks
]

vector_db.add(embeddings, metadatas)
vector_db.save()

print(f"Stored {len(chunks)} chunks in vector DB")
