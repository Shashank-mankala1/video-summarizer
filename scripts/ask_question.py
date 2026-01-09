import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



from app.services.qa_service import QAService

INDEX_PATH = "data/vector_store/c7ZAceXakIE.index"

qa = QAService(INDEX_PATH)

question = "What is the main topic of the video?"

result = qa.answer(question)

print("Answer:\n", result["answer"])
print("\nSources:")
for s in result["sources"]:
    print(f"- {s['start_time']} to {s['end_time']}")
