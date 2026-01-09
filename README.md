# YouTube Video Summarizer & Q&A

A powerful tool that downloads YouTube videos, transcribes the audio, generates concise summaries, and allows you to ask questions about the video content using RAG (Retrieval-Augmented Generation).

## 🚀 Features

- **Video Ingestion**: Downloads audio from YouTube videos.
- **Smart Transcription**: Uses **OpenAI Whisper** for accurate speech-to-text conversion.
- **Summarization**: Generates a quick summary of the entire video.
- **Interactive Q&A**: Chat with the video! Ask specific questions and get answers based on the video content.
- **Vector Search**: Uses **FAISS** for efficient similarity search and retrieval.

## 🛠️ Tech Stack

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **LLM / Inference**: Groq API
- **Transcription**: OpenAI Whisper
- **Vector DB**: FAISS
- **Embeddings**: Sentence Transformers (`sentence-transformers`)
- **Video Processing**: `yt-dlp`, `ffmpeg-python`

## 📋 Prerequisites

- Python 3.8+
- [FFmpeg](https://ffmpeg.org/download.html) installed and added to your system PATH.
- A **Groq API Key**.

## ⚙️ Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd video-summarizer
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Mac/Linux
    source .venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment**:
    Create a `.env` file in the root directory and add your Groq API key:
    ```env
    GROQ_API_KEY=your_groq_api_key_here
    ```

## 🏃‍♂️ Running the Application

This application consists of a backend API and a Streamlit frontend. You need to run both terminals.

### 1. Start the Backend API
In your first terminal, run:
```bash
uvicorn app.main:app --reload
```
The API will start at `http://127.0.0.1:8000`.

### 2. Start the Frontend UI
In a second terminal, run:
```bash
streamlit run frontend/streamlit_app.py
```
The app will open in your browser at `http://localhost:8501`.

## 🎮 Usage

1.  Paste a **YouTube URL** into the input field.
2.  Click **"Process Video"**.
    - The app will download, transcribe, embed, and summarize the video.
    - Status updates will be shown in real-time.
3.  Once completed:
    - Read the **Summary**.
    - Use the **Chat Interface** to ask questions (e.g., "What was the main conclusion?", "Who is the speaker?").

## 📂 Project Structure

```
├── app/
│   ├── api/            # API Routes
│   ├── db/             # Vector Database Logic
│   ├── rag/            # RAG & Chunking Logic
│   ├── services/       # Core Services (YouTube, STT, Summary)
│   └── main.py         # FastAPI Entry Point
├── data/               # Stored data (videos, transcripts, indices)
├── frontend/           # Streamlit App
├── scripts/            # Helper scripts
├── .env                # Environment Variables
├── requirements.txt    # Python Dependencies
└── README.md           # Documentation
```
