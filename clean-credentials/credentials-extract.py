#!/usr/bin/env python3
"""Parse a plain-text credentials file into a structured CSV."""

import csv
import re
import sys

import settings


def infer_category(service_name: str) -> str:
    """Auto-detect category based on keywords in the service name."""
    s_lower = service_name.lower()
    for cat, keywords in settings.CATEGORY_RULES.items():
        if any(kw in s_lower for kw in keywords):
            return cat
    return "General / Misc"


def expand_handle(val: str) -> str:
    if not val:
        return ""
    val_clean = val.strip()
    return settings.EMAIL_MAP.get(val_clean.lower(), val_clean)


def is_url(val: str) -> bool:
    val_lower = val.lower().strip()
    return (
        val_lower.startswith("http://")
        or val_lower.startswith("https://")
        or val_lower.startswith("www.")
        or any(ext in val_lower for ext in [".com", ".in", ".org", ".net", ".io", ".co"])
    )


def parse_line(line: str, current_category: str):
    line = line.strip()

    if not line:
        return None, ""

    if ">>" in line:
        new_cat = line.split(">>")[0].strip()
        return None, new_cat

    tokens = [t.strip() for t in re.split(r"[,|]|\s+-\s+", line) if t.strip()]
    if not tokens:
        return None, current_category

    service = tokens[0]
    remaining = tokens[1:]

    username = ""
    email = ""
    password = ""
    url = ""
    notes = []

    for tok in remaining:
        tok_exp = expand_handle(tok)

        if not email and ("@" in tok_exp or tok.lower() in settings.EMAIL_MAP):
            email = tok_exp
        elif not url and is_url(tok):
            url = tok
        elif not password and not username and not email:
            username = tok
        elif not password:
            password = tok
        else:
            notes.append(tok)

    if "@" in username or username.lower() in settings.EMAIL_MAP:
        if not email:
            email = expand_handle(username)
            username = ""

    final_category = current_category if current_category else infer_category(service)

    record = {
        "category": final_category,
        "service": service,
        "username": expand_handle(username),
        "email": expand_handle(email),
        "password": password,
        "url": url,
        "notes": ", ".join(notes) if notes else "",
    }

    return record, current_category


def main() -> None:
    settings.INPUT_DIR.mkdir(parents=True, exist_ok=True)
    settings.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    input_file = settings.INPUT_FILE
    output_file = settings.OUTPUT_FILE

    if not input_file.is_file():
        print(f"Input file not found: {input_file}", file=sys.stderr)
        print(f"Place your credentials file in: {settings.INPUT_DIR}/", file=sys.stderr)
        sys.exit(1)

    rows = []
    skipped = 0
    active_category = ""

    with open(input_file, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            record, active_category = parse_line(line, active_category)
            if record and (record["service"] or record["password"] or record["email"]):
                rows.append(record)
            elif line.strip() and ">>" not in line:
                print(f"Skipped line {line_num}: {line.strip()}")
                skipped += 1

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "category",
            "service",
            "username",
            "email",
            "password",
            "url",
            "notes",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(
        f"Done! Processed {len(rows)} entries into {output_file} "
        f"(Skipped lines: {skipped})."
    )
    print(f"Move sensitive output out of {settings.OUTPUT_DIR}/ when finished.")


if __name__ == "__main__":
    main()
