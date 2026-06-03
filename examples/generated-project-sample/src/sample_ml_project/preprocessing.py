from __future__ import annotations

from typing import Any


Rows = list[dict[str, Any]]


def safe_float(value: Any) -> float | None:
    """Convert a value to float when possible."""
    if value is None or value == "":
        return None

    try:
        return float(str(value).replace(",", "."))
    except ValueError:
        return None


def fill_missing(rows: Rows, *, columns: list[str], value: Any) -> Rows:
    """Fill missing-like values in selected columns."""
    output = [dict(row) for row in rows]

    for row in output:
        for column in columns:
            if row.get(column) in (None, ""):
                row[column] = value

    return output


def drop_columns(rows: Rows, columns: list[str]) -> Rows:
    """Remove columns when they exist."""
    output = [dict(row) for row in rows]

    for row in output:
        for column in columns:
            row.pop(column, None)

    return output


def min_max_scale(rows: Rows, *, columns: list[str]) -> Rows:
    """Simple min-max scaling for numeric columns.

    Use only when scaling is useful for the model family.
    Distance, variance, and gradient-based models usually need scaling.
    Tree-based models usually do not.
    """
    output = [dict(row) for row in rows]

    for column in columns:
        values = [safe_float(row.get(column)) for row in output]
        numeric_values = [value for value in values if value is not None]

        if not numeric_values:
            continue

        min_value = min(numeric_values)
        max_value = max(numeric_values)
        denominator = max_value - min_value

        for row in output:
            value = safe_float(row.get(column))
            if value is None or denominator == 0:
                row[f"{column}_scaled"] = None
            else:
                row[f"{column}_scaled"] = (value - min_value) / denominator

    return output


def label_encode(rows: Rows, *, columns: list[str]) -> tuple[Rows, dict[str, dict[Any, int]]]:
    """Very small label encoder for categorical columns.

    For serious modeling, prefer a proper preprocessing pipeline.
    """
    output = [dict(row) for row in rows]
    mappings: dict[str, dict[Any, int]] = {}

    for column in columns:
        values = sorted({row.get(column) for row in output}, key=lambda item: str(item))
        mapping = {value: index for index, value in enumerate(values)}
        mappings[column] = mapping

        for row in output:
            row[f"{column}_encoded"] = mapping.get(row.get(column))

    return output, mappings
