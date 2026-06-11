from __future__ import annotations

import json
from pathlib import Path
from typing import Any

def project_root() -> Path:
    """Returns the project root directory."""
    return Path(__file__).resolve().parents[3]

def load_config(path: str | Path = "configs/config.json") -> dict[str, Any]:
    """Loads the project configuration from a JSON file."""
    config_path = project_root() / path

    if not config_path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")

    return json.loads(config_path.read_text(encoding="utf-8"))

def get_mlflow_status(config: dict[str, Any]) -> bool:
    """
    Returns whether MLflow tracking is enabled based on the project configuration.
    Prioritizes 'tracking.enabled_mlflow' (canonical) with fallback to 'tracking.mlflow.enabled'.
    """
    tracking = config.get("tracking", {})
    enabled = tracking.get("enabled_mlflow")
    if enabled is None:
        enabled = tracking.get("mlflow", {}).get("enabled", False)
    return bool(enabled)
