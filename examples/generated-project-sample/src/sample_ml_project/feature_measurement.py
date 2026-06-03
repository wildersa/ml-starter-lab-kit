
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class FeatureImpact:
    """Small record describing whether a feature helped."""

    feature_name: str
    metric_name: str
    metric_before: float
    metric_after: float
    leakage_risk: str = "unknown"
    stability_note: str = "not_checked"
    decision: str = "review"
    note: str = ""

    @property
    def delta(self) -> float:
        return self.metric_after - self.metric_before

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["delta"] = self.delta
        return result


def decide_feature_impact(
    *,
    feature_name: str,
    metric_name: str,
    metric_before: float,
    metric_after: float,
    min_delta: float = 0.0,
    leakage_risk: str = "unknown",
    stability_note: str = "not_checked",
    note: str = "",
) -> FeatureImpact:
    """Create a basic feature impact decision.

    Assumes higher metric is better.
    For error metrics such as MAE/RMSE, invert the comparison or adapt this function.
    """
    delta = metric_after - metric_before

    if leakage_risk == "high":
        decision = "remove_or_quarantine"
    elif delta > min_delta:
        decision = "keep"
    elif delta == 0:
        decision = "no_gain"
    else:
        decision = "remove"

    return FeatureImpact(
        feature_name=feature_name,
        metric_name=metric_name,
        metric_before=metric_before,
        metric_after=metric_after,
        leakage_risk=leakage_risk,
        stability_note=stability_note,
        decision=decision,
        note=note,
    )


def feature_impact_table(records: list[FeatureImpact]) -> list[dict[str, Any]]:
    """Convert feature impact records to table-like dictionaries."""
    return [record.to_dict() for record in records]
