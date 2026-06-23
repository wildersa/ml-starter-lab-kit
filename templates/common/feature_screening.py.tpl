from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

try:
    import pandas as pd
    import numpy as np
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
    from sklearn.metrics import (
        accuracy_score,
        f1_score,
        mean_absolute_error,
        r2_score,
        roc_auc_score
    )
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    DEPENDENCIES_AVAILABLE = False
    _IMPORT_ERROR = str(e)

from .core.config import load_config, project_root

class FeatureScreeningLab:
    def __init__(self, problem_profile: dict[str, Any], config: dict[str, Any]):
        self.profile = problem_profile
        self.config = config
        self.lang = problem_profile.get("language", "en")
        self.t = {
            "en": {
                "report_title": "Diagnostic Model & Feature Importance",
                "intro": "This diagnostic step uses a Random Forest to quickly assess predictive signal and feature importance. It is NOT the final training pipeline.",
                "status_running": "Running diagnostic model for {task}...",
                "status_complete": "Diagnostic results saved.",
                "dependencies_missing": "pandas and scikit-learn are required for Feature Screening. Please install them with 'pip install pandas scikit-learn'.",
                "task_unsupported": "Feature Screening currently supports classification and regression tasks.",
                "metrics_section": "## 1. Diagnostic Metrics",
                "importance_section": "## 2. Feature Importance",
                "leakage_section": "## 3. Leakage Warnings",
                "appendix_section": "## 4. Educational Notes",
                "metric_name": "Metric",
                "metric_value": "Value",
                "feature_name": "Feature",
                "importance_value": "Importance",
                "leakage_warning": "SUSPICIOUS SIGNAL: Feature '{col}' has extremely high importance/signal. This often indicates target leakage (e.g., the feature contains information not available at prediction time).",
                "not_causal_warning": "WARNING: Feature importance shows statistical association, not necessarily causality. A high score doesn't mean changing this feature will cause the target to change.",
                "leakage_desc": "Leakage occurs when features contain information that would not be available in a real-world production setting.",
                "baseline_comparison": "Compared to naive baseline (Baseline Lab), this diagnostic model achieves:",
            },
            "pt-BR": {
                "report_title": "Modelo Diagnóstico e Importância de Features",
                "intro": "Este passo diagnóstico utiliza uma Random Forest para avaliar rapidamente o sinal preditivo e a importância das características. NÃO é o pipeline final de treinamento.",
                "status_running": "Executando modelo diagnóstico para {task}...",
                "status_complete": "Resultados diagnósticos salvos.",
                "dependencies_missing": "O pandas e o scikit-learn são necessários para a Triagem de Features (Feature Screening). Instale-os com 'pip install pandas scikit-learn'.",
                "task_unsupported": "A Triagem de Features atualmente suporta tarefas de classificação e regressão.",
                "metrics_section": "## 1. Métricas Diagnósticas",
                "importance_section": "## 2. Importância das Features",
                "leakage_section": "## 3. Avisos de Leakage",
                "appendix_section": "## 4. Notas Educacionais",
                "metric_name": "Métrica",
                "metric_value": "Valor",
                "feature_name": "Feature",
                "importance_value": "Importância",
                "leakage_warning": "SINAL SUSPEITO: A feature '{col}' tem importância/sinal extremamente alto. Isso geralmente indica leakage (vazamento) de dados (ex: a feature contém informações que não estariam disponíveis no momento da predição).",
                "not_causal_warning": "AVISO: A importância de features mostra associação estatística, não necessariamente causalidade. Um score alto não significa que alterar esta feature causará uma mudança no alvo.",
                "leakage_desc": "Leakage ocorre quando as features contêm informações que não estariam disponíveis em um cenário real de produção.",
                "baseline_comparison": "Comparado ao baseline ingênuo (Baseline Lab), este modelo diagnóstico alcança:",
            }
        }[self.lang]

    def _preprocess_for_diagnostic(self, df: pd.DataFrame, target_col: str) -> tuple[pd.DataFrame, pd.Series]:
        """Simple preprocessing for a quick diagnostic model."""
        # Drop rows with missing target
        df = df.dropna(subset=[target_col])
        y = df[target_col]
        X = df.drop(columns=[target_col])

        # Simple categorical handling: One-hot encode and drop non-numeric
        X = pd.get_dummies(X, drop_first=True)

        # Fill missing values with median for numeric
        for col in X.select_dtypes(include=[np.number]).columns:
            X[col] = X[col].fillna(X[col].median())

        # If there are still non-numeric columns, drop them for the diagnostic
        X = X.select_dtypes(include=[np.number])

        return X, y

    def run(self) -> dict[str, Any]:
        task = self.config.get("project", {}).get("task")
        target_col = self.config.get("target", {}).get("column")
        raw_path = self.config.get("data", {}).get("raw_path")

        print(self.t["status_running"].format(task=task))

        try:
            df = pd.read_csv(project_root() / raw_path)
        except Exception as e:
            print(f"Error loading dataset: {e}")
            sys.exit(1)

        if target_col not in df.columns:
            print(f"Error: Target column '{target_col}' not found.")
            sys.exit(1)

        X, y = self._preprocess_for_diagnostic(df, target_col)

        if X.empty:
             print("Error: No features available for diagnostic modeling.")
             sys.exit(1)

        # Split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Detect task type
        is_classification = False
        is_regression = False
        goal = self.profile.get("goal", "").lower()

        if any(kw in goal for kw in ["category", "categoria", "classify", "classificar"]):
            is_classification = True
        elif any(kw in goal for kw in ["number", "número", "price", "value", "preço", "valor"]):
            is_regression = True
        else:
            if pd.api.types.is_numeric_dtype(y) and y.nunique() > 10:
                is_regression = True
            else:
                is_classification = True

        results = {
            "task": "classification" if is_classification else "regression",
            "metrics": {},
            "feature_importance": [],
            "warnings": []
        }

        if is_classification:
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            results["metrics"]["accuracy"] = float(accuracy_score(y_test, y_pred))
            results["metrics"]["f1_macro"] = float(f1_score(y_test, y_pred, average="macro"))

            # ROC AUC if binary
            if y.nunique() == 2:
                try:
                    y_prob = model.predict_proba(X_test)[:, 1]
                    results["metrics"]["roc_auc"] = float(roc_auc_score(y_test, y_prob))
                except: pass
        else:
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            results["metrics"]["mae"] = float(mean_absolute_error(y_test, y_pred))
            results["metrics"]["r2"] = float(r2_score(y_test, y_pred))

        # Feature Importance
        importances = model.feature_importances_
        feature_names = X.columns
        feat_imp = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)

        for name, imp in feat_imp:
            results["feature_importance"].append({
                "feature": name,
                "importance": float(imp)
            })

            # Simple leakage heuristic
            if imp > 0.8:
                results["warnings"].append(self.t["leakage_warning"].format(col=name))

        return results

    def save_artifacts(self, results: dict[str, Any]):
        root = project_root()
        reports_dir = root / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)

        # 1. JSON Metrics
        metrics_path = reports_dir / "quick-model-metrics.json"
        with open(metrics_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        # 2. CSV Importance
        csv_path = reports_dir / "feature-importance.csv"
        imp_df = pd.DataFrame(results["feature_importance"])
        imp_df.to_csv(csv_path, index=False)

        # 3. Markdown Report
        md_path = reports_dir / "quick-model-report.md"
        md = [
            f"# {self.t['report_title']}",
            "",
            self.t["intro"],
            "",
            self.t["metrics_section"],
            f"| {self.t['metric_name']} | {self.t['metric_value']} |",
            "| :--- | :--- |"
        ]
        for m_name, m_val in results["metrics"].items():
            md.append(f"| {m_name.upper()} | {m_val:.4f} |")

        md.append("")
        md.append(self.t["importance_section"])
        md.append(f"| {self.t['feature_name']} | {self.t['importance_value']} |")
        md.append("| :--- | :--- |")
        # Top 15 features
        for item in results["feature_importance"][:15]:
            md.append(f"| {item['feature']} | {item['importance']:.4f} |")

        md.append("")
        md.append(self.t["leakage_section"])
        if not results["warnings"]:
            md.append("No suspicious features detected.")
        else:
            for w in results["warnings"]:
                md.append(f"- **{w}**")

        md.append("")
        md.append(self.t["appendix_section"])
        md.append(f"- {self.t['not_causal_warning']}")
        md.append(f"- {self.t['leakage_desc']}")

        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(md))

        print(self.t["status_complete"])
        print(f"- {metrics_path}")
        print(f"- {csv_path}")
        print(f"- {md_path}")

def main():
    root = project_root()

    # Load config and profile
    try:
        config = load_config()
    except Exception:
        print("Error: Configuration not found.")
        sys.exit(1)

    profile_path = root / "configs/problem_profile.json"
    if profile_path.exists():
        try:
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
        except:
            profile = {"language": "en"}
    else:
        profile = {"language": "en"}

    lang = profile.get("language", "en")
    t_missing = {
        "en": "pandas and scikit-learn are required for Feature Screening. Please install them with 'pip install pandas scikit-learn'.",
        "pt-BR": "O pandas e o scikit-learn são necessários para a Triagem de Features (Feature Screening). Instale-os com 'pip install pandas scikit-learn'."
    }.get(lang, "pandas and scikit-learn are required for Feature Screening.")

    if not DEPENDENCIES_AVAILABLE:
        print(t_missing)
        # print(f"DEBUG: Import error was: {_IMPORT_ERROR}")
        sys.exit(1)

    lab = FeatureScreeningLab(profile, config)
    results = lab.run()
    lab.save_artifacts(results)

if __name__ == "__main__":
    main()
