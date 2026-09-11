"""Load defaults, then overlay config.local.py if present."""

import importlib.util
from pathlib import Path

from defaults import *  # noqa: F403

SCRIPT_DIR = Path(__file__).resolve().parent
_local_path = SCRIPT_DIR / "config.local.py"

if _local_path.is_file():
    spec = importlib.util.spec_from_file_location("config_local", _local_path)
    if spec and spec.loader:
        _local = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_local)
        for _name in dir(_local):
            if not _name.startswith("_"):
                globals()[_name] = getattr(_local, _name)
