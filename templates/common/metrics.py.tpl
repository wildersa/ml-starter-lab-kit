from __future__ import annotations

from math import sqrt
from typing import Any


def accuracy(y_true: list[Any], y_pred: list[Any]) -> float:
    """Classification accuracy."""
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length.")
    if not y_true:
        return 0.0

    correct = sum(1 for expected, predicted in zip(y_true, y_pred) if expected == predicted)
    return correct / len(y_true)


def mean_absolute_error(y_true: list[float], y_pred: list[float]) -> float:
    """Regression MAE."""
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length.")
    if not y_true:
        return 0.0

    return sum(abs(expected - predicted) for expected, predicted in zip(y_true, y_pred)) / len(y_true)


def root_mean_squared_error(y_true: list[float], y_pred: list[float]) -> float:
    """Regression RMSE."""
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length.")
    if not y_true:
        return 0.0

    mse = sum((expected - predicted) ** 2 for expected, predicted in zip(y_true, y_pred)) / len(y_true)
    return sqrt(mse)


def mean_absolute_percentage_error(y_true: list[float], y_pred: list[float]) -> float:
    """Regression MAPE."""
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length.")
    if not y_true:
        return 0.0

    # Avoid division by zero by using a small epsilon
    epsilon = 1e-10
    return sum(
        abs((expected - predicted) / max(abs(expected), epsilon))
        for expected, predicted in zip(y_true, y_pred)
    ) / len(y_true)


def r2_score(y_true: list[float], y_pred: list[float]) -> float:
    """Regression R2 score (Coefficient of Determination)."""
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length.")
    if not y_true:
        return 0.0

    y_true_mean = sum(y_true) / len(y_true)
    ss_res = sum((expected - predicted) ** 2 for expected, predicted in zip(y_true, y_pred))
    ss_tot = sum((expected - y_true_mean) ** 2 for expected in y_true)

    if ss_tot == 0:
        return 0.0
    return 1 - (ss_res / ss_tot)


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
    """Classification precision."""
    counts = confusion_counts(y_true, y_pred, positive_label=positive_label)
    denominator = counts["tp"] + counts["fp"]
    return counts["tp"] / denominator if denominator > 0 else 0.0


def recall(y_true: list[Any], y_pred: list[Any], *, positive_label: Any) -> float:
    """Classification recall."""
    counts = confusion_counts(y_true, y_pred, positive_label=positive_label)
    denominator = counts["tp"] + counts["fn"]
    return counts["tp"] / denominator if denominator > 0 else 0.0


def f1_score(y_true: list[Any], y_pred: list[Any], *, positive_label: Any) -> float:
    """Classification F1 score."""
    p = precision(y_true, y_pred, positive_label=positive_label)
    r = recall(y_true, y_pred, positive_label=positive_label)
    denominator = p + r
    return 2 * (p * r) / denominator if denominator > 0 else 0.0


# --- Multi-Armed Bandit Metrics ---

def bandit_total_reward(rewards: list[int | float]) -> float:
    """Total reward obtained in a bandit simulation."""
    return float(sum(rewards))


def bandit_average_reward(rewards: list[int | float]) -> float:
    """Average reward per round in a bandit simulation."""
    if not rewards:
        return 0.0
    return sum(rewards) / len(rewards)


def bandit_lift(avg_reward: float, baseline_reward: float) -> float:
    """Relative improvement over a baseline reward."""
    if baseline_reward == 0:
        return 0.0
    return (avg_reward - baseline_reward) / baseline_reward
