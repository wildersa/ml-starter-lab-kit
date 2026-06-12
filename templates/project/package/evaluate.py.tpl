from __future__ import annotations

import json
from collections import Counter
from typing import Any

from .core.config import load_config, project_root
from .core.data import load_csv

TRANSLATIONS = {
    "en": {
        "report_title": "Evaluation Report",
        "summary_h": "## Summary",
        "metrics_h": "## Metrics",
        "interpretation_h": "## Interpretation",
        "next_experiment_h": "## Next experiment",
        "how_to_read_h": "## How to read this report",
        "project_name": "**Project:** {name}",
        "task_type": "**Task:** {task}",
        "model_type": "**Model type:** {model_type}",
        "samples": "**Samples evaluated:** {count}",
        "accuracy_desc": "Accuracy represents the proportion of correct predictions out of the total number of samples.",
        "baseline_note": "This evaluation used a **{baseline_type}** baseline as a performance floor.",
        "interpretation_supervised": "An accuracy of {value:.2%} means the model correctly predicted the class for {value:.2%} of the test cases.",
        "interpretation_regression": "An RMSE of {value:.4f} represents the average magnitude of error in your predictions, in the same units as your target.",
        "next_steps_supervised": "1. Try adding more features in `features.py`.\n2. Experiment with different model types in `train.py`.\n3. Check for data leakage if accuracy is suspiciously high.",
        "next_steps_regression": "1. Look for non-linear relationships in your features.\n2. Try normalizing or scaling numeric features.\n3. Identify and handle outliers that might be inflating the error.",
        "how_to_read_text": "This report summarizes the performance of your model compared to a simple baseline. Different tasks use different metrics: accuracy for classification and RMSE for regression.",
        "no_metrics": "No metrics available to report."
    },
    "pt-BR": {
        "report_title": "Relatório de Avaliação",
        "summary_h": "## Resumo",
        "metrics_h": "## Métricas",
        "interpretation_h": "## Interpretação",
        "next_experiment_h": "## Próximo experimento",
        "how_to_read_h": "## Como ler este relatório",
        "project_name": "**Projeto:** {name}",
        "task_type": "**Tarefa:** {task}",
        "model_type": "**Tipo de modelo:** {model_type}",
        "samples": "**Amostras avaliadas:** {count}",
        "accuracy_desc": "A acurácia representa a proporção de previsões corretas em relação ao número total de amostras.",
        "baseline_note": "Esta avaliação utilizou um baseline do tipo **{baseline_type}** como um patamar mínimo de desempenho.",
        "interpretation_supervised": "Uma acurácia de {value:.2%} significa que o modelo previu corretamente a classe para {value:.2%} dos casos de teste.",
        "interpretation_regression": "Um RMSE de {value:.4f} representa a magnitude média do erro em suas previsões, nas mesmas unidades do seu alvo.",
        "next_steps_supervised": "1. Tente adicionar mais features em `features.py`.\n2. Experimente diferentes tipos de modelos em `train.py`.\n3. Verifique se há vazamento de dados (leakage) se a acurácia for suspeitosamente alta.",
        "next_steps_regression": "1. Procure por relações não lineares em suas features.\n2. Tente normalizar ou escalar features numéricas.\n3. Identifique e trate outliers que possam estar inflando o erro.",
        "how_to_read_text": "Este relatório resume o desempenho do seu modelo em comparação a um baseline simples. Diferentes tarefas usam métricas diferentes: acurácia para classificação e RMSE para regressão.",
        "no_metrics": "Nenhuma métrica disponível para relatar."
    }
}


