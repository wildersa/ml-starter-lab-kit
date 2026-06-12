from __future__ import annotations

import json
from collections import Counter

from .core.config import load_config, project_root
from .core.data import load_csv


def load_model(path: str = "models/model.json") -> dict[str, object]:
    model_path = project_root() / path

    if not model_path.exists():
        raise FileNotFoundError("Model not found. Run train.py first.")

    return json.loads(model_path.read_text(encoding="utf-8"))


def evaluate_majority_baseline(rows: list[dict[str, str]], model: dict[str, object]) -> dict[str, object]:
    target = model["target_column"]
    prediction = model["prediction"]

    y_true = [row.get(target) for row in rows if row.get(target) not in (None, "")]
    correct = sum(1 for value in y_true if value == prediction)

    return {
        "metric": "accuracy",
        "accuracy": correct / len(y_true) if y_true else 0,
        "samples": len(y_true),
        "prediction": prediction,
        "target_distribution": dict(Counter(y_true)),
    }


def main() -> None:
    config = load_config()
    rows = load_csv(config["data"]["processed_path"])
    model = load_model()

    if model.get("model_type") == "majority_class_baseline":
        metrics = evaluate_majority_baseline(rows, model)
    else:
        metrics = {
            "note": "Evaluation not yet implemented for this model type.",
            "model_type": model.get("model_type"),
        }

    output_path = project_root() / "reports/metrics.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")

    # Generate Markdown report
    report_path = project_root() / "reports/evaluation-report.md"
    lang = config.get("project", {}).get("language", "en")

    if lang == "pt-BR":
        report_content = f"""# Relatório de Avaliação

## Resumo
- **Modelo**: {model.get("model_type", "N/A")}
- **Amostras**: {metrics.get("samples", 0)}
- **Métrica Principal**: {metrics.get("metric", "N/A")}
- **Valor**: {metrics.get(metrics.get("metric", ""), "N/A")}

## Detalhes
```json
{json.dumps(metrics, indent=2, ensure_ascii=False)}
```
"""
    else:
        report_content = f"""# Evaluation Report

## Summary
- **Model**: {model.get("model_type", "N/A")}
- **Samples**: {metrics.get("samples", 0)}
- **Primary Metric**: {metrics.get("metric", "N/A")}
- **Value**: {metrics.get(metrics.get("metric", ""), "N/A")}

## Details
```json
{json.dumps(metrics, indent=2, ensure_ascii=False)}
```
"""
    report_path.write_text(report_content, encoding="utf-8")

    print("Metrics saved at reports/metrics.json")
    print("Report saved at reports/evaluation-report.md")
    print(json.dumps(metrics, indent=2, ensure_ascii=False))

    # MLflow Tracking
    if config.get("tracking", {}).get("enabled_mlflow"):
        try:
            import mlflow

            with mlflow.start_run(run_name="baseline_evaluation"):
                # Log metrics
                if "accuracy" in metrics:
                    mlflow.log_metric("accuracy", metrics["accuracy"])

                mlflow.log_metric("samples", metrics.get("samples", 0))

                # Log report artifact
                if output_path.exists():
                    mlflow.log_artifact(str(output_path))

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
