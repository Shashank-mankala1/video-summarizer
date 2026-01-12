# YouTube Video Summarizer with Interactive Q&A

## Project Overview

This project is an end-to-end Generative AI application that takes a YouTube video as input, generates structured summaries, and allows users to ask questions to clarify doubts based strictly on the video content.

The system converts video to text, stores semantic representations of the transcript, and uses a Retrieval-Augmented Generation (RAG) pipeline to provide accurate, context-grounded answers.

## Key Features

- Accepts YouTube video links as input
- Automatically transcribes video audio into text
- Generates structured summaries:
  - TL;DR
  - Bullet point summary
  - Key takeaways
- Supports interactive question answering over video content
- Prevents hallucinations using RAG
- Answers are grounded only in video transcript
- Supports follow-up questions with chat memory
- (Optional) Timestamp-based citations

## Problem Statement

Long YouTube videos make it difficult to:
- Quickly understand key ideas
- Revisit specific explanations
- Clarify doubts without rewatching the entire video

This project solves the problem by:
- Condensing video content into readable summaries
- Allowing users to ask natural language questions
- Returning accurate answers using retrieved transcript context

## System Architecture (High Level)

1. User submits YouTube video URL
2. Audio is extracted from the video
3. Speech-to-Text converts audio to transcript
4. Transcript is cleaned and chunked
5. Text chunks are converted into embeddings
6. Embeddings are stored in a vector database
7. Summary is generated using an LLM
8. User asks questions
9. Relevant transcript chunks are retrieved
10. LLM generates answers using retrieved context

## Tech Stack

### Backend
- Python
- FastAPI

### AI / NLP
- **Speech to Text:** Whisper or Faster Whisper
- **Large Language Model:** GPT or open-source LLM
- **Embeddings:** OpenAI or Sentence Transformers
- **RAG Framework:** LangChain or LlamaIndex

### Vector Database
- FAISS (local)
- ChromaDB (persistent)

### Frontend
- Streamlit (initial)
- React or Next.js (future upgrade)

## Core Concepts Used

- Retrieval-Augmented Generation (RAG)
- Vector embeddings
- Semantic search
- Prompt engineering
- Chunk-based summarization
- Context-grounded question answering
- Multimodal AI (video to text to reasoning)

## Summarization Strategy

The system uses a multi-stage summarization pipeline:
1. Split transcript into manageable chunks
2. Generate summaries for each chunk
3. Combine chunk summaries into section summaries
4. Generate a final high-level summary

**Supported summary formats:**
- TL;DR
- Bullet points
- Key takeaways
- Chapter-wise summaries (optional)

## Question Answering Strategy

1. User question is converted into an embedding
2. Relevant transcript chunks are retrieved from vector DB
3. Retrieved content is passed to the LLM
4. LLM generates an answer strictly using retrieved context

**This ensures:**
- Reduced hallucinations
- High answer accuracy
- Faithful responses to video content

## Data Flow

`YouTube Video` → `Audio Extraction` → `Speech to Text` → `Transcript` → `Chunking` → `Embeddings` → `Vector Database` → `RAG Pipeline` → `Summary and Q&A`

## Evaluation Metrics

- Retrieval relevance score
- Answer faithfulness to transcript
- Latency per query
- Token usage
- User satisfaction

## Project Phases

### Phase 1: Video Processing
- Extract audio
- Generate transcript

### Phase 2: Summarization
- Chunk-based summarization
- Final summary generation

### Phase 3: RAG Q&A
- Embedding generation
- Vector DB integration
- Question answering pipeline

### Phase 4: UI and Deployment
- User interface
- API integration
- Deployment

## Future Enhancements

- Timestamp-based citations
- Multi-language support
- Quiz generation from video
- PDF summary export
- Cross-video question answering
- Knowledge graph extraction

## Why This Project Matters

This project demonstrates:
- Practical application of GenAI
- Real-world RAG implementation
- Scalable AI system design
- Strong understanding of LLM limitations and solutions

**It is suitable for:**
- Data Scientist roles
- ML Engineer roles
- AI Engineer roles
- GenAI-focused positions

