# Compare folders

`compare_folders.py` checks whether files from a source folder A were migrated to destination folder B. It scans subfolders recursively and writes a text report to `output/`.

## Basics

### Run it

```bash
cd compare-folders
python3 compare_folders.py
```

The script asks for two folders (defaults come from `config.local.py` if present):

```text
A folder [/your/default/source]:
B folder [/your/default/destination]:
```

Press Enter to accept a default, or type a path for a one-off run.

Then choose a comparison mode:

```text
1. Exact filename match
2. Normalized filename match
3. Fuzzy filename match
4. All filename comparisons
5. Content match via SHA-256 hash
```

### Configuration

Copy `config.example.py` to `config.local.py` and set:

- `A_FOLDER`, `B_FOLDER` — default paths
- `FUZZY_FILENAME_THRESHOLD` — default `0.80` (80%)
- `REPORT_TIMEZONE` — IANA timezone for report filenames (e.g. `UTC`, `Asia/Kolkata`)

`config.local.py` is gitignored.

### Input and output

| Folder | Use |
|--------|-----|
| `input/` | Reserved for future use; A/B paths are elsewhere on disk |
| `output/` | Timestamped reports: `folder_comparison_YYYYMMDD_HHMMSS.txt` |

Move or delete old reports from `output/` when no longer needed.

## Advanced

### Comparison modes

| Mode | Question it answers |
|------|---------------------|
| 1 — Exact filename | Same filename anywhere under B? |
| 2 — Normalized filename | Same name after lowercasing, ignoring punctuation? |
| 3 — Fuzzy filename | Best filename match above threshold? |
| 4 — All comparisons | Every A×B filename pair (can be large) |
| 5 — SHA-256 hash | Same file content regardless of name? |

For migration verification, a useful sequence: mode 2 → mode 3 → mode 5.

### Markdown normalization

For `.md` files, hashing ignores YAML front matter, line-ending differences, and trailing blank lines so Obsidian-style metadata does not false-flag differences.

### Limitations

- Filename similarity does not prove content match — check `CONTENT MATCH` in the report.
- Mode 4 can produce very large reports.
- The script **reads only** — it does not copy, move, or delete files in A or B.

<!-- readme-footer -->
---

I am new to programming, but love using Technology in daily life and work! Through this project, I am sharing some useful utilities & tools that have been created under my direction with the help of AI. I hope they can help improve your productivity, as they have done for me.

This repository is being made available in the spirit of open source. Readers are advised to use the commands and instructions here with care. The creator accepts no responsibility for system damage, data loss or other consequences resulting from their use.

For more advanced ideas, decisions and lessons from building with AI:
Project KnowHow http://knowhow.thinkshop.in
