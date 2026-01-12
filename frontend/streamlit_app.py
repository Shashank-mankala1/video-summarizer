import streamlit as st
import requests
import time
import os
from dotenv import load_dotenv
load_dotenv()

if "ready" not in st.session_state:
    st.session_state.ready = False

if "processing" not in st.session_state:
    st.session_state.processing = False

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "task_id" not in st.session_state:
    st.session_state.task_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

def format_eta(seconds: int) -> str:
    if seconds is None:
        return ""
    if seconds < 60:
        return f"{seconds} seconds"
    return f"{seconds // 60 + 1} minutes"

API_BASE_URL=os.getenv("API_BASE_URL", "http://api:8000")
INGEST_URL = f"{API_BASE_URL}/video/ingest"
QA_URL = f"{API_BASE_URL}/qa/ask"

st.set_page_config(page_title="YouTube Video Summarizer & Q&A")

st.title("YouTube Video Summarizer & Q&A")

youtube_link = st.text_input("Paste YouTube video link")

PROGRESS_MAP = {
    "downloading_audio": 10,
    "transcribing": 35,
    "chunking": 50,
    "embedding": 70,
    "summarizing": 85,
    "saving": 95,
    "completed": 100
}

if st.button("Process Video"):
    res = requests.post(INGEST_URL, json={"youtube_url": youtube_link}).json()
    if res.get("status") == "cached":
        st.success("Video already processed. Loaded from cache.")
        st.session_state.summary = res.get("summary", "")
        st.session_state.ready = True
        st.session_state.processing = False
        st.session_state.task_id = None

    # CACHE MISS → background processing
    else:
        st.session_state.task_id = res["task_id"]
        st.session_state.processing = True
        st.session_state.ready = False

if st.session_state.get("processing"):
    progress_bar = st.progress(0)
    status_text = st.empty()
    eta_box = st.empty()
    eta_box.info(f"Estimated time remaining: ...")
    while True:
        res = requests.get(
            f"{API_BASE_URL}/video/status/{st.session_state.task_id}"
        ).json()

        eta_res = requests.get(f"{API_BASE_URL}/video/eta/{st.session_state.task_id}").json()
        eta = eta_res.get("eta_seconds")

        if eta:
            eta_box.info(f"Estimated time remaining: ~{format_eta(eta)}")

        status = res["status"]

        if status.startswith("error"):
            st.error(status)
            break

        progress = PROGRESS_MAP.get(status, 0)
        progress_bar.progress(progress)
        status_text.text(f"Processing: {status.replace('_', ' ').title()}")

        if status == "completed":
            eta_box.empty()
            st.success("Video processed successfully!")
            st.session_state.processing = False
            st.session_state.ready = True
            # st.session_state.summary = res.get("summary")
            summary_res = requests.get(
                f"{API_BASE_URL}/video/summary"
            ).json()

            st.session_state.summary = summary_res.get("summary", "")
            break

        time.sleep(1)


if "messages" not in st.session_state:
    st.session_state.messages = []

if st.session_state.get("ready"):
    # st.divider()
    st.subheader("Video Summary")
    st.markdown(st.session_state.summary)
    st.divider()
    st.subheader("Ask questions about the video")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    question = st.chat_input("Ask a question", key="qa")

    if question:
        # 1️⃣ Show user question immediately
        with st.chat_message("user"):
            st.markdown(question)

        st.session_state.messages.append(
            {"role": "user", "content": question}
        )

        # 2️⃣ Show assistant response immediately
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = requests.post(
                    QA_URL,
                    json={"question": question}
                ).json()

                answer = response["answer"]
                st.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

