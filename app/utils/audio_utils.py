import os
import subprocess


def split_audio(
    audio_path: str,
    chunk_duration_sec: int = 60,
    overlap_sec: int = 3,
    output_dir: str = "data/audio_chunks"
):
    os.makedirs(output_dir, exist_ok=True)

    chunks = []
    index = 0
    start_time = 0.0

    # Get audio duration using ffprobe
    cmd_duration = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path
    ]

    duration = float(
        subprocess.check_output(cmd_duration).decode().strip()
    )

    while start_time < duration:
        chunk_path = os.path.join(output_dir, f"chunk_{index}.wav")

        cmd_split = [
            "ffmpeg", "-y",
            "-ss", str(start_time),
            "-t", str(chunk_duration_sec),
            "-i", audio_path,
            "-af", "silenceremove=start_periods=1:start_silence=0.5:start_threshold=-50dB",
            "-ac", "1",
            "-ar", "16000",
            "-vn",
            "-f", "wav",
            chunk_path
        ]



        subprocess.run(cmd_split, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        chunks.append({
            "path": chunk_path,
            "start_time": start_time
        })

        start_time += (chunk_duration_sec - overlap_sec)
        index += 1

    return chunks
