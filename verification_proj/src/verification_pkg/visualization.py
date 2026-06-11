from __future__ import annotations

from typing import Any

Rows = list[dict[str, Any]]

def explain_visualization_policy() -> str:
    """Return the starter kit visualization policy."""
    return (
        "This module intentionally avoids plotting dependencies by default. "
        "Add matplotlib, seaborn, plotly, or another library only when the project needs charts."
    )

def value_counts(rows: Rows, column: str) -> dict[Any, int]:
    """Return counts that can later be plotted as a bar chart."""
    counts: dict[Any, int] = {}

    for row in rows:
        value = row.get(column)
        counts[value] = counts.get(value, 0) + 1

    return counts

def numeric_histogram_bins(rows: Rows, column: str, *, bins: int = 10) -> list[dict[str, float | int]]:
    """Create simple histogram bin counts without plotting.

    This prepares data for a future chart without requiring matplotlib.
    """
    values: list[float] = []

    for row in rows:
        try:
            values.append(float(row[column]))
        except (KeyError, TypeError, ValueError):
            continue

    if not values or bins <= 0:
        return []

    min_value = min(values)
    max_value = max(values)

    if min_value == max_value:
        return [{"start": min_value, "end": max_value, "count": len(values)}]

    width = (max_value - min_value) / bins
    result = []

    for index in range(bins):
        start = min_value + index * width
        end = start + width
        count = sum(1 for value in values if start <= value < end)
        result.append({"start": start, "end": end, "count": count})

    result[-1]["count"] += sum(1 for value in values if value == max_value)
    return result
