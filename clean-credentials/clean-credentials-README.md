# Clean credentials

`credentials-extract.py` parses a plain-text credentials file into a structured CSV for import into a password manager or spreadsheet.

## Basics

### Run it

```bash
cd clean-credentials
cp config.example.py config.local.py   # first time — set email aliases
# Place your file at input/credentials.txt
python3 credentials-extract.py
```

Output: `output/credentials.csv`

**Move the CSV out of `output/` when finished** — it contains passwords.

### Input format

Plain text, one entry per line. Use `>>` for category headers:

```text
Work Accounts >>
github, myuser, secretpass, https://github.com
n.b@g, app-password-here
```

Tokens are split on commas, pipes, or ` - `. Short email aliases (e.g. `n.b@g`) expand via `EMAIL_MAP` in `config.local.py`.

### Configuration

Copy `config.example.py` → `config.local.py`:

| Setting | Purpose |
|---------|---------|
| `EMAIL_MAP` | Short handles → full email addresses |
| `CATEGORY_RULES` | Keywords → auto-categories when no `>>` header |
| `INPUT_FILE` / `OUTPUT_FILE` | Override default paths (optional) |

### Input and output

| Path | Role |
|------|------|
| `input/credentials.txt` | Your source file (gitignored) |
| `output/credentials.csv` | Generated export (gitignored) |

Neither path is committed to git.

### Security

- Treat `input/` and `output/` as sensitive at all times.
- Do not commit credential files or `config.local.py` with real emails.
- Review the CSV before importing elsewhere; delete local copies when done.

## Advanced

### Category rules

`CATEGORY_RULES` in `config.local.py` maps keywords in a line to a category when no `>>` header is active. Useful for mixed dumps where sections are not explicitly labeled.

### Custom paths

Override `INPUT_FILE` and `OUTPUT_FILE` in `config.local.py` if your source file is not `input/credentials.txt` or you want a different export location. Paths are still gitignored when they sit under `input/` or `output/`.

<!-- readme-footer -->
---

I am new to programming, but love using Technology in daily life and work! Through this project, I am sharing some useful utilities & tools that have been created under my direction with the help of AI. I hope they can help improve your productivity, as they have done for me.

This repository is being made available in the spirit of open source. Readers are advised to use the commands and instructions here with care. The creator accepts no responsibility for system damage, data loss or other consequences resulting from their use.

For more advanced ideas, decisions and lessons from building with AI:
Project KnowHow http://knowhow.thinkshop.in
