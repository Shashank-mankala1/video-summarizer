
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.youtube_service import YouTubeService
from app.services.stt_service import SpeechToTextService
from app.rag.chunking import TranscriptChunker
from app.services.embedding_service import EmbeddingService
from app.services.summary_service import SummaryService
from app.db.vector_db import VectorDB
from app.utils.redis_conn import redis_conn
import time

def run_ingestion(task_id: str, youtube_url: str):
    print("WORKER RUNNING", task_id)
    try:
        ingestion_start = time.time()
        video_id = youtube_url.split("v=")[-1]

        def update(status: str):
            redis_conn.hset(task_id, "status", status)
            redis_conn.hset(task_id, f"ts_{status}", time.time())

        yt_service = YouTubeService(output_dir="data/raw_videos")
        stt_service = SpeechToTextService()
        chunker = TranscriptChunker()
        embedder = EmbeddingService()
        summary_service = SummaryService()

        update("downloading_audio")
        audio_file = yt_service.download_audio(youtube_url)
        video_duration = stt_service._get_audio_duration(audio_file)
        redis_conn.hset(task_id, "video_duration", video_duration)
    
        print(f"[DEBUG] Video duration: {video_duration:.2f} seconds")


        transcription_start = time.time()
        # print("[DEBUG] Transcription started")
        update("transcribing")
        transcript_path = stt_service.transcribe(
            audio_file, "data/transcripts"
        )

        transcription_end = time.time()
        print(f"[DEBUG] Transcription completed in {transcription_end - transcription_start:.2f} seconds")

        chunking_start = time.time()
        update("chunking")
        chunks = chunker.chunk_transcript(transcript_path)

        chunking_end = time.time()
        print(f"[DEBUG] Chunking completed in {chunking_end - chunking_start:.2f} seconds")

        embedding_start = time.time()
        update("embedding")
        texts = [c["text"] for c in chunks]
        embeddings = embedder.embed_texts(texts)

        embedding_end = time.time()
        print(f"[DEBUG] Embedding completed in {embedding_end - embedding_start:.2f} seconds")

        summarizing_start = time.time()
        update("summarizing")
        summary = summary_service.generate_summary(chunks)

        summarizing_end = time.time()
        print(f"[DEBUG] Summarizing completed in {summarizing_end - summarizing_start:.2f} seconds")

        saving_start = time.time()
        update("saving")
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

        os.makedirs("data/summaries", exist_ok=True)
        with open(f"data/summaries/{video_id}.txt", "w", encoding="utf-8") as f:
            f.write(summary)

        with open("data/vector_store/latest.txt", "w") as f:
            f.write(video_id)

        update("completed")

        saving_end = time.time()
        print(f"[DEBUG] Saving completed in {saving_end - saving_start:.2f} seconds")

        ingestion_end = time.time()
        print(f"[DEBUG] Ingestion completed in {ingestion_end - ingestion_start:.2f} seconds")

    except Exception as e:
        redis_conn.hset(task_id, "status", f"error:{str(e)}")
