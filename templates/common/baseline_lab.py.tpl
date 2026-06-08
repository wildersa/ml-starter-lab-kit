from __future__ import annotations

import json
import sys
from typing import Any

import pandas as pd
try:
    from sklearn.dummy import DummyClassifier, DummyRegressor
    from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

from .core.config import load_config, project_root

class BaselineLab:
    def __init__(self, eda_summary: dict[str, Any], problem_profile: dict[str, Any], config: dict[str, Any]):
        self.eda = eda_summary
        self.profile = problem_profile
        self.config = config
        self.lang = problem_profile.get("language", "en")
        self.t = {
            "en": {
                "report_title": "Baseline Lab Results",
                "intro": "A baseline provides a simple benchmark to compare against more complex models.",
                "status_running": "Running baseline for {task}...",
                "status_complete": "Baseline results saved.",
                "eda_prerequisite": "Baseline Lab requires an EDA summary. Please run EDA first:\n  python -m {pkg}.lab eda",
                "sklearn_missing": "scikit-learn is required for Baseline Lab. Please install it with 'pip install scikit-learn'.",
                "task_unsupported": "Baseline Lab currently supports classification and regression tasks.",
                "model_name": "Baseline Model",
                "metric_name": "Metric",
                "metric_value": "Value",
                "summary_section": "## Summary",
                "results_section": "## Results",
                "why_baseline_section": "## Why this Baseline?",
                "why_baseline_text": "We use a 'Dummy' strategy to see how a model performs using only simple rules (like always predicting the most frequent class or the mean value), without actually 'learning' from features. Any real model must significantly outperform this baseline.",
            },
            "pt-BR": {
                "report_title": "Resultados do Baseline Lab",
                "intro": "Um baseline fornece um ponto de referência simples para comparar com modelos mais complexos.",
                "status_running": "Executando baseline para {task}...",
                "status_complete": "Resultados do baseline salvos.",
                "eda_prerequisite": "O Baseline Lab exige um resumo de EDA. Por favor, execute a EDA primeiro:\n  python -m {pkg}.lab eda",
                "sklearn_missing": "O scikit-learn é necessário para o Baseline Lab. Instale-o com 'pip install scikit-learn'.",
                "task_unsupported": "O Baseline Lab atualmente suporta tarefas de classificação e regressão.",
                "model_name": "Modelo Baseline",
                "metric_name": "Métrica",
                "metric_value": "Valor",
                "summary_section": "## Resumo",
                "results_section": "## Resultados",
                "why_baseline_section": "## Por que este Baseline?",
                "why_baseline_text": "Usamos uma estratégia 'Dummy' para ver como um modelo se comporta usando apenas regras simples (como sempre prever a classe mais frequente ou o valor médio), sem realmente 'aprender' com as features. Qualquer modelo real deve superar significativamente este baseline.",
            }
        }[self.lang]

    def run(self) -> tuple[dict[str, Any], str]:
        if not SKLEARN_AVAILABLE:
            print(self.t["sklearn_missing"])
            sys.exit(1)

        task = self.config.get("project", {}).get("task")
        goal = self.profile.get("goal", "").lower()
        target_col = self.config.get("target", {}).get("column")
        raw_path = self.config.get("data", {}).get("raw_path")

        print(self.t["status_running"].format(task=task))

        # Load data
        try:
            df = pd.read_csv(project_root() / raw_path)
        except Exception as e:
            print(f"Error loading dataset: {e}")
            sys.exit(1)

        if target_col not in df.columns:
            print(f"Error: Target column '{target_col}' not found in dataset.")
            sys.exit(1)

        df = df.dropna(subset=[target_col])
        y = df[target_col]
        # For simple baseline we don't need X, but Dummy models might expect it
        X = df.drop(columns=[target_col])

        results = {
            "task": task,
            "target": target_col,
            "metrics": {}
        }

        # Determine if classification or regression
        # Heuristic: use goal first, then fallback to target data type if goal is ambiguous
        is_classification = any(kw in goal for kw in ["category", "categoria", "classify", "classificar", "churn", "subscribed", "yes/no"])
        is_regression = any(kw in goal for kw in ["number", "número", "price", "value", "preço", "valor", "amount", "quantia"])

        # Refine based on data type if not strictly determined by goal keywords
        if not is_classification and not is_regression:
            if pd.api.types.is_numeric_dtype(y) and y.nunique() > 10:
                is_regression = True
            else:
                is_classification = True

        if is_classification:
            model = DummyClassifier(strategy="most_frequent")
            model.fit(X, y)
            y_pred = model.predict(X)

            acc = accuracy_score(y, y_pred)
            results["model_type"] = "DummyClassifier (most_frequent)"
            results["metrics"]["accuracy"] = float(acc)

        elif is_regression:
            model = DummyRegressor(strategy="mean")
            model.fit(X, y)
            y_pred = model.predict(X)

            mae = mean_absolute_error(y, y_pred)
            r2 = r2_score(y, y_pred)
            results["model_type"] = "DummyRegressor (mean)"
            results["metrics"]["mae"] = float(mae)
            results["metrics"]["r2"] = float(r2)
        else:
            print(self.t["task_unsupported"])
            return {}, ""

        # Build Markdown report
        md = [
            f"# {self.t['report_title']}",
            "",
            self.t["intro"],
            "",
            self.t["summary_section"],
            f"- **{self.t['model_name']}**: {results['model_type']}",
            f"- **Target**: {target_col}",
            "",
            self.t["results_section"],
            f"| {self.t['metric_name']} | {self.t['metric_value']} |",
            f"| :--- | :--- |"
        ]

        for m_name, m_val in results["metrics"].items():
            md.append(f"| {m_name.upper()} | {m_val:.4f} |")

        md.append("")
        md.append(self.t["why_baseline_section"])
        md.append(self.t["why_baseline_text"])

        return results, "\n".join(md)

def main():
    root = project_root()
    eda_path = root / "configs/eda_summary.json"

    # Language detection fallback
    lang = "en"
    profile_path = root / "configs/problem_profile.json"
    if profile_path.exists():
        try:
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
            lang = profile.get("language", "en")
        except:
            profile = {"language": "en"}
    else:
        profile = {"language": "en"}

    try:
        config = load_config()
        pkg = config.get("project", {}).get("package", "your_package")
    except Exception:
        pkg = "your_package"

    if not eda_path.exists():
        msgs = {
            "en": "Baseline Lab requires an EDA summary. Please run EDA first:\n  python -m {pkg}.lab eda",
            "pt-BR": "O Baseline Lab exige um resumo de EDA. Por favor, execute a EDA primeiro:\n  python -m {pkg}.lab eda"
        }
        print(msgs.get(lang, msgs["en"]).format(pkg=pkg))
        return

    try:
        with open(eda_path, "r", encoding="utf-8") as f:
            eda_summary = json.load(f)

        lab = BaselineLab(eda_summary, profile, config)
        results, report_md = lab.run()

        if not results:
            return

        # Create artifacts
        results_path = root / "configs/baseline_results.json"
        results_path.parent.mkdir(parents=True, exist_ok=True)
        with open(results_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        report_path = root / "reports/baseline-results.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_md)

        print(lab.t["status_complete"])
        print(f"- {results_path}")
        print(f"- {report_path}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except json.JSONDecodeError:
        print(f"Error: Could not parse EDA summary at {eda_path}")
    except Exception as e:
        print(f"Error in Baseline Lab: {e}")

if __name__ == "__main__":
    main()
