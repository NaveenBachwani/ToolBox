#!/usr/bin/env python3
"""Interactive migration checker for two recursively scanned folders."""

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from difflib import SequenceMatcher
from hashlib import sha256
from pathlib import Path
import re
from zoneinfo import ZoneInfo

import settings


@dataclass(frozen=True)
class FileRecord:
    relative_path: Path
    size: int
    digest: str


def normalize_markdown(file_contents: bytes) -> bytes:
    """Ignore common Markdown migration metadata and harmless blank lines."""
    normalized = file_contents.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    if normalized.startswith(b"---\n"):
        metadata_end = normalized.find(b"\n---\n", len(b"---\n"))
        if metadata_end != -1:
            normalized = normalized[metadata_end + len(b"\n---\n") :]
            if normalized.startswith(b"\n"):
                normalized = normalized[1:]
    if normalized:
        normalized = normalized.rstrip(b"\n") + b"\n"
    return normalized


def hash_file(path: Path) -> str:
    file_contents = path.read_bytes()
    if path.suffix.lower() == ".md":
        file_contents = normalize_markdown(file_contents)
    return sha256(file_contents).hexdigest()


def scan_folder(folder: Path) -> tuple[dict[Path, FileRecord], list[str]]:
    records: dict[Path, FileRecord] = {}
    errors: list[str] = []
    for path in sorted(folder.rglob("*")):
        if not path.is_file():
            continue
        relative_path = path.relative_to(folder)
        try:
            records[relative_path] = FileRecord(relative_path, path.stat().st_size, hash_file(path))
        except OSError as error:
            errors.append(f"{relative_path}: {error}")
    return records, errors


def display_path(folder: Path, relative_path: Path) -> str:
    return str(folder / relative_path)


def normalize_filename(path: Path) -> str:
    """Create a comparison-friendly basename without changing the real filename."""
    name = path.stem.casefold()
    name = re.sub(r"[_-]+", " ", name)
    name = re.sub(r"[^\w\s]", " ", name, flags=re.UNICODE)
    return " ".join(name.split())


def filename_similarity(a_path: Path, b_path: Path) -> float:
    return SequenceMatcher(None, normalize_filename(a_path), normalize_filename(b_path)).ratio()


def add_section(output: list[str], title: str, lines: list[str]) -> None:
    output.extend((f"\n{title} ({len(lines)})", "-" * (len(title) + len(str(len(lines))) + 3)))
    output.extend(lines or ["None"])


def prompt_for_folder(label: str, default: Path) -> Path:
    default_display = default if str(default) else "(none — enter a path)"
    entered_path = input(f"{label} folder [{default_display}]: ").strip()
    if entered_path:
        return Path(entered_path).expanduser()
    if not str(default):
        raise SystemExit(f"{label} folder is required.")
    return default


def choose_mode() -> int:
    threshold = settings.FUZZY_FILENAME_THRESHOLD
    print("\nChoose a comparison mode:")
    print("1. Exact filename match")
    print("2. Normalized filename match")
    print(f"3. Fuzzy filename match (threshold {threshold:.0%})")
    print("4. All filename comparisons")
    print("5. Content match via SHA-256 hash")
    while True:
        choice = input("Enter 1-5: ").strip()
        if choice in {"1", "2", "3", "4", "5"}:
            return int(choice)
        print("Please enter a number from 1 to 5.")


def content_matches(a_record: FileRecord, b_record: FileRecord) -> str:
    return "CONTENT MATCH" if a_record.digest == b_record.digest else "content differs"


