from __future__ import annotations

import json
from math import sqrt
from pathlib import Path
from typing import Any

from .core.config import load_config, project_root
from .core.data import load_csv


# --- Inlined basic metrics to ensure evaluate.py is self-contained ---

def accuracy(y_true: list[Any], y_pred: list[Any]) -> float:
    if not y_true:
        return 0.0
    correct = sum(1 for expected, predicted in zip(y_true, y_pred) if expected == predicted)
    return correct / len(y_true)


def confusion_counts(y_true: list[Any], y_pred: list[Any], *, positive_label: Any) -> dict[str, int]:
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
    counts = confusion_counts(y_true, y_pred, positive_label=positive_label)
    denominator = counts["tp"] + counts["fp"]
    return counts["tp"] / denominator if denominator > 0 else 0.0


def recall(y_true: list[Any], y_pred: list[Any], *, positive_label: Any) -> float:
    counts = confusion_counts(y_true, y_pred, positive_label=positive_label)
    denominator = counts["tp"] + counts["fn"]
    return counts["tp"] / denominator if denominator > 0 else 0.0


def f1_score(y_true: list[Any], y_pred: list[Any], *, positive_label: Any) -> float:
    p = precision(y_true, y_pred, positive_label=positive_label)
    r = recall(y_true, y_pred, positive_label=positive_label)
    denominator = p + r
    return 2 * (p * r) / denominator if denominator > 0 else 0.0


def mean_absolute_error(y_true: list[float], y_pred: list[float]) -> float:
    if not y_true:
        return 0.0
    return sum(abs(expected - predicted) for expected, predicted in zip(y_true, y_pred)) / len(y_true)


def root_mean_squared_error(y_true: list[float], y_pred: list[float]) -> float:
    if not y_true:
        return 0.0
    mse = sum((expected - predicted) ** 2 for expected, predicted in zip(y_true, y_pred)) / len(y_true)
    return sqrt(mse)


def mean_absolute_percentage_error(y_true: list[float], y_pred: list[float]) -> float:
    if not y_true:
        return 0.0
    epsilon = 1e-10
    return sum(
        abs((expected - predicted) / max(abs(expected), epsilon))
        for expected, predicted in zip(y_true, y_pred)
    ) / len(y_true)


def r2_score(y_true: list[float], y_pred: list[float]) -> float:
    if not y_true:
        return 0.0
    y_true_mean = sum(y_true) / len(y_true)
    ss_res = sum((expected - predicted) ** 2 for expected, predicted in zip(y_true, y_pred))
    ss_tot = sum((expected - y_true_mean) ** 2 for expected in y_true)
    if ss_tot == 0:
        return 0.0
    return 1 - (ss_res / ss_tot)


# --- Evaluation Logic ---

def load_model(path: str = "models/model.json") -> dict[str, Any]:
    model_path = project_root() / path
    if not model_path.exists():
        raise FileNotFoundError("Model not found. Run train.py first.")
    return json.loads(model_path.read_text(encoding="utf-8"))


def evaluate_classification(rows: list[dict[str, Any]], model: dict[str, Any]) -> dict[str, Any]:
    target = model["target_column"]
    prediction = model["prediction"]
    y_true = [row.get(target) for row in rows if row.get(target) not in (None, "")]
    y_pred = [prediction] * len(y_true)

    if not y_true:
        return {"samples": 0, "metric": "accuracy", "accuracy": 0}

    pos_label = prediction
    metrics = {
        "samples": len(y_true),
        "metric": "accuracy",
        "accuracy": accuracy(y_true, y_pred),
        "precision": precision(y_true, y_pred, positive_label=pos_label),
        "recall": recall(y_true, y_pred, positive_label=pos_label),
        "f1_score": f1_score(y_true, y_pred, positive_label=pos_label),
        "confusion_matrix": confusion_counts(y_true, y_pred, positive_label=pos_label),
        "predicted_class": prediction,
    }
    return metrics


def evaluate_regression(rows: list[dict[str, Any]], model: dict[str, Any]) -> dict[str, Any]:
    target = model["target_column"]
    try:
        prediction = float(model["prediction"])
    except (ValueError, TypeError):
        prediction = 0.0

    y_true = []
    for row in rows:
        val = row.get(target)
        if val not in (None, ""):
            try:
                y_true.append(float(val))
            except (ValueError, TypeError):
                continue

    y_pred = [prediction] * len(y_true)
    if not y_true:
        return {"samples": 0, "metric": "rmse", "rmse": 0}

    metrics = {
        "samples": len(y_true),
        "metric": "rmse",
        "rmse": root_mean_squared_error(y_true, y_pred),
        "mae": mean_absolute_error(y_true, y_pred),
        "mape": mean_absolute_percentage_error(y_true, y_pred),
        "r2": r2_score(y_true, y_pred),
        "predicted_value": prediction,
    }
    return metrics


