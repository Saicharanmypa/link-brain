import subprocess

MODEL_NAME = "qwen3:4b"  # change if needed

SYSTEM_PROMPT = (
    "You are an analytical assistant. "
    "Be precise. Avoid filler. No emojis. No fluff."
)

USER_TEMPLATE = """
CONTENT:
{text}

TASKS:
1) Produce exactly 5 TL;DR bullets (max 12 words each).
2) Extract 3–5 key ideas.
3) Explain why this matters in 80–120 words.

FORMAT:
TL;DR:
- ...
- ...
- ...
- ...
- ...

Key Ideas:
- ...
- ...
- ...

Why This Matters:
...
"""


def summarize_text(text: str) -> str:
    prompt = SYSTEM_PROMPT + "\n" + USER_TEMPLATE.format(text=text)

    result = subprocess.run(
        ["ollama", "run", MODEL_NAME],
        input=prompt,
        text=True,
        encoding="utf-8",          # 🔑 force UTF-8
        errors="ignore",           # 🔑 drop garbage chars safely
        capture_output=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return result.stdout.strip()