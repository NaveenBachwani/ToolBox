"""Copy to config.local.py and customize. config.local.py is gitignored."""

from pathlib import Path

# Default source folder (press Enter at prompt if empty)
A_FOLDER = Path("/path/to/source")

# Default destination folder
B_FOLDER = Path("/path/to/destination")

# Fuzzy filename match threshold (0.0–1.0)
FUZZY_FILENAME_THRESHOLD = 0.80

# Timezone for report filenames (IANA name, e.g. UTC, America/New_York)
REPORT_TIMEZONE = "UTC"
