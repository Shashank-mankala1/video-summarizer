import os
from groq import Groq

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

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        return response.choices[0].message.content