def filename_report(
    mode: int,
    a_folder: Path,
    b_folder: Path,
    a_records: dict[Path, FileRecord],
    b_records: dict[Path, FileRecord],
) -> list[str]:
    lines: list[str] = []
    used_b: set[Path] = set()
    threshold = settings.FUZZY_FILENAME_THRESHOLD
    for a_path in sorted(a_records):
        candidates: list[tuple[float, Path]] = []
        for b_path in sorted(b_records):
            exact = a_path.name == b_path.name
            normalized = normalize_filename(a_path) == normalize_filename(b_path)
            similarity = filename_similarity(a_path, b_path)
            include = (
                (mode == 1 and exact)
                or (mode == 2 and normalized)
                or (mode == 3 and similarity >= threshold)
                or mode == 4
            )
            if include:
                candidates.append((similarity, b_path))

        candidates.sort(key=lambda item: (-item[0], str(item[1])))
        if not candidates:
            lines.append(f"A: {display_path(a_folder, a_path)}\nB: NO FILENAME CANDIDATE")
            continue

        selected_candidates = candidates if mode == 4 else [candidates[0]]
        for similarity, b_path in selected_candidates:
            match_status = content_matches(a_records[a_path], b_records[b_path])
            lines.append(
                f"A: {display_path(a_folder, a_path)}\n"
                f"B: {display_path(b_folder, b_path)}\n"
                f"Filename similarity: {similarity:.1%} | {match_status}"
            )
            used_b.add(b_path)

    unmatched_b = [display_path(b_folder, path) for path in sorted(set(b_records) - used_b)]
    add_section(lines, "B files not selected as filename candidates", unmatched_b)
    return lines


def hash_report(
    a_folder: Path,
    b_folder: Path,
    a_records: dict[Path, FileRecord],
    b_records: dict[Path, FileRecord],
) -> list[str]:
    b_by_hash: dict[str, list[Path]] = defaultdict(list)
    for path, record in b_records.items():
        b_by_hash[record.digest].append(path)

    matched_b: set[Path] = set()
    matches: list[str] = []
    missing: list[str] = []
    for a_path in sorted(a_records):
        matches_in_b = sorted(b_by_hash.get(a_records[a_path].digest, []))
        if matches_in_b:
            for b_path in matches_in_b:
                matches.append(
                    f"A: {display_path(a_folder, a_path)}\n"
                    f"B: {display_path(b_folder, b_path)}\n"
                    f"SHA-256: {a_records[a_path].digest}"
                )
                matched_b.add(b_path)
        else:
            missing.append(display_path(a_folder, a_path))

    unmatched_b = [display_path(b_folder, path) for path in sorted(set(b_records) - matched_b)]
    output: list[str] = []
    add_section(output, "Files with matching normalized SHA-256 content", matches)
    add_section(output, "A files with no matching content in B", missing)
    add_section(output, "B files with no matching content in A", unmatched_b)
    return output


def compare_folders(a_folder: Path, b_folder: Path, mode: int) -> Path:
    if not a_folder.is_dir():
        raise SystemExit(f"A folder does not exist or is not a directory: {a_folder}")
    if not b_folder.is_dir():
        raise SystemExit(f"B folder does not exist or is not a directory: {b_folder}")

    settings.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    settings.INPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Scanning files and calculating normalized SHA-256 hashes...")
    a_records, a_errors = scan_folder(a_folder)
    b_records, b_errors = scan_folder(b_folder)
    threshold = settings.FUZZY_FILENAME_THRESHOLD
    mode_names = {
        1: "Exact filename match",
        2: "Normalized filename match",
        3: f"Fuzzy filename match ({threshold:.0%}+)",
        4: "All filename comparisons",
        5: "Content match via SHA-256 hash",
    }
    output = [
        "FOLDER COMPARISON SUMMARY",
        "==========================",
        f"Mode: {mode_names[mode]}",
        f"A: {a_folder}",
        f"B: {b_folder}",
        f"Files scanned in A: {len(a_records):,}",
        f"Files scanned in B: {len(b_records):,}",
    ]
    if mode == 5:
        output.extend(hash_report(a_folder, b_folder, a_records, b_records))
    else:
        add_section(
            output,
            "Filename comparison results",
            filename_report(mode, a_folder, b_folder, a_records, b_records),
        )
    errors = [f"A: {error}" for error in a_errors] + [f"B: {error}" for error in b_errors]
    add_section(output, "Files that could not be read", errors)

    report = "\n".join(output)
    report_path = settings.OUTPUT_DIR / (
        f"folder_comparison_{datetime.now(ZoneInfo(settings.REPORT_TIMEZONE)):%Y%m%d_%H%M%S}.txt"
    )
    report_path.write_text(report + "\n", encoding="utf-8")
    print(report)
    print(f"\nReport saved to: {report_path}")
    return report_path


if __name__ == "__main__":
    selected_a = prompt_for_folder("A", settings.A_FOLDER)
    selected_b = prompt_for_folder("B", settings.B_FOLDER)
    selected_mode = choose_mode()
    compare_folders(selected_a, selected_b, selected_mode)