def generate_report(metrics: dict[str, Any], config: dict[str, Any], problem_profile: dict[str, Any]) -> str:
    lang = problem_profile.get("language", "en")
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])

    project_name = config.get("project", {}).get("name", "Unknown")
    task = config.get("project", {}).get("task", "Unknown")
    model_type = metrics.get("model_type", "Unknown")

    md = [
        f"# {t['report_title']}",
        "",
        t["summary_h"],
        t["project_name"].format(name=project_name),
        t["task_type"].format(task=task),
        t["model_type"].format(model_type=model_type),
        t["samples"].format(count=metrics.get("samples", 0)),
        t["baseline_note"].format(baseline_type=model_type),
        ""
    ]

    md.append(t["metrics_h"])
    if "accuracy" in metrics:
        md.append(f"- **Accuracy:** {metrics['accuracy']:.4f}")
        md.append("")
        md.append(t["interpretation_h"])
        md.append(t["interpretation_supervised"].format(value=metrics["accuracy"]))
        md.append("")
        md.append(t["next_experiment_h"])
        md.append(t["next_steps_supervised"])
    elif "rmse" in metrics:
        md.append(f"- **RMSE:** {metrics['rmse']:.4f}")
        md.append("")
        md.append(t["interpretation_h"])
        md.append(t["interpretation_regression"].format(value=metrics["rmse"]))
        md.append("")
        md.append(t["next_experiment_h"])
        md.append(t["next_steps_regression"])
    else:
        md.append(f"- {t['no_metrics']}")
        md.append("")
        md.append(t["interpretation_h"])
        md.append(str(metrics.get("note", "No specific interpretation available.")))
        md.append("")
        md.append(t["next_experiment_h"])
        md.append("1. Review your data features.\n2. Try different algorithm parameters.")

    md.append("")
    md.append(t["how_to_read_h"])
    md.append(t["how_to_read_text"])

    return "\n".join(md)


def load_model(path: str = "models/model.json") -> dict[str, object]:
    model_path = project_root() / path

    if not model_path.exists():
        raise FileNotFoundError("Model not found. Run train.py first.")

    return json.loads(model_path.read_text(encoding="utf-8"))


def evaluate_majority_baseline(rows: list[dict[str, Any]], model: dict[str, Any]) -> dict[str, Any]:
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


def evaluate_mean_baseline(rows: list[dict[str, Any]], model: dict[str, Any]) -> dict[str, Any]:
    target = model["target_column"]
    prediction = float(model["prediction"])

    y_true = []
    for row in rows:
        val = row.get(target)
        if val not in (None, ""):
            try:
                y_true.append(float(val))
            except (ValueError, TypeError):
                continue

    if not y_true:
        return {"metric": "rmse", "rmse": 0, "samples": 0}

    mse = sum((y - prediction) ** 2 for y in y_true) / len(y_true)
    rmse = mse ** 0.5

    return {
        "metric": "rmse",
        "rmse": rmse,
        "samples": len(y_true),
        "prediction": prediction,
    }


def main() -> None:
    config = load_config()
    rows = load_csv(config["data"]["processed_path"])
    model = load_model()

    profile_path = project_root() / "configs/problem_profile.json"
    if profile_path.exists():
        problem_profile = json.loads(profile_path.read_text(encoding="utf-8"))
    else:
        problem_profile = {"language": "en"}

    if model.get("model_type") == "majority_class_baseline":
        metrics = evaluate_majority_baseline(rows, model)
        metrics["model_type"] = "majority_class_baseline"
    elif model.get("model_type") == "mean_value_baseline":
        metrics = evaluate_mean_baseline(rows, model)
        metrics["model_type"] = "mean_value_baseline"
    else:
        metrics = {
            "note": "Evaluation not yet implemented for this model type.",
            "model_type": model.get("model_type"),
        }

    reports_dir = project_root() / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    metrics_path = reports_dir / "metrics.json"
    metrics_path.write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")

    report_md = generate_report(metrics, config, problem_profile)
    report_path = reports_dir / "evaluation-report.md"
    report_path.write_text(report_md, encoding="utf-8")

    print(f"Metrics saved at {metrics_path}")
    print(f"Report saved at {report_path}")
    print(json.dumps(metrics, indent=2, ensure_ascii=False))

    # MLflow Tracking
    if config.get("tracking", {}).get("enabled_mlflow"):
        try:
            import mlflow

            with mlflow.start_run(run_name="baseline_evaluation"):
                # Log metrics
                if "accuracy" in metrics:
                    mlflow.log_metric("accuracy", metrics["accuracy"])
                if "rmse" in metrics:
                    mlflow.log_metric("rmse", metrics["rmse"])

                mlflow.log_metric("samples", metrics.get("samples", 0))

                # Log artifacts
                if metrics_path.exists():
                    mlflow.log_artifact(str(metrics_path))
                if report_path.exists():
                    mlflow.log_artifact(str(report_path))

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
