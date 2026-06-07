from __future__ import annotations

import json
from pathlib import Path
from .io import write_text

def create_config(
    root: Path,
    values: dict[str, str],
    *,
    force: bool,
    problem_profile: dict[str, str] | None = None
) -> None:
    task = values["TASK"]
    raw_path = values["DATASET_PATH"]
    target_column = values["TARGET_COLUMN"]

    if values.get("INCLUDE_DEMO") == "true":
        raw_path = "data/raw/demo_dataset.csv"
        if task == "supervised":
            goal = (problem_profile or {}).get("goal", "").lower()
            if any(keyword in goal for keyword in ["number", "número", "2"]):
                target_column = "price"
            else:
                target_column = "subscribed"
        elif task == "unsupervised":
            target_column = ""
        elif task == "timeseries":
            target_column = "sales"
        elif task == "vision":
            target_column = "label"
        elif task == "generic":
            target_column = "target"

    config: dict[str, object] = {
        "project": {
            "name": values["PROJECT_NAME"],
            "package": values["PACKAGE_NAME"],
            "task": task
        },
        "data": {
            "raw_path": raw_path,
            "processed_path": "data/processed/modeling_table.csv"
        },
        "target": {
            "column": target_column
        },
        "split": {
            "test_size": 0.2,
            "random_state": 42
        },
        "features": {
            "drop_columns": [],
            "calculated_features": [
                {
                    "type": "ratio",
                    "name": "example_ratio",
                    "numerator": "col_a",
                    "denominator": "col_b",
                    "enabled": False
                },
                {
                    "type": "datetime_parts",
                    "column": "event_date",
                    "enabled": False
                },
                {
                    "type": "lag",
                    "column": "value",
                    "lags": [1, 7],
                    "groupby": None,
                    "order_by": "event_date",
                    "enabled": False
                },
                {
                    "type": "rolling_mean",
                    "column": "value",
                    "windows": [7, 30],
                    "groupby": None,
                    "order_by": "event_date",
                    "shift": 1,
                    "enabled": False
                }
            ]
        },
        "model": {
            "type": "baseline",
            "params": {}
        },
        "tracking": {
            "enabled_mlflow": values.get("ENABLE_MLFLOW") == "true"
        },
        "eda": {
            "id_columns": [],
            "date_columns": [],
            "categorical_columns": [],
            "numeric_columns": [],
            "suspected_leakage_columns": []
        }
    }

    if task == "unsupervised":
        config["target"] = {"column": ""}
        config["model"] = {
            "type": "pca_kmeans",
            "params": {
                "n_components": 2,
                "n_clusters": 3,
                "random_state": 42
            }
        }

    if task == "timeseries":
        config["time_series"] = {
            "date_column": "date",
            "value_column": "value",
            "window_size": 30,
            "horizon": 7,
            "groupby": None
        }

    write_text(
        root / "configs/config.json",
        json.dumps(config, indent=2, ensure_ascii=False),
        force=force,
    )


def create_problem_profile(
    root: Path,
    problem_profile: dict[str, str],
    *,
    force: bool
) -> None:
    # Ensure language is stored
    if "language" not in problem_profile:
        problem_profile["language"] = "en"

    write_text(
        root / "configs/problem_profile.json",
        json.dumps(problem_profile, indent=2, ensure_ascii=False),
        force=force,
    )