## Author

**Shashank Mankala**<br>
[LinkedIn](https://www.linkedin.com/in/shashankmankala/) | [GitHub](https://github.com/Shashank-mankala1)

```
youtube-video-summarizer/
│
├── README.md
├── requirements.txt
├── .env
├── .gitignore
│
├── data/
│   ├── raw_videos/              # Downloaded video or audio files
│   ├── transcripts/             # Generated transcripts (txt / json)
│   ├── summaries/               # Saved summaries per video
│   └── vector_store/            # Persisted vector database
│
├── app/
│   ├── main.py                  # FastAPI entry point
│   ├── config.py                # App level configuration
│   │
│   ├── api/
│   │   ├── routes/
│   │   │   ├── video.py         # Video upload / YouTube link APIs
│   │   │   ├── summary.py       # Summarization endpoints
│   │   │   └── qa.py            # Question answering endpoints
│   │   └── schemas.py           # Request / response models
│   │
│   ├── services/
│   │   ├── youtube_service.py   # YouTube download logic
│   │   ├── audio_service.py     # Audio extraction (ffmpeg)
│   │   ├── stt_service.py       # Speech to Text (Whisper)
│   │   ├── summarizer.py        # Chunk + final summarization
│   │   ├── embedding_service.py # Embedding generation
│   │   ├── retriever.py         # Vector DB retrieval logic
│   │   └── qa_service.py        # RAG based question answering
│   │
│   ├── rag/
│   │   ├── chunking.py          # Transcript chunking logic
│   │   ├── prompts.py           # Prompt templates
│   │   └── pipeline.py          # RAG orchestration
│   │
│   ├── db/
│   │   ├── vector_db.py         # FAISS / Chroma setup
│   │   └── metadata_store.py    # Video metadata storage
│   │
│   ├── utils/
│   │   ├── logger.py            # Logging
│   │   ├── helpers.py           # Common helper functions
│   │   └── constants.py         # Static constants
│   │
│   └── tests/
│       ├── test_transcript.py
│       ├── test_summary.py
│       └── test_qa.py
│
├── frontend/
│   ├── streamlit_app.py         # UI for users
│   └── components/
│       ├── sidebar.py
│       ├── chat_ui.py
│       └── summary_view.py
│
├── scripts/
│   ├── ingest_video.py          # CLI ingestion
│   ├── build_vector_store.py    # Pre compute embeddings
│   └── evaluate_rag.py          # Evaluation scripts
│
└── deployment/
    ├── Dockerfile
    ├── docker-compose.yml
    └── README.md
```
```
queued
↓
downloading_audio
↓
transcribing
↓
chunking
↓
embedding
↓
summarizing
↓
saving
↓
completed

```

Planned Improvements:

1. Video Ingestion Layer (VERY HIGH IMPACT)
  A. Video-Level Caching ⭐⭐⭐⭐⭐

  What: Skip entire pipeline if video already processed

  Where: /video/ingest

  How: Check existence of:

  vector_store/{video_id}.index

  summaries/{video_id}.txt

  B. Background Job Queue (Advanced)
  What: Use Redis + Celery or RQ

  Where: Replace FastAPI BackgroundTasks

2. Transcription Layer
  A. Chunked Audio Transcription (Advanced)

  What: Transcribe in segments concurrently

  Impact: Faster for long videos

3. Retrieval & Q&A Layer (HIGH QUALITY IMPACT)
  Current State: Top K retrieval, Single question context

  Improvements
  A. Re-Ranking ⭐⭐⭐⭐

  What: Retrieve top 10

  How: Re-rank top 3 with cross-encoder

  Impact: Better answers, Fewer "I do not know"

  B. Chat-Aware Retrieval ⭐⭐⭐⭐

  What: Include previous question context

  Impact: Better follow-up answers, Natural conversation


4. UX & Product Efficiency
A. ETA Prediction ⭐⭐⭐

  What: Show estimated remaining time

B. Summary Streaming ⭐⭐⭐⭐

  What: Stream summary generation

  Instead of waiting for full summary, show chunks as they are generated[write word by word ]