def qa_prompt(context: str, question: str) -> str:
    return f"""
You are an assistant answering questions strictly using the provided context.
If the answer is not present in the context, say "I do not know based on the video."

Context:
{context}

Question:
{question}

Answer:
"""
