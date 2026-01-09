import os
from groq import Groq
from app.services.retriever import Retriever
from app.rag.prompts import qa_prompt
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class QAService:
    def __init__(self, index_path: str):
        self.retriever = Retriever(index_path)

    def answer(self, question: str):
        chunks = self.retriever.retrieve(question, top_k=3)

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
