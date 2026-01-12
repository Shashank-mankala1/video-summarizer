import os
from groq import Groq
from app.services.retriever import Retriever
from app.rag.prompts import qa_prompt
from dotenv import load_dotenv
from app.services.reranker_service import ReRankerService

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class QAService:
    def __init__(self, index_path: str):
        self.retriever = Retriever(index_path)
        self.reranker = ReRankerService()

    def answer(self, question: str):
        # 1. Retrieve top 10 from FAISS
        retrieved_chunks = self.retriever.retrieve(question, top_k=10)

        # 2. Extract text for re-ranking
        documents = [c["text"] for c in retrieved_chunks]

        # 3. Re-rank and select best 3
        top_texts = self.reranker.rerank(
            query=question,
            documents=documents,
            top_k=3
        )

        # 4. Map back to original chunks (preserve timestamps)
        chunks = [c for c in retrieved_chunks if c["text"] in top_texts]

        context = "\n\n".join(
            f"[{c['start_time']} - {c['end_time']}]: {c['text']}"
            for c in chunks
        )

        prompt = qa_prompt(context, question)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        return {
            "answer": response.choices[0].message.content,
            "sources": chunks
        }
