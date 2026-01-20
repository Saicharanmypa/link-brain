# Link Brain 🧠

Link Brain is a local-first AI tool that converts YouTube links into
concise, structured insights using a local LLM.

No cloud APIs. No data leaves your machine.

---

## Features
- YouTube transcript extraction (auto-captions)
- Caption cleaning and validation
- Structured summaries:
  - TL;DR
  - Key ideas
  - Why this matters
- Local LLM inference using Ollama
- SQLite-based local memory

---

## Requirements
- Python 3.10+
- Ollama installed
- A local LLM model (Qwen3 recommended)

---

## Setup

Clone the repository and install Python dependencies:

```bash
git clone https://github.com/YOUR_USERNAME/link-brain.git
cd link-brain
pip install -r requirements.txt


Install Ollama from:
https://ollama.com


Pull a model:

```bash
ollama pull qwen3:4b
