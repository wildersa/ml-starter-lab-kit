from __future__ import annotations

import json
import re
from pathlib import Path


TASKS = {
    "1": "generic",
    "2": "supervised",
    "3": "unsupervised",
    "4": "timeseries",
    "5": "datathon",
}


def ask(prompt: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{prompt}{suffix}: ").strip()
    return value or (default or "")


def ask_yes_no(prompt: str, default: bool = True) -> bool:
    default_label = "S/n" if default else "s/N"
    value = input(f"{prompt} [{default_label}]: ").strip().lower()

    if not value:
        return default

    return value in {"s", "sim", "y", "yes"}


def choose_task() -> str:
    print()
    print("Tipo de projeto:")
    print("1. generic       - estrutura genérica de ML")
    print("2. supervised    - classificação/regressão")
    print("3. unsupervised  - PCA/K-Means/clustering")
    print("4. timeseries    - séries temporais/LSTM")
    print("5. datathon      - estrutura expandida para Fase 5/Datathon")

    while True:
        choice = ask("Escolha uma opção", "2")
        if choice in TASKS:
            return TASKS[choice]
        if choice in TASKS.values():
            return choice
        print("Opção inválida.")


def normalize_package_name(value: str) -> str:
    value = value.strip().lower().replace("-", "_").replace(" ", "_")
    value = re.sub(r"[^a-z0-9_]", "", value)
    value = re.sub(r"_+", "_", value).strip("_")

    if not value:
        value = "ml_project"

    if value[0].isdigit():
        value = f"ml_{value}"

    return value


def render(content: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        content = content.replace("{{" + key + "}}", value)
    return content


def write_text(path: Path, content: str, *, force: bool) -> bool:
    if path.exists() and not force:
        return False

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.lstrip(), encoding="utf-8")
    return True


def touch_gitkeep(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    gitkeep = path / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.write_text("", encoding="utf-8")


def create_dirs(root: Path, package_name: str, task: str, include_docs: bool) -> None:
    dirs = [
        "configs",
        "data/raw",
        "data/processed",
        "data/external",
        "notebooks",
        "models",
        "reports/figures",
        f"src/{package_name}",
        "tests",
    ]

    if include_docs:
        dirs.append("docs")

    if task == "datathon":
        dirs.extend([
            "data/kaggle",
            "data/synthetic_enrichment",
            "data/golden_set",
            "infra/azure",
            "docs",
            "reports",
        ])

    for directory in dirs:
        touch_gitkeep(root / directory)


def create_config(root: Path, values: dict[str, str], *, force: bool) -> None:
    task = values["TASK"]

    config: dict[str, object] = {
        "project": {
            "name": values["PROJECT_NAME"],
            "package": values["PACKAGE_NAME"],
            "task": task
        },
        "data": {
            "raw_path": values["DATASET_PATH"],
            "processed_path": "data/processed/modeling_table.csv"
        },
        "target": {
            "column": values["TARGET_COLUMN"]
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

    if task == "datathon":
        config["datathon"] = {
            "arms": [
                "sem_oferta",
                "educacao_financeira",
                "simulador_credito"
            ],
            "policy_version": "policy-demo-v0",
            "explore_rate": 0.05,
            "reward_columns": [
                "click",
                "started_journey",
                "conversion"
            ]
        }

    write_text(
        root / "configs/config.json",
        json.dumps(config, indent=2, ensure_ascii=False),
        force=force,
    )


def create_readme(root: Path, values: dict[str, str], *, force: bool) -> None:
    content = '''
# {{PROJECT_NAME}}

Projeto de Machine Learning gerado com `ml-starter-kit-builder`.

## Tipo de projeto

`{{TASK}}`

## Estrutura

```text
configs/             configurações em JSON
data/raw/            dados originais
data/processed/      dados tratados
notebooks/           exploração e análise
src/{{PACKAGE_NAME}}/ código principal
models/              modelos treinados
reports/             métricas, figuras e relatórios
tests/               testes mínimos
```

## Fluxo sugerido

```text
1. Coloque o dataset em data/raw/
2. Ajuste configs/config.json
3. Faça a EDA no notebook
4. Edite src/{{PACKAGE_NAME}}/features.py
5. Treine o modelo
6. Avalie os resultados
7. Documente limitações e próximos passos
```

## Comandos sugeridos

```bash
python -m src.{{PACKAGE_NAME}}.data
python -m src.{{PACKAGE_NAME}}.train
python -m src.{{PACKAGE_NAME}}.evaluate
```
'''
    write_text(root / "README.md", render(content, values), force=force)


def create_package_files(root: Path, values: dict[str, str], *, force: bool) -> None:
    package = values["PACKAGE_NAME"]
    base = root / "src" / package

    files = {
        "__init__.py": "# Pacote principal do projeto.\n",
        "config.py": '''
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_config(path: str | Path = "configs/config.json") -> dict[str, Any]:
    config_path = project_root() / path

    if not config_path.exists():
        raise FileNotFoundError(f"Config não encontrado: {config_path}")

    return json.loads(config_path.read_text(encoding="utf-8"))
''',
        "data.py": '''
from __future__ import annotations

import csv
from pathlib import Path

from .config import load_config, project_root


def load_csv(path: str | Path) -> list[dict[str, str]]:
    file_path = project_root() / path

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset não encontrado: {file_path}")

    with file_path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def save_csv(rows: list[dict[str, object]], path: str | Path) -> None:
    if not rows:
        raise ValueError("Nenhuma linha para salvar.")

    file_path = project_root() / path
    file_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(rows[0].keys())

    with file_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    config = load_config()
    raw_path = config["data"]["raw_path"]
    processed_path = config["data"]["processed_path"]

    rows = load_csv(raw_path)
    print(f"Linhas carregadas: {len(rows)}")

    if rows:
        print(f"Colunas: {list(rows[0].keys())}")

    save_csv(rows, processed_path)
    print(f"Arquivo processado salvo em: {processed_path}")


if __name__ == "__main__":
    main()
''',
        "features.py": '''
from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime


def safe_float(value: object) -> float | None:
    if value is None:
        return None

    try:
        return float(str(value).replace(",", "."))
    except ValueError:
        return None


def add_ratio_feature(
    rows: list[dict[str, object]],
    *,
    name: str,
    numerator: str,
    denominator: str,
) -> list[dict[str, object]]:
    for row in rows:
        num = safe_float(row.get(numerator))
        den = safe_float(row.get(denominator))

        if num is None or den in (None, 0):
            row[name] = None
        else:
            row[name] = num / den

    return rows


def add_datetime_parts(
    rows: list[dict[str, object]],
    *,
    column: str,
    date_format: str | None = None,
) -> list[dict[str, object]]:
    for row in rows:
        raw = row.get(column)

        if not raw:
            continue

        try:
            dt = (
                datetime.strptime(str(raw), date_format)
                if date_format
                else datetime.fromisoformat(str(raw))
            )
        except ValueError:
            continue

        row[f"{column}_year"] = dt.year
        row[f"{column}_month"] = dt.month
        row[f"{column}_day"] = dt.day
        row[f"{column}_dayofweek"] = dt.weekday()
        row[f"{column}_is_weekend"] = dt.weekday() >= 5

    return rows


def add_lag_features(
    rows: list[dict[str, object]],
    *,
    column: str,
    lags: Iterable[int],
    order_by: str | None = None,
    groupby: str | None = None,
) -> list[dict[str, object]]:
    sorted_rows = sorted(
        rows,
        key=lambda r: (
            r.get(groupby, "") if groupby else "",
            r.get(order_by, "") if order_by else "",
        ),
    )

    groups: dict[object, list[dict[str, object]]] = {}
    for row in sorted_rows:
        key = row.get(groupby) if groupby else "__all__"
        groups.setdefault(key, []).append(row)

    for group_rows in groups.values():
        for index, row in enumerate(group_rows):
            for lag in lags:
                lag_index = index - lag
                row[f"{column}_lag_{lag}"] = (
                    group_rows[lag_index].get(column)
                    if lag_index >= 0
                    else None
                )

    return rows


def add_rolling_mean_features(
    rows: list[dict[str, object]],
    *,
    column: str,
    windows: Iterable[int],
    order_by: str | None = None,
    groupby: str | None = None,
    shift: int = 1,
) -> list[dict[str, object]]:
    sorted_rows = sorted(
        rows,
        key=lambda r: (
            r.get(groupby, "") if groupby else "",
            r.get(order_by, "") if order_by else "",
        ),
    )

    groups: dict[object, list[dict[str, object]]] = {}
    for row in sorted_rows:
        key = row.get(groupby) if groupby else "__all__"
        groups.setdefault(key, []).append(row)

    for group_rows in groups.values():
        values = [safe_float(row.get(column)) for row in group_rows]

        for index, row in enumerate(group_rows):
            for window in windows:
                end = max(0, index - shift + 1)
                start = max(0, end - window)
                history = [v for v in values[start:end] if v is not None]

                row[f"{column}_rolling_mean_{window}"] = (
                    sum(history) / len(history)
                    if history
                    else None
                )

    return rows


def apply_configured_features(
    rows: list[dict[str, object]],
    feature_config: dict[str, object],
) -> list[dict[str, object]]:
    rows = [dict(row) for row in rows]

    for rule in feature_config.get("calculated_features", []):
        if not rule.get("enabled", False):
            continue

        rule_type = rule.get("type")

        if rule_type == "ratio":
            rows = add_ratio_feature(
                rows,
                name=rule["name"],
                numerator=rule["numerator"],
                denominator=rule["denominator"],
            )

        elif rule_type == "datetime_parts":
            rows = add_datetime_parts(
                rows,
                column=rule["column"],
            )

        elif rule_type == "lag":
            rows = add_lag_features(
                rows,
                column=rule["column"],
                lags=rule["lags"],
                groupby=rule.get("groupby"),
                order_by=rule.get("order_by"),
            )

        elif rule_type == "rolling_mean":
            rows = add_rolling_mean_features(
                rows,
                column=rule["column"],
                windows=rule["windows"],
                groupby=rule.get("groupby"),
                order_by=rule.get("order_by"),
                shift=rule.get("shift", 1),
            )

    drop_columns = set(feature_config.get("drop_columns", []))
    if drop_columns:
        for row in rows:
            for column in drop_columns:
                row.pop(column, None)

    return rows
''',
        "train.py": '''
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from .config import load_config, project_root
from .data import load_csv
from .features import apply_configured_features


def train_baseline_classifier(rows: list[dict[str, object]], target_column: str) -> dict[str, object]:
    if not target_column:
        raise ValueError("target_column não configurado.")

    values = [row.get(target_column) for row in rows if row.get(target_column) not in (None, "")]
    if not values:
        raise ValueError(f"Nenhum valor encontrado para target: {target_column}")

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

    if task in {"generic", "supervised", "datathon"}:
        model = train_baseline_classifier(rows, target_column)
    elif task == "unsupervised":
        model = {
            "model_type": "unsupervised_placeholder",
            "note": "Adicione PCA/K-Means com scikit-learn aqui, se o projeto usar scikit-learn."
        }
    elif task == "timeseries":
        model = {
            "model_type": "timeseries_placeholder",
            "note": "Adicione LSTM/Keras ou outro modelo temporal aqui, se o projeto usar deep learning."
        }
    else:
        raise ValueError(f"Task não suportada: {task}")

    save_model(model)
    print("Modelo salvo em models/model.json")
    print(json.dumps(model, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
''',
        "evaluate.py": '''
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
''',
        "predict.py": '''
from __future__ import annotations

import json
from .config import project_root


def load_model(path: str = "models/model.json") -> dict[str, object]:
    model_path = project_root() / path

    if not model_path.exists():
        raise FileNotFoundError("Modelo não encontrado. Rode train.py primeiro.")

    return json.loads(model_path.read_text(encoding="utf-8"))


def predict_one(input_row: dict[str, object]) -> dict[str, object]:
    model = load_model()

    if model.get("model_type") == "majority_class_baseline":
        return {
            "prediction": model["prediction"],
            "model_type": model["model_type"],
            "reason": "baseline de classe majoritária",
        }

    return {
        "prediction": None,
        "model_type": model.get("model_type"),
        "reason": "predict ainda não implementado para este modelo",
    }


def main() -> None:
    example = {"example": "value"}
    print(json.dumps(predict_one(example), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
''',
    }

    for rel, content in files.items():
        write_text(base / rel, content, force=force)


def create_tests(root: Path, values: dict[str, str], *, force: bool) -> None:
    package = values["PACKAGE_NAME"]
    content = f'''
from src.{package}.features import add_ratio_feature


def test_add_ratio_feature():
    rows = [
        {{"a": "10", "b": "2"}},
        {{"a": "10", "b": "0"}},
    ]

    result = add_ratio_feature(rows, name="a_por_b", numerator="a", denominator="b")

    assert result[0]["a_por_b"] == 5
    assert result[1]["a_por_b"] is None
'''
    write_text(root / "tests/test_features.py", content, force=force)


def create_notebook_placeholder(root: Path, *, force: bool) -> None:
    content = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# 01 - EDA\\n",
                    "\\n",
                    "Notebook inicial para análise exploratória.\\n",
                    "\\n",
                    "Sugestões:\\n",
                    "- tamanho da base;\\n",
                    "- tipos das colunas;\\n",
                    "- nulos;\\n",
                    "- distribuição do target;\\n",
                    "- vazamento de dados;\\n",
                    "- outliers;\\n",
                    "- primeiras hipóteses de features.\\n"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    write_text(
        root / "notebooks/01_eda.ipynb",
        json.dumps(content, indent=2, ensure_ascii=False),
        force=force,
    )


def create_docs(root: Path, values: dict[str, str], *, force: bool) -> None:
    docs = {
        "docs/data-dictionary.md": '''
# Dicionário de Dados

| Coluna | Tipo | Descrição | Uso no modelo | Observações |
|---|---|---|---|---|
| TODO | TODO | TODO | TODO | TODO |
''',
        "reports/modeling-notes.md": '''
# Notas de Modelagem

## Problema

TODO

## Baseline

TODO

## Features calculadas

TODO

## Métricas

TODO

## Limitações

TODO
''',
        ".gitignore": '''
__pycache__/
*.pyc
.venv/
.env
.ipynb_checkpoints/
models/*.pkl
models/*.joblib
data/raw/*
!data/raw/.gitkeep
data/processed/*
!data/processed/.gitkeep
''',
        ".env.example": '''
# Exemplo de variáveis de ambiente
# Não coloque segredos reais aqui.
''',
    }

    if values["TASK"] == "datathon":
        docs.update({
            "data/kaggle/README.md": '''
# Base Kaggle

Preencha:

- Link da base:
- Versão:
- Licença:
- Colunas usadas:
- Colunas descartadas:
- Risco de vazamento temporal:
- Justificativa da escolha:
''',
            "reports/data-generation.md": '''
# Geração de Dados Derivados

## Objetivo

Descrever como os dados sintéticos foram criados.

## Arquivos esperados

- `data/synthetic_enrichment/offer_catalog.sample.csv`
- `data/synthetic_enrichment/offer_events.sample.csv`
- `data/synthetic_enrichment/delayed_rewards.sample.csv`
- `data/golden_set/evaluation_cases.jsonl`

## Hipóteses

TODO

## Limitações

TODO
''',
            "docs/algorithmic-strategy.md": '''
# Estratégia Algorítmica

## Baseline

TODO

## Thompson Sampling

TODO

## UCB / LinUCB / Nilos-UCB

TODO

## Cold-start

TODO

## Delayed rewards

TODO
''',
            "docs/architecture-azure.md": '''
# Arquitetura Azure

```mermaid
flowchart LR
    U[Usuário/Avaliador] --> API[API ou CLI de decisão]
    API --> POL[Política adaptativa]
    POL --> DATA[Dados processados + enriquecimento sintético]
    API --> LOG[Log auditável]
    LOG --> OBS[Azure Monitor / App Insights / Log Analytics]
    POL --> MLOPS[Retreino, aprovação e promoção]
    SEC[Entra ID / Key Vault / Managed Identity] --> API
```

## Serviços escolhidos

TODO

## Trade-offs

TODO

## Escala e redução

TODO

## FinOps

TODO
''',
            "docs/model-card.md": '''
# Model Card

## Nome e versão

TODO

## Intended use

TODO

## Out-of-scope use

TODO

## Dados

TODO

## Métricas

TODO

## Riscos e limitações

TODO
''',
            "docs/system-card.md": '''
# System Card

## Escopo do sistema

TODO

## Fluxo de decisão

TODO

## Guardrails

TODO

## Riscos

- reward hacking;
- manipulação de contexto;
- viés de exposição;
- uso indevido do assistente;
- recomendação financeira autônoma indevida.

## Monitoramento

TODO
''',
            "docs/lgpd-plan.md": '''
# Plano LGPD

## Finalidade

TODO

## Base legal

TODO

## Minimização

TODO

## Retenção

TODO

## Logs e telemetria

TODO

## Incidentes

TODO
''',
            "docs/demo-day-pitch.md": '''
# Roteiro Demo Day

## Problema

TODO

## Abordagem

TODO

## Demo

TODO

## Evidências

TODO

## Riscos e governança

TODO

## Impacto e FinOps

TODO
''',
            "infra/azure/deployment-plan.md": '''
# Plano de Deploy Azure

## Ambiente local

TODO

## Arquitetura-alvo

TODO

## Serviços Azure

TODO

## Segurança

TODO

## Observabilidade

TODO

## Custos

TODO
''',
            "data/synthetic_enrichment/offer_catalog.sample.csv": '''
arm_id,arm_name,channel,description
sem_oferta,Sem oferta,app,Não exibir oferta
educacao_financeira,Educação financeira,app,Conteúdo educativo
simulador_credito,Simulador de crédito,web,CTA para simulação
''',
            "data/synthetic_enrichment/offer_events.sample.csv": '''
event_id,subject_key,channel,segment,chosen_arm,reward
evt_001,user_001,app,novo,educacao_financeira,1
evt_002,user_002,web,recorrente,sem_oferta,0
''',
            "data/synthetic_enrichment/delayed_rewards.sample.csv": '''
event_id,reward_type,reward_value,observed_after_days
evt_001,click,1,0
evt_001,conversion,0,7
''',
            "data/golden_set/evaluation_cases.jsonl": '''
{"case_id":"case_001","context":{"segment":"novo","channel":"app"},"expected_behavior":"selecionar braço elegível","pass_fail":"deve registrar decisão com versão de política"}
''',
        })

    for rel, content in docs.items():
        write_text(root / rel, content, force=force)


def create_pyproject(root: Path, values: dict[str, str], *, force: bool) -> None:
    content = '''
[project]
name = "{{PACKAGE_NAME}}"
version = "0.1.0"
description = "{{PROJECT_NAME}}"
requires-python = ">=3.11"

# Intencionalmente sem dependências.
# Adicione pandas, scikit-learn, xgboost, tensorflow, keras etc. somente quando o projeto precisar.

[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]
'''
    write_text(root / "pyproject.toml", render(content, values), force=force)


def print_summary(root: Path, values: dict[str, str]) -> None:
    print()
    print("Starter-kit criado.")
    print(f"Destino: {root.resolve()}")
    print(f"Projeto: {values['PROJECT_NAME']}")
    print(f"Pacote: {values['PACKAGE_NAME']}")
    print(f"Tipo: {values['TASK']}")
    print()
    print("Próximos passos:")
    print("1. Ajuste configs/config.json")
    print("2. Coloque seu dataset em data/raw/")
    print("3. Edite src/<pacote>/features.py")
    print("4. Rode:")
    print(f"   python -m src.{values['PACKAGE_NAME']}.data")
    print(f"   python -m src.{values['PACKAGE_NAME']}.train")
    print(f"   python -m src.{values['PACKAGE_NAME']}.evaluate")


def main() -> None:
    print("ML Starter Kit Builder")
    print("======================")

    default_project = Path.cwd().name
    project_name = ask("Nome do projeto", default_project)
    package_name = normalize_package_name(
        ask("Nome do pacote Python", normalize_package_name(project_name))
    )
    task = choose_task()

    dataset_path = ask("Caminho do dataset", "data/raw/dataset.csv")

    if task == "unsupervised":
        target_column = ""
    else:
        target_column = ask("Nome da coluna target", "target")

    output_dir = Path(ask("Diretório onde criar a estrutura", ".")).resolve()
    include_docs = ask_yes_no("Criar arquivos de documentação?", True)
    include_pyproject = ask_yes_no("Criar pyproject.toml sem dependências?", True)
    force = ask_yes_no("Sobrescrever arquivos existentes se houver conflito?", False)

    values = {
        "PROJECT_NAME": project_name,
        "PACKAGE_NAME": package_name,
        "TASK": task,
        "DATASET_PATH": dataset_path,
        "TARGET_COLUMN": target_column,
    }

    create_dirs(output_dir, package_name, task, include_docs)
    create_config(output_dir, values, force=force)
    create_readme(output_dir, values, force=force)
    create_package_files(output_dir, values, force=force)
    create_tests(output_dir, values, force=force)
    create_notebook_placeholder(output_dir, force=force)

    if include_docs:
        create_docs(output_dir, values, force=force)

    if include_pyproject:
        create_pyproject(output_dir, values, force=force)

    print_summary(output_dir, values)


if __name__ == "__main__":
    main()
