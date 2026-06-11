from __future__ import annotations

import csv
from pathlib import Path
from .config import project_root

def load_csv(path: str | Path) -> list[dict[str, str]]:
    """Loads a CSV file from the project root."""
    file_path = project_root() / path

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    with file_path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))

def save_csv(rows: list[dict[str, object]], path: str | Path) -> None:
    """Saves a list of dictionaries as a CSV file to the project root."""
    if not rows:
        raise ValueError("No rows to save.")

    file_path = project_root() / path
    file_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(rows[0].keys())

    with file_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
