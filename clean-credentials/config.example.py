"""Copy to config.local.py and customize. config.local.py is gitignored."""

# Short aliases in your credentials.txt expanded to full addresses
EMAIL_MAP = {
    "alias": "you@example.com",
}

# Keyword lists used to auto-categorize services (customize freely)
CATEGORY_RULES = {
    "Developer & Tech": ["github", "gitlab"],
    "Social & Productivity": ["buffer", "meetup"],
}

# Optional: override input/output filenames
# INPUT_FILE = INPUT_DIR / "my-credentials.txt"
# OUTPUT_FILE = OUTPUT_DIR / "my-credentials.csv"
