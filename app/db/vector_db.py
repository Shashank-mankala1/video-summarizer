import faiss
import json
import os
import numpy as np

class VectorDB:
    def __init__(self, dim: int, index_path: str):
        self.dim = dim
        self.index_path = index_path
        self.meta_path = index_path + ".meta.json"

        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

    def add(self, embeddings, metadatas):
        embeddings = np.array(embeddings).astype("float32")
        self.index.add(embeddings)
        self.metadata.extend(metadatas)

    def save(self):
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, self.index_path)

        with open(self.meta_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2)

    def load(self):
        self.index = faiss.read_index(self.index_path)
        with open(self.meta_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)