def main() -> None:
    config = load_config()
    rows = load_csv(config["data"]["processed_path"])
    model = load_model()

    task = config["project"]["task"]
    model_type = model.get("model_type", "unknown")
    lang = config.get("project", {}).get("language", "en")

    metrics: dict[str, Any] = {}
    is_ts = (task == "timeseries")

    if task == "unsupervised":
        metrics = {
            "samples": len(rows),
            "metric": "silhouette_placeholder",
            "silhouette_placeholder": 0.0,
            "note": "Clustering evaluation (e.g. Silhouette Score) requires cluster assignments."
        }
    elif task == "vision":
        metrics = {
            "samples": len(rows),
            "metric": "mAP_placeholder",
            "mAP_placeholder": 0.0,
            "note": "Vision evaluation (e.g. mAP for detection) not implemented in baseline."
        }
    elif task == "bandit":
        metrics = {
            "metric": "cumulative_reward",
            "cumulative_reward": 0.0,
            "note": "Multi-Armed Bandit evaluation requires simulation history or off-policy logs."
        }
    elif model_type in ("majority_class_baseline", "classifier"):
        metrics = evaluate_classification(rows, model)
    elif model_type in ("mean_value_baseline", "regressor") or is_ts:
        metrics = evaluate_regression(rows, model)
        if is_ts:
            metrics["note"] = "Backtesting not implemented. Evaluation uses a simple global split/baseline."
    else:
        metrics = {
            "samples": len(rows),
            "metric": "none",
            "note": f"No specific evaluation implemented for task '{task}' and model '{model_type}'."
        }

    output_path = project_root() / "reports/metrics.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")

    report_path = project_root() / "reports/evaluation-report.md"
    report_content = generate_markdown_report(metrics, model, task, lang)
    report_path.write_text(report_content, encoding="utf-8")

    print(f"Metrics saved at {output_path.relative_to(project_root())}")
    print(f"Report saved at {report_path.relative_to(project_root())}")
    print(json.dumps(metrics, indent=2, ensure_ascii=False))

    if config.get("tracking", {}).get("enabled_mlflow"):
        log_to_mlflow(metrics, model, output_path)


def generate_markdown_report(metrics: dict[str, Any], model: dict[str, Any], task: str, lang: str) -> str:
    model_type = model.get("model_type", "N/A")
    primary_metric = metrics.get("metric", "N/A")
    primary_value = metrics.get(primary_metric, "N/A")

    if lang == "pt-BR":
        title = "Relatório de Avaliação"
        summary_header = "Resumo"
        details_header = "Detalhes e Interpretação"
        model_label = "Modelo"
        samples_label = "Amostras"
        metric_label = "Métrica Principal"
        value_label = "Valor"

        interpretation = ""
        if primary_metric == "accuracy":
            interpretation = f"A acurácia de {primary_value:.2%} representa o desempenho do modelo de 'classe majoritária'. Qualquer modelo futuro deve superar este valor para ser útil."
        elif primary_metric == "rmse":
            interpretation = f"O RMSE de {primary_value:.4f} é baseado na predição do valor médio. É o erro padrão a ser superado por modelos de regressão mais complexos."

        if metrics.get("note"):
            interpretation += f"\n\n**Nota**: {metrics['note']}"
    else:
        title = "Evaluation Report"
        summary_header = "Summary"
        details_header = "Details and Interpretation"
        model_label = "Model"
        samples_label = "Samples"
        metric_label = "Primary Metric"
        value_label = "Value"

        interpretation = ""
        if primary_metric == "accuracy":
            interpretation = f"The accuracy of {primary_value:.2%} represents the 'majority class' baseline performance. Any future model must beat this score to be considered useful."
        elif primary_metric == "rmse":
            interpretation = f"The RMSE of {primary_value:.4f} is based on predicting the mean value. This is the baseline error to be beat by more complex regression models."

        if metrics.get("note"):
            interpretation += f"\n\n**Note**: {metrics['note']}"

    content = f"""# {title}

## {summary_header}
- **{model_label}**: {model_type}
- **{samples_label}**: {metrics.get("samples", 0)}
- **{metric_label}**: {primary_metric}
- **{value_label}**: {primary_value}

## {details_header}
{interpretation}

```json
{json.dumps(metrics, indent=2, ensure_ascii=False)}
```
"""
    return content


def log_to_mlflow(metrics: dict[str, Any], model: dict[str, Any], metrics_path: Path) -> None:
    try:
        import mlflow
        with mlflow.start_run(run_name="evaluation"):
            for k, v in metrics.items():
                if isinstance(v, (int, float)):
                    mlflow.log_metric(k, v)
            if metrics_path.exists():
                mlflow.log_artifact(str(metrics_path))
    except ImportError:
        pass
    except Exception as e:
        print(f"MLflow tracking failed: {e}")


if __name__ == "__main__":
    main()
