def parse_summary(text: str):
    sections = {
        "tldr": "",
        "key_ideas": "",
        "why_it_matters": ""
    }

    current = None
    lines = text.splitlines()

    for line in lines:
        line = line.strip()

        if line.lower().startswith("tl;dr"):
            current = "tldr"
            continue
        elif line.lower().startswith("key ideas"):
            current = "key_ideas"
            continue
        elif line.lower().startswith("why this matters"):
            current = "why_it_matters"
            continue

        if current and line:
            sections[current] += line + "\n"

    return (
        sections["tldr"].strip(),
        sections["key_ideas"].strip(),
        sections["why_it_matters"].strip()
    )