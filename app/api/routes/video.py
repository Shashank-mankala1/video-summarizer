from fastapi import APIRouter
from pydantic import BaseModel
import os

from app.services.youtube_service import YouTubeService
from app.services.stt_service import SpeechToTextService
from app.rag.chunking import TranscriptChunker
from app.services.embedding_service import EmbeddingService
from app.db.vector_db import VectorDB
from app.services.summary_service import SummaryService
from fastapi import APIRouter, BackgroundTasks
from app.utils.task_store import task_status
import uuid
from rq import Queue
from app.utils.redis_conn import redis_conn
from app.workers.ingest_worker import run_ingestion
from app.utils.eta_config import STAGE_ORDER, STAGE_AVG_TIME
import time


queue = Queue("ingestion", connection=redis_conn)

router = APIRouter()

class VideoRequest(BaseModel):
    youtube_url: str
def estimate_eta(video_duration: float, status: str) -> int:
    """
    Returns ETA in seconds.
    Data-driven, duration-based ETA.
    """

    if status == "completed":
        return 0

    # Once transcription is done, we are almost finished
    if status != "transcribing":
        return 5

    # Transcription ETA buckets (based on real measurements)
    if video_duration <= 300:
        return 30
    elif video_duration <= 600:
        return 35
    elif video_duration <= 900:
        return 45
    else:
        return int(55 + (video_duration - 900) * 0.01)

@router.get("/status/{task_id}")
def get_status(task_id: str):
    status = redis_conn.hget(task_id, "status")
    return {"status": status or "unknown"}



@router.post("/ingest")
def ingest_video(req: VideoRequest):
    video_id = req.youtube_url.split("v=")[-1]

    index_path = f"data/vector_store/{video_id}.index"
    summary_path = f"data/summaries/{video_id}.txt"

    # ✅ VIDEO-LEVEL CACHE CHECK
    if os.path.exists(index_path) and os.path.exists(summary_path):
        with open("data/vector_store/latest.txt", "w") as f:
            f.write(video_id)

        with open(summary_path, "r", encoding="utf-8") as f:
            summary = f.read()

        return {
            "status": "cached",
            "video_id": video_id,
            "summary": summary
        }

    # ❌ CACHE MISS → enqueue job in Redis
    import uuid
    task_id = str(uuid.uuid4())

    redis_conn.hset(task_id, "status", "queued")
    queue.enqueue(run_ingestion, task_id, req.youtube_url, job_timeout=600)

    return {
        "status": "processing",
        "task_id": task_id
    }


@router.get("/summary")
def get_latest_summary():
    try:
        with open("data/vector_store/latest.txt", "r") as f:
            video_id = f.read().strip()

        with open(f"data/summaries/{video_id}.txt", "r", encoding="utf-8") as f:
            summary = f.read()

        return {"summary": summary}

    except Exception as e:
        return {"summary": ""}


@router.get("/eta/{task_id}")
def get_eta(task_id: str):
    status = redis_conn.hget(task_id, "status")
    duration = redis_conn.hget(task_id, "video_duration")

    if not status or not duration:
        return {"eta_seconds": None}

    status = status.decode() if isinstance(status, bytes) else status
    video_duration = float(duration)

    eta = estimate_eta(video_duration, status)

    return {"eta_seconds": eta}

