import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from fastapi import APIRouter
from pydantic import BaseModel
from app.services.qa_service import QAService
from app.services.reranker_service import ReRankerService
reranker = ReRankerService()

router = APIRouter()

LATEST_VIDEO_FILE = "data/vector_store/latest.txt"

def get_latest_index():
    with open(LATEST_VIDEO_FILE, "r") as f:
        video_id = f.read().strip()
    return f"data/vector_store/{video_id}.index"



class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    sources: list

@router.post("/ask", response_model=AnswerResponse)
def ask_question(req: QuestionRequest):
    index_path = get_latest_index()
    qa_service = QAService(index_path)
    result = qa_service.answer(req.question)
    return result
