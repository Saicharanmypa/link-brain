import html
import concurrent.futures
import os

IS_CLOUD = os.getenv("RENDER") == "true"


from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

from ingest import detect_link
from extract import extract_youtube_text, validate_text
from summarize import summarize_text
from parse import parse_summary
from store import init_db, save_summary
from chunk import chunk_text

app = FastAPI()
init_db()


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
      <head>
        <title>Link Brain</title>
        <script>
          function onSubmit() {
            const btn = document.getElementById("submitBtn");
            btn.disabled = true;
            btn.innerText = "Summarizing…";
            document.getElementById("status").innerText = "Working… please wait.";
            return true;
          }
        </script>
      </head>
      <body>
        <h2>Link Brain 🧠</h2>
        <form method="post" onsubmit="return onSubmit();">
          <input type="text" name="url" placeholder="Paste YouTube URL" size="60" required />
          <br><br>
          <button id="submitBtn" type="submit">Summarize</button>
        </form>
        <p id="status"></p>
      </body>
    </html>
    """


@app.post("/", response_class=HTMLResponse)
def summarize(url: str = Form(...)):
    try:
        source_type = detect_link(url)
        if source_type != "youtube":
            return "<p>❌ Only YouTube links are supported.</p>"

        text = extract_youtube_text(url)
        if not validate_text(text):
            return "<p>❌ No usable captions found. Try a video with subtitles.</p>"
        if IS_CLOUD:
            return "<p>⚠️ LLM disabled in cloud demo. Run locally for full functionality.</p>"

        # 🔹 CHUNK TRANSCRIPT
        chunks = chunk_text(text)
        partial_summaries = []

        # 🔹 SUMMARIZE EACH CHUNK WITH TIMEOUT
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for chunk in chunks:
                future = executor.submit(summarize_text, chunk)
                try:
                    part = future.result(timeout=120)
                    partial_summaries.append(part)
                except concurrent.futures.TimeoutError:
                    return "<p>❌ Took too long while processing chunks.</p>"

        # 🔹 FINAL SUMMARY OF SUMMARIES
        combined = "\n".join(partial_summaries)
        summary = summarize_text(combined)

        tldr, key_ideas, why_it_matters = parse_summary(summary)
        save_summary(url, source_type, tldr, key_ideas, why_it_matters)

        safe_summary = html.escape(summary)

        return f"""
        <html>
          <body>
            <h2>Summary</h2>
            <pre>{safe_summary}</pre>
            <br>
            <a href="/">Go back</a>
          </body>
        </html>
        """

    except Exception as e:
        print(e)
        return "<p>❌ Unexpected error. Check server logs.</p>"