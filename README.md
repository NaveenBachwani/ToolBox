# ToolBox

Small, focused Python scripts for everyday file and data tasks. Each tool lives in its own folder with local `input/` and `output/` directories.

## Requirements

| Need | Details |
|------|---------|
| **OS** | Linux or macOS (Windows: try WSL) |
| **Python** | 3.10+ (`python3 --version`) |
| **Extra packages** | None — standard library only |
| **Skills** | `cd`, `ls`, `python3`, and editing a short config file |

## Quick start

```bash
cd compare-folders
cp config.example.py config.local.py   # optional — set your paths
python3 compare_folders.py
```

Results appear in that tool’s `output/` folder. Full usage is in each tool’s doc (start with **Basics**).

## Tools

| Folder | Doc | What it does |
|--------|-----|----------------|
| [compare-folders](compare-folders/) | [compare-folders-README.md](compare-folders/compare-folders-README.md) | Compare two folder trees (filename + content hash) |
| [clean-credentials](clean-credentials/) | [clean-credentials-README.md](clean-credentials/clean-credentials-README.md) | Convert a plain-text credentials file to CSV |

## Folder layout (every tool)

| Path | In git? | Purpose |
|------|---------|---------|
| `input/` | No | Put files here before running |
| `output/` | No | Results land here — move them out when done |
| `config.local.py` | No | Your personal paths and settings |
| `config.example.py` | Yes | Template to copy |
| `defaults.py` | Yes | Shared safe defaults |

Scripts create `input/` and `output/` if missing.

## Personal config

1. Copy `config.example.py` → `config.local.py` in the tool folder.
2. Edit paths or other settings.
3. Never commit `config.local.py` (it is gitignored).

<!-- readme-footer -->
---

I am new to programming, but love using Technology in daily life and work! Through this project, I am sharing some useful utilities & tools that have been created under my direction with the help of AI. I hope they can help improve your productivity, as they have done for me.

This repository is being made available in the spirit of open source. Readers are advised to use the commands and instructions here with care. The creator accepts no responsibility for system damage, data loss or other consequences resulting from their use.

For more advanced ideas, decisions and lessons from building with AI:
Project KnowHow http://knowhow.thinkshop.in
