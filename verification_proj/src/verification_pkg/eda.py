from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from .core.config import load_config, project_root
from .core.data import load_csv

Rows = list[dict[str, Any]]

def infer_columns(rows: Rows) -> list[str]:
    """Return columns found in the first row."""
    if not rows:
        return []
    return list(rows[0].keys())

def missing_summary(rows: Rows) -> dict[str, int]:
    """Count missing-like values by column."""
    columns = infer_columns(rows)
    result = {column: 0 for column in columns}

    for row in rows:
        for column in columns:
            value = row.get(column)
            if value is None or value == "":
                result[column] += 1

    return result

def unique_count_summary(rows: Rows) -> dict[str, int]:
    """Count unique values by column."""
    columns = infer_columns(rows)
    result: dict[str, int] = {}

    for column in columns:
        result[column] = len({str(row.get(column)) for row in rows})

    return result

def target_distribution(rows: Rows, target_column: str) -> dict[Any, int]:
    """Count values for a target column."""
    return dict(Counter(row.get(target_column) for row in rows))

def run_eda() -> None:
    """Performs EDA and saves persistent artifacts."""
    try:
        config = load_config()
    except FileNotFoundError:
        print("Error: Configuration file not found.")
        sys.exit(1)

    raw_path = config.get("data", {}).get("raw_path")
    target_column = config.get("target", {}).get("column")

    if not raw_path:
        print("Error: Dataset path not configured in config.json.")
        sys.exit(1)

    try:
        rows = load_csv(raw_path)
    except FileNotFoundError:
        print(f"Error: Dataset not found at {raw_path}")
        return

    if not rows:
        print(f"Error: Dataset at {raw_path} is empty.")
        return

    columns = infer_columns(rows)
    missing = missing_summary(rows)
    uniques = unique_count_summary(rows)

    target_exists = target_column in columns
    target_dist = {}
    if target_exists:
        target_dist = target_distribution(rows, target_column)

    # P0.1: JSON artifact
    summary = {
        "rows": len(rows),
        "columns": columns,
        "target_column": target_column,
        "target_exists": target_exists,
        "missing_summary": missing,
        "unique_counts": uniques,
        "target_distribution": {str(k): v for k, v in target_dist.items()}
    }

    summary_path = project_root() / "configs/eda_summary.json"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # P0.2: Markdown artifact
    report_lines = [
        "# Dataset Summary",
        "",
        f"**Rows:** {len(rows)}",
        f"**Columns:** {len(columns)}",
        "",
        "## Columns",
        ""
    ]

    for col in columns:
        col_type = "target" if col == target_column else "feature"
        report_lines.append(f"- **{col}** ({col_type}): {uniques[col]} unique values, {missing[col]} missing")

    if target_exists:
        report_lines.append("")
        report_lines.append(f"## Target Distribution: {target_column}")
        report_lines.append("")
        for val, count in target_dist.items():
            report_lines.append(f"- {val}: {count}")

    report_path = project_root() / "reports/eda-summary.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"EDA complete. Artifacts created:")
    print(f"- {summary_path}")
    print(f"- {report_path}")

if __name__ == "__main__":
    run_eda()
