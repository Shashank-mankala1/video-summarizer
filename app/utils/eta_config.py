STAGE_ORDER = [
    "queued",
    "downloading_audio",
    "transcribing",
    "chunking",
    "embedding",
    "summarizing",
    "saving",
    "completed"
]

# Average seconds per stage (rough, conservative)
STAGE_AVG_TIME = {
    "queued": 2,
    "downloading_audio": 15,
    "transcribing": 180,
    "chunking": 5,
    "embedding": 20,
    "summarizing": 30,
    "saving": 5
}
