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
