import subprocess
import tempfile
import os
import re


def extract_youtube_text(url: str) -> str:
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "subs")

        command = [
            "yt-dlp",
            "--write-auto-sub",
            "--skip-download",
            "--sub-lang", "en",
            "--sub-format", "vtt",
            "-o", output_path,
            url
        ]

        subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        for filename in os.listdir(tmpdir):
            if filename.endswith(".vtt"):
                file_path = os.path.join(tmpdir, filename)

                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                cleaned_lines = []

                for line in lines:
                    line = line.strip()

                    if not line:
                        continue
                    if "-->" in line:
                        continue
                    if line.isdigit():
                        continue

                    # remove VTT tags like <c> and timestamps
                    line = re.sub(r"<.*?>", "", line)
                    cleaned_lines.append(line)

                text = " ".join(cleaned_lines)
                text = re.sub(r"\s+", " ", text).strip()

                return text

    return ""


def validate_text(text: str, min_length: int = 500) -> bool:
    if not text:
        return False
    if len(text) < min_length:
        return False
    return True    