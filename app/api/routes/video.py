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

router = APIRouter()

class VideoRequest(BaseModel):
    youtube_url: str

def run_ingestion(task_id: str, youtube_url: str, ):
    try:
        video_id = youtube_url.split("v=")[-1]

        yt_service = YouTubeService(output_dir="data/raw_videos")
        stt_service = SpeechToTextService()
        chunker = TranscriptChunker()
        embedder = EmbeddingService()
        summary_service = SummaryService()

        task_status[task_id] = "downloading_audio"
        audio_file = yt_service.download_audio(youtube_url)

        task_status[task_id] = "transcribing"
        transcript_path = stt_service.transcribe(audio_file, "data/transcripts")

        task_status[task_id] = "chunking"
        chunks = chunker.chunk_transcript(transcript_path)

        task_status[task_id] = "embedding"
        texts = [c["text"] for c in chunks]
        embeddings = embedder.embed_texts(texts)

        task_status[task_id] = "summarizing"
        summary = summary_service.generate_summary(chunks)

        task_status[task_id] = "saving"
        # save vector DB + summary
        # Save FAISS index
        index_path = f"data/vector_store/{video_id}.index"
        vector_db = VectorDB(dim=len(embeddings[0]), index_path=index_path)

        metadata = [
            {
                "text": c["text"],
                "start_time": c["start_time"],
                "end_time": c["end_time"]
            }
            for c in chunks
        ]

        vector_db.add(embeddings, metadata)
        vector_db.save()

        # Save summary
        os.makedirs("data/summaries", exist_ok=True)
        with open(f"data/summaries/{video_id}.txt", "w", encoding="utf-8") as f:
            f.write(summary)

        # Update latest video pointer
        with open("data/vector_store/latest.txt", "w") as f:
            f.write(video_id)

        task_status[task_id] = "completed"

    except Exception as e:
        task_status[task_id] = f"error:{str(e)}"

# @router.post("/ingest")
# def ingest_video(req: VideoRequest, background_tasks: BackgroundTasks):
#     task_id = str(uuid.uuid4())
#     task_status[task_id] = "started"

#     background_tasks.add_task(run_ingestion, task_id, req.youtube_url)

#     return {
#         "task_id": task_id
#     }
@router.get("/status/{task_id}")
def get_status(task_id: str):
    return {
        "status": task_status.get(task_id, "unknown")
    }



@router.post("/ingest")
def ingest_video(req: VideoRequest, background_tasks: BackgroundTasks):
    # video_id = req.youtube_url.split("v=")[-1]

    # yt_service = YouTubeService(output_dir="data/raw_videos")
    # stt_service = SpeechToTextService()
    # chunker = TranscriptChunker()
    # embedder = EmbeddingService()
    # summary_service = SummaryService()

    task_id = str(uuid.uuid4())
    task_status[task_id] = "started"

    background_tasks.add_task(run_ingestion, task_id, req.youtube_url)

    return {
        "task_id": task_id
    }
    # # 1. Download audio
    # audio_file = yt_service.download_audio(req.youtube_url)

    # # 2. Transcribe
    # transcript_path = stt_service.transcribe(
    #     audio_path=audio_file,
    #     output_dir="data/transcripts"
    # )

    # # 3. Chunk
    # chunks = chunker.chunk_transcript(transcript_path)
    # summary_service = SummaryService()
    # summary = summary_service.generate_summary(chunks)

    # # 4. Embed
    # texts = [c["text"] for c in chunks]
    # embeddings = embedder.embed_texts(texts)

    # # 5. Store in FAISS
    # index_path = f"data/vector_store/{video_id}.index"
    # vector_db = VectorDB(dim=len(embeddings[0]), index_path=index_path)

    # metadata = [
    #     {
    #         "text": c["text"],
    #         "start_time": c["start_time"],
    #         "end_time": c["end_time"]
    #     }
    #     for c in chunks
    # ]

    # vector_db.add(embeddings, metadata)
    # vector_db.save()

    # # ✅ WRITE THIS HERE (VERY IMPORTANT)
    # with open("data/vector_store/latest.txt", "w") as f:
    #     f.write(video_id)

    # return {
    #     "status": "success",
    #     "video_id": video_id,
    #     "summary": summary
    # }
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
