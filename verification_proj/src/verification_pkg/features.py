from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime

def safe_float(value: object) -> float | None:
    if value is None:
        return None

    try:
        return float(str(value).replace(",", "."))
    except ValueError:
        return None

def add_ratio_feature(
    rows: list[dict[str, object]],
    *,
    name: str,
    numerator: str,
    denominator: str,
) -> list[dict[str, object]]:
    for row in rows:
        num = safe_float(row.get(numerator))
        den = safe_float(row.get(denominator))

        if num is None or den in (None, 0):
            row[name] = None
        else:
            row[name] = num / den

    return rows

def add_datetime_parts(
    rows: list[dict[str, object]],
    *,
    column: str,
    date_format: str | None = None,
) -> list[dict[str, object]]:
    for row in rows:
        raw = row.get(column)

        if not raw:
            continue

        try:
            dt = (
                datetime.strptime(str(raw), date_format)
                if date_format
                else datetime.fromisoformat(str(raw))
            )
        except ValueError:
            continue

        row[f"{column}_year"] = dt.year
        row[f"{column}_month"] = dt.month
        row[f"{column}_day"] = dt.day
        row[f"{column}_dayofweek"] = dt.weekday()
        row[f"{column}_is_weekend"] = dt.weekday() >= 5

    return rows

def add_lag_features(
    rows: list[dict[str, object]],
    *,
    column: str,
    lags: Iterable[int],
    order_by: str | None = None,
    groupby: str | None = None,
) -> list[dict[str, object]]:
    sorted_rows = sorted(
        rows,
        key=lambda r: (
            r.get(groupby, "") if groupby else "",
            r.get(order_by, "") if order_by else "",
        ),
    )

    groups: dict[object, list[dict[str, object]]] = {}
    for row in sorted_rows:
        key = row.get(groupby) if groupby else "__all__"
        groups.setdefault(key, []).append(row)

    for group_rows in groups.values():
        for index, row in enumerate(group_rows):
            for lag in lags:
                lag_index = index - lag
                row[f"{column}_lag_{lag}"] = (
                    group_rows[lag_index].get(column)
                    if lag_index >= 0
                    else None
                )

    return rows

def add_rolling_mean_features(
    rows: list[dict[str, object]],
    *,
    column: str,
    windows: Iterable[int],
    order_by: str | None = None,
    groupby: str | None = None,
    shift: int = 1,
) -> list[dict[str, object]]:
    sorted_rows = sorted(
        rows,
        key=lambda r: (
            r.get(groupby, "") if groupby else "",
            r.get(order_by, "") if order_by else "",
        ),
    )

    groups: dict[object, list[dict[str, object]]] = {}
    for row in sorted_rows:
        key = row.get(groupby) if groupby else "__all__"
        groups.setdefault(key, []).append(row)

    for group_rows in groups.values():
        values = [safe_float(row.get(column)) for row in group_rows]

        for index, row in enumerate(group_rows):
            for window in windows:
                end = max(0, index - shift + 1)
                start = max(0, end - window)
                history = [v for v in values[start:end] if v is not None]

                row[f"{column}_rolling_mean_{window}"] = (
                    sum(history) / len(history)
                    if history
                    else None
                )

    return rows

def apply_configured_features(
    rows: list[dict[str, object]],
    feature_config: dict[str, object],
) -> list[dict[str, object]]:
    rows = [dict(row) for row in rows]

    for rule in feature_config.get("calculated_features", []):
        if not rule.get("enabled", False):
            continue

        rule_type = rule.get("type")

        if rule_type == "ratio":
            rows = add_ratio_feature(
                rows,
                name=rule["name"],
                numerator=rule["numerator"],
                denominator=rule["denominator"],
            )

        elif rule_type == "datetime_parts":
            rows = add_datetime_parts(
                rows,
                column=rule["column"],
            )

        elif rule_type == "lag":
            rows = add_lag_features(
                rows,
                column=rule["column"],
                lags=rule["lags"],
                groupby=rule.get("groupby"),
                order_by=rule.get("order_by"),
            )

        elif rule_type == "rolling_mean":
            rows = add_rolling_mean_features(
                rows,
                column=rule["column"],
                windows=rule["windows"],
                groupby=rule.get("groupby"),
                order_by=rule.get("order_by"),
                shift=rule.get("shift", 1),
            )

    drop_columns = set(feature_config.get("drop_columns", []))
    if drop_columns:
        for row in rows:
            for column in drop_columns:
                row.pop(column, None)

    return rows
