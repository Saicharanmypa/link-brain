from ingest import detect_link
from extract import extract_youtube_text, validate_text
from summarize import summarize_text
from parse import parse_summary
from store import init_db, save_summary

init_db()

url = input("Drop the link: ")
source_type = detect_link(url)

print(f"Detected source type: {source_type}")

if source_type == "youtube":
    text = extract_youtube_text(url)

    if not validate_text(text):
        print("❌ Rejected: Low-quality or too-short transcript")
    else:
        print(f"✅ Accepted transcript ({len(text)} chars)")
        summary = summarize_text(text)

        tldr, key_ideas, why_it_matters = parse_summary(summary)

        save_summary(
            url=url,
            source_type=source_type,
            tldr=tldr,
            key_ideas=key_ideas,
            why_it_matters=why_it_matters
        )

        print("\n=== SAVED SUMMARY ===\n")
        print(summary)

else:
    print("Article extraction not implemented yet.")