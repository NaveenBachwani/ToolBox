"""Generic defaults for compare_folders. Override via config.local.py (gitignored)."""

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
INPUT_DIR = SCRIPT_DIR / "input"
OUTPUT_DIR = SCRIPT_DIR / "output"

A_FOLDER = Path("")
B_FOLDER = Path("")
FUZZY_FILENAME_THRESHOLD = 0.80
REPORT_TIMEZONE = "UTC"
