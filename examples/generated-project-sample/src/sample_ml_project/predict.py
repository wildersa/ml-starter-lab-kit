from __future__ import annotations

import json
from .config import project_root


def load_model(path: str = "models/model.json") -> dict[str, object]:
    model_path = project_root() / path

    if not model_path.exists():
        raise FileNotFoundError("Model not found. Run train.py first.")

    return json.loads(model_path.read_text(encoding="utf-8"))


def predict_one(input_row: dict[str, object]) -> dict[str, object]:
    model = load_model()

    if model.get("model_type") == "majority_class_baseline":
        return {
            "prediction": model["prediction"],
            "model_type": model["model_type"],
            "reason": "majority class baseline",
        }

    return {
        "prediction": None,
        "model_type": model.get("model_type"),
        "reason": "predict not yet implemented for this model",
    }


def main() -> None:
    example = {"example": "value"}
    print(json.dumps(predict_one(example), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
