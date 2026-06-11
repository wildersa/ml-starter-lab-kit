from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from .core.config import load_config, project_root
from .core.data import load_csv
from .features import apply_configured_features

def train_baseline_classifier(rows: list[dict[str, object]], target_column: str) -> dict[str, object]:
    if not target_column:
        raise ValueError("target_column not configured.")

    values = [row.get(target_column) for row in rows if row.get(target_column) not in (None, "")]
    if not values:
        raise ValueError(f"No values found for target: {target_column}")

    most_common = Counter(values).most_common(1)[0][0]

    return {
        "model_type": "majority_class_baseline",
        "target_column": target_column,
        "prediction": most_common,
        "classes": dict(Counter(values)),
    }

def save_model(model: dict[str, object], path: str | Path = "models/model.json") -> None:
    model_path = project_root() / path
    model_path.parent.mkdir(parents=True, exist_ok=True)
    model_path.write_text(json.dumps(model, indent=2, ensure_ascii=False), encoding="utf-8")

def main() -> None:
    config = load_config()
    rows = load_csv(config["data"]["processed_path"])
    rows = apply_configured_features(rows, config.get("features", {}))

    task = config["project"]["task"]
    target_column = config["target"]["column"]

    if task in {"generic", "supervised", "vision"}:
        model = train_baseline_classifier(rows, target_column)
    elif task == "unsupervised":
        model = {
            "model_type": "unsupervised_placeholder",
            "note": "Add PCA/K-Means with scikit-learn here, if the project uses scikit-learn."
        }
    elif task == "timeseries":
        model = {
            "model_type": "timeseries_placeholder",
            "note": "Add LSTM/Keras or another temporal model here, if the project uses deep learning."
        }
    else:
        raise ValueError(f"Task not supported: {task}")

    save_model(model)
    print("Model saved at models/model.json")
    print(json.dumps(model, indent=2, ensure_ascii=False))

    # MLflow Tracking
    if config.get("tracking", {}).get("enabled_mlflow"):
        try:
            import mlflow

            with mlflow.start_run(run_name="baseline_training"):
                mlflow.log_param("task", task)
                mlflow.log_param("target_column", target_column)
                mlflow.log_param("model_type", model.get("model_type"))
                mlflow.log_param("dataset_path", config["data"]["raw_path"])

                # Log model artifact
                model_path = project_root() / "models/model.json"
                if model_path.exists():
                    mlflow.log_artifact(str(model_path))

                print("MLflow: tracking complete.")
        except ImportError:
            print("\n" + "="*50)
            print("MLflow is enabled in config but not installed.")
            print("Please install it using:")
            print("  pip install -r requirements-mlflow.txt")
            print("="*50 + "\n")
        except Exception as e:
            print(f"MLflow tracking failed: {e}")

if __name__ == "__main__":
    main()
