from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

def infer_type(values: list[str]) -> str:
    """Infers the data type of a list of string values."""
    valid_values = [v for v in values if v.strip()]
    if not valid_values:
        return "empty/unknown"

    is_numeric = True
    for v in valid_values:
        try:
            float(v.replace(",", ".")) # handle some european decimals just in case
        except ValueError:
            is_numeric = False
            break
    if is_numeric:
        return "numeric"

    is_date = True
    for v in valid_values:
        # Very simple heuristic: contains - or / and some numbers
        if not (("-" in v or "/" in v) and any(c.isdigit() for c in v)):
            is_date = False
            break
    if is_date:
        return "date-like"

    return "categorical/text"

def check_dataset_readiness(path: Path) -> dict[str, Any]:
    """
    Checks if the dataset exists and returns a summary of its structure.
    Useful for both CLI and Streamlit onboarding flows.
    """
    if not path.exists():
        return {"exists": False, "path": str(path)}

    try:
        with open(path, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            columns = reader.fieldnames
            if not columns:
                return {"exists": True, "path": str(path), "empty": True}

            sample_rows = []
            for i, row in enumerate(reader):
                sample_rows.append(row)
                if i >= 100:
                    break

        column_info = {}
        target_candidates = []
        for col in columns:
            col_values = [row[col] for row in sample_rows if col in row and row[col] is not None]
            col_type = infer_type(col_values)
            column_info[col] = {"type": col_type}

            if col.lower() in ["target", "label", "y", "class", "outcome"]:
                target_candidates.append(col)

        return {
            "exists": True,
            "path": str(path),
            "empty": False,
            "columns": column_info,
            "sample_count": len(sample_rows),
            "target_candidates": target_candidates,
        }
    except Exception as e:
        return {"exists": True, "path": str(path), "error": str(e)}
