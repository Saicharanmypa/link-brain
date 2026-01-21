import argparse
from ingest import detect_link
from extract import extract_youtube_text, validate_text
from summarize import summarize_text
from parse import parse_summary
from store import init_db, save_summary

def main():
    parser = argparse.ArgumentParser(description="Link Brain: YouTube summarizer")
    parser.add_argument("--url", type=str, help="YouTube URL to summarize")
    parser.add_argument("--no-save", action="store_true", help="Do not save to database")
    args = parser.parse_args()

    if not args.url:
        print("❌ Error: --url is required")
        return

    init_db()

    url = args.url
    source_type = detect_link(url)

    if source_type != "youtube":
        print("❌ Unsupported URL. Only YouTube links are allowed.")
        return

    text = extract_youtube_text(url)

    if not validate_text(text):
        print("❌ No usable captions found. Try a video with English subtitles.")
        return

    summary = summarize_text(text)
    tldr, key_ideas, why_it_matters = parse_summary(summary)

    if not args.no_save:
        save_summary(url, source_type, tldr, key_ideas, why_it_matters)

    print("\n===== SUMMARY =====\n")
    print("\n" + "="*30)
print(" LINK BRAIN SUMMARY ")
print("="*30 + "\n")
print(summary)
print("\n" + "="*30)

if __name__ == "__main__":
    main()