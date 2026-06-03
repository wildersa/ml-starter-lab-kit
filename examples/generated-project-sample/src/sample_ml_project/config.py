
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_config(path: str | Path = "configs/config.json") -> dict[str, Any]:
    config_path = project_root() / path

    if not config_path.exists():
        raise FileNotFoundError(f"Config não encontrado: {config_path}")

    return json.loads(config_path.read_text(encoding="utf-8"))
