import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from app.api.routes.qa import router as qa_router
from app.api.routes.video import router as video_router

app = FastAPI(title="YouTube Video Summarizer API")

app.include_router(video_router, prefix="/video")
app.include_router(qa_router, prefix="/qa")


@app.get("/")
def root():
    return {"message": "Welcome to the YouTube Video Summarizer API!"}

@app.get("/health")
def health():
    return {"status": "ok"}
