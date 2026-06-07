from __future__ import annotations

from collections import Counter
from typing import Any

from .core.config import load_config
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
        result[column] = len({row.get(column) for row in rows})

    return result


def target_distribution(rows: Rows, target_column: str) -> dict[Any, int]:
    """Count values for a target column."""
    return dict(Counter(row.get(target_column) for row in rows))


def print_basic_report(rows: Rows, target_column: str | None = None) -> None:
    """Print a small EDA report without external dependencies."""
    print(f"Rows: {len(rows)}")
    print(f"Columns: {len(infer_columns(rows))}")
    print("Missing values:")
    print(missing_summary(rows))
    print("Unique values:")
    print(unique_count_summary(rows))

    if target_column:
        print(f"Target distribution for {target_column}:")
        print(target_distribution(rows, target_column))


def main() -> None:
    config = load_config()
    raw_path = config["data"]["raw_path"]
    target_column = config["target"]["column"]

    try:
        rows = load_csv(raw_path)
        print(f"\n--- Basic EDA: {raw_path} ---")
        print_basic_report(rows, target_column)
    except FileNotFoundError:
        print(f"Dataset not found at {raw_path}. Please place your data there first.")
    except Exception as e:
        print(f"Error during EDA: {e}")


if __name__ == "__main__":
    main()
