import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class SummaryService:
    def generate_summary(self, chunks):
        context = "\n\n".join(c["text"] for c in chunks)

        prompt = f"""
Summarize the following video transcript in one clear paragraph.
Focus on the main idea and key points.
Do not add anything that is not present in the text.

Transcript:
{context}

Summary:
"""

        models = ["llama-3.1-8b-instant", "meta-llama/llama-guard-4-12b", "meta-llama/llama-prompt-guard-2-22m", "meta-llama/llama-prompt-guard-2-86m"]

        for model in models:
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"Model {model} failed: {e}")
                continue
        
        raise Exception("All summary models failed")
