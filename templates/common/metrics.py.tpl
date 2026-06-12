from __future__ import annotations

from math import sqrt
from typing import Any


def accuracy(y_true: list[Any], y_pred: list[Any]) -> float:
    """Classification accuracy: (TP + TN) / Total."""
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length.")
    if not y_true:
        return 0.0

    correct = sum(1 for expected, predicted in zip(y_true, y_pred) if expected == predicted)
    return correct / len(y_true)


def confusion_counts(y_true: list[Any], y_pred: list[Any], *, positive_label: Any) -> dict[str, int]:
    """Return TP, FP, TN, FN for a binary classification task."""
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length.")

    result = {"tp": 0, "fp": 0, "tn": 0, "fn": 0}

    for expected, predicted in zip(y_true, y_pred):
        if expected == positive_label and predicted == positive_label:
            result["tp"] += 1
        elif expected != positive_label and predicted == positive_label:
            result["fp"] += 1
        elif expected != positive_label and predicted != positive_label:
            result["tn"] += 1
        elif expected == positive_label and predicted != positive_label:
            result["fn"] += 1

    return result


def precision(y_true: list[Any], y_pred: list[Any], *, positive_label: Any) -> float:
    """Classification precision: TP / (TP + FP). How many predicted positives are actually positive?"""
    counts = confusion_counts(y_true, y_pred, positive_label=positive_label)
    tp, fp = counts["tp"], counts["fp"]
    if (tp + fp) == 0:
        return 0.0
    return tp / (tp + fp)


def recall(y_true: list[Any], y_pred: list[Any], *, positive_label: Any) -> float:
    """Classification recall: TP / (TP + FN). How many actual positives did we find?"""
    counts = confusion_counts(y_true, y_pred, positive_label=positive_label)
    tp, fn = counts["tp"], counts["fn"]
    if (tp + fn) == 0:
        return 0.0
    return tp / (tp + fn)


def f1_score(y_true: list[Any], y_pred: list[Any], *, positive_label: Any) -> float:
    """Classification F1 score: harmonic mean of precision and recall."""
    p = precision(y_true, y_pred, positive_label=positive_label)
    r = recall(y_true, y_pred, positive_label=positive_label)
    if (p + r) == 0:
        return 0.0
    return 2 * (p * r) / (p + r)


def mean_absolute_error(y_true: list[float], y_pred: list[float]) -> float:
    """Regression Mean Absolute Error (MAE). Average of absolute differences."""
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length.")
    if not y_true:
        return 0.0

    return sum(abs(expected - predicted) for expected, predicted in zip(y_true, y_pred)) / len(y_true)


def root_mean_squared_error(y_true: list[float], y_pred: list[float]) -> float:
    """Regression Root Mean Squared Error (RMSE). Punishes larger errors more than MAE."""
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length.")
    if not y_true:
        return 0.0

    mse = sum((expected - predicted) ** 2 for expected, predicted in zip(y_true, y_pred)) / len(y_true)
    return sqrt(mse)


def mean_absolute_percentage_error(y_true: list[float], y_pred: list[float]) -> float:
    """Regression MAPE. Safely handles zero actual values by skipping them."""
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length.")
    if not y_true:
        return 0.0

    total_error = 0.0
    valid_count = 0
    for expected, predicted in zip(y_true, y_pred):
        if abs(expected) > 1e-9:
            total_error += abs((expected - predicted) / expected)
            valid_count += 1

    if valid_count == 0:
        return 0.0
    return total_error / valid_count


def r_squared(y_true: list[float], y_pred: list[float]) -> float:
    """Regression R-squared (Coefficient of Determination).
    1.0 is a perfect fit, 0.0 is a baseline that always predicts the mean.
    """
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length.")
    if not y_true:
        return 0.0

    mean_y = sum(y_true) / len(y_true)
    ss_res = sum((expected - predicted) ** 2 for expected, predicted in zip(y_true, y_pred))
    ss_tot = sum((expected - mean_y) ** 2 for expected in y_true)

    if ss_tot == 0:
        return 0.0
    return 1 - (ss_res / ss_tot)


def bandit_summary(rewards: list[float]) -> dict[str, float]:
    """Basic summary metrics for Multi-Armed Bandit rewards."""
    if not rewards:
        return {"total_reward": 0.0, "average_reward": 0.0, "count": 0}

    total = sum(rewards)
    return {
        "total_reward": float(total),
        "average_reward": total / len(rewards),
        "count": len(rewards)
    }


def arm_counts(selected_arms: list[Any]) -> dict[Any, int]:
    """Return the number of times each arm was selected."""
    counts: dict[Any, int] = {}
    for arm in selected_arms:
        counts[arm] = counts.get(arm, 0) + 1
    return counts


def calculate_lift(current: float, baseline: float) -> float:
    """Calculate relative lift: (current - baseline) / baseline.
    Returns 0.0 if baseline is 0.
    """
    if baseline == 0:
        return 0.0
    return (current - baseline) / baseline
