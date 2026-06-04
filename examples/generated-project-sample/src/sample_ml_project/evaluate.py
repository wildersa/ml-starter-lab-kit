from __future__ import annotations

import json
from collections import Counter

from .config import load_config, project_root
from .data import load_csv


def load_model(path: str = "models/model.json") -> dict[str, object]:
    model_path = project_root() / path

    if not model_path.exists():
        raise FileNotFoundError("Modelo não encontrado. Rode train.py primeiro.")

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
            "note": "Avaliação ainda não implementada para este tipo de modelo.",
            "model_type": model.get("model_type"),
        }

    output = project_root() / "reports/metrics.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")

    print("Métricas salvas em reports/metrics.json")
    print(json.dumps(metrics, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
