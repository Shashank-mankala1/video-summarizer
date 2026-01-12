import numpy as np
from app.services.embedding_service import EmbeddingService
from app.db.vector_db import VectorDB

class Retriever:
    def __init__(self, index_path: str, embedding_model: str = "all-MiniLM-L6-v2"):
        self.embedding_service = EmbeddingService(embedding_model)
        self.vector_db = VectorDB(dim=384, index_path=index_path)
        self.vector_db.load()

    def retrieve(self, query: str, top_k: int = 3):
        query_embedding = self.embedding_service.embed_texts([query])
        query_embedding = np.array(query_embedding).astype("float32")

        distances, indices = self.vector_db.index.search(query_embedding, k=10)

        results = []
        for idx in indices[0]:
            results.append(self.vector_db.metadata[idx])

        return results
