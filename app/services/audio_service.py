import ffmpeg
import os

class AudioService:
    def extract_audio(self, input_file: str) -> str:
        output_file = input_file.rsplit(".", 1)[0] + ".mp3"

        (
            ffmpeg
            .input(input_file)
            .output(output_file, format="mp3", acodec="libmp3lame")
            .overwrite_output()
            .run(quiet=True)
        )

        return output_file
