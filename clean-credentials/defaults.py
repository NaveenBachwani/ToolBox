"""Generic defaults for credentials-extract. Override via config.local.py (gitignored)."""

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
INPUT_DIR = SCRIPT_DIR / "input"
OUTPUT_DIR = SCRIPT_DIR / "output"

INPUT_FILE = INPUT_DIR / "credentials.txt"
OUTPUT_FILE = OUTPUT_DIR / "credentials.csv"

EMAIL_MAP: dict[str, str] = {}

CATEGORY_RULES: dict[str, list[str]] = {
    "Developer & Tech": ["github", "gitlab"],
    "Social & Productivity": ["buffer", "meetup"],
    "General": ["example"],
}
