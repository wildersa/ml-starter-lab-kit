from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

try:
    import pandas as pd
    import numpy as np
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False

from .core.config import load_config, project_root

class DataInsights:
    def __init__(self, df: pd.DataFrame, target_col: str | None, lang: str = "en"):
        self.df = df
        self.target_col = target_col
        self.lang = lang
        self.t = {
            "en": {
                "report_title": "Dataset Intelligence Report",
                "summary_section": "## 1. Data Quality Summary",
                "target_section": "## 2. Target Analysis",
                "feature_section": "## 3. Feature Screening",
                "warnings_section": "## 4. Risks and Warnings",
                "explanation_section": "## 5. Educational Appendix",
                "rows": "Rows",
                "columns": "Columns",
                "missing_values": "Missing Values",
                "unique_values": "Unique Values",
                "type": "Type",
                "status": "Status",
                "warning": "WARNING",
                "ok": "OK",
                "target_not_found": "Target column '{col}' not found in dataset.",
                "constant_col": "Constant column: {col} has only one unique value.",
                "high_cardinality": "High cardinality: {col} has {n} unique values ({pct:.1f}%).",
                "imbalance_warning": "Imbalanced target: {col} has a minority class with only {pct:.1f}%.",
                "leakage_duplicate": "Potential leakage: {col} seems to be a duplicate or near-duplicate of the target.",
                "leakage_name": "Potential leakage: {col} has a name suspiciously similar to the target.",
                "multicollinearity": "High multicollinearity: {col1} and {col2} have a correlation of {corr:.2f}.",
                "feature_utility": "Feature Utility (Simple Correlation/Association with Target)",
                "low_utility": "Low utility: {col} has very low association with the target.",
                "missing_desc": "Percentage of missing data in the column.",
                "leakage_desc": "Leakage happens when information from the future or the target itself is 'leaked' into features.",
                "multicollinearity_desc": "High correlation between features can make model coefficients unstable and harder to interpret.",
                "imbalance_desc": "If classes are very uneven, the model might just learn to predict the majority class.",
            },
            "pt-BR": {
                "report_title": "Relatório de Inteligência de Dados",
                "summary_section": "## 1. Resumo de Qualidade de Dados",
                "target_section": "## 2. Análise do Alvo (Target)",
                "feature_section": "## 3. Triagem de Características (Features)",
                "warnings_section": "## 4. Riscos e Avisos",
                "explanation_section": "## 5. Apêndice Educacional",
                "rows": "Linhas",
                "columns": "Colunas",
                "missing_values": "Valores Ausentes",
                "unique_values": "Valores Únicos",
                "type": "Tipo",
                "status": "Status",
                "warning": "AVISO",
                "ok": "OK",
                "target_not_found": "Coluna alvo '{col}' não encontrada no dataset.",
                "constant_col": "Coluna constante: {col} possui apenas um valor único.",
                "high_cardinality": "Alta cardinalidade: {col} possui {n} valores únicos ({pct:.1f}%).",
                "imbalance_warning": "Alvo desbalanceado: {col} tem uma classe minoritária com apenas {pct:.1f}%.",
                "leakage_duplicate": "Potencial leakage: {col} parece ser uma duplicata ou quase duplicata do alvo.",
                "leakage_name": "Potencial leakage: {col} tem um nome suspeitamente similar ao alvo.",
                "multicollinearity": "Alta multicolinearidade: {col1} e {col2} possuem correlação de {corr:.2f}.",
                "feature_utility": "Utilidade da Feature (Correlação/Associação Simples com o Alvo)",
                "low_utility": "Baixa utilidade: {col} possui associação muito baixa com o alvo.",
                "missing_desc": "Porcentagem de dados ausentes na coluna.",
                "leakage_desc": "Leakage ocorre quando informações do futuro ou do próprio alvo 'vazam' para as features.",
                "multicollinearity_desc": "Alta correlação entre features pode tornar os coeficientes do modelo instáveis e difíceis de interpretar.",
                "imbalance_desc": "Se as classes estiverem muito desequilibradas, o modelo pode aprender apenas a prever a classe majoritária.",
            }
        }[self.lang]
        self.insights = {
            "quality": {},
            "target": {},
            "features": [],
            "warnings": []
        }

    def analyze(self):
        df = self.df
        n_rows = len(df)

        # 1. Quality Summary
        self.insights["quality"] = {
            "rows": n_rows,
            "columns": len(df.columns),
            "column_inventory": []
        }

        for col in df.columns:
            nunique = df[col].nunique()
            missing = df[col].isnull().sum()
            col_type = str(df[col].dtype)

            self.insights["quality"]["column_inventory"].append({
                "column": col,
                "type": col_type,
                "nunique": int(nunique),
                "missing": int(missing),
                "missing_pct": float(missing / n_rows)
            })

            # Constant column warning
            if nunique <= 1:
                self.insights["warnings"].append({
                    "type": "constant_column",
                    "column": col,
                    "message": self.t["constant_col"].format(col=col)
                })

            # High cardinality warning (for non-numeric)
            if not pd.api.types.is_numeric_dtype(df[col]) and nunique / n_rows > 0.5 and n_rows > 20:
                self.insights["warnings"].append({
                    "type": "high_cardinality",
                    "column": col,
                    "message": self.t["high_cardinality"].format(col=col, n=nunique, pct=(nunique/n_rows)*100)
                })

        # 2. Target Analysis
        if self.target_col and self.target_col in df.columns:
            y = df[self.target_col]
            nunique_y = y.nunique()
            is_numeric_y = pd.api.types.is_numeric_dtype(y)

            target_type = "classification" if nunique_y < 20 or not is_numeric_y else "regression"

            dist = y.value_counts(normalize=True).to_dict()
            self.insights["target"] = {
                "column": self.target_col,
                "type_guess": target_type,
                "nunique": int(nunique_y),
                "distribution": {str(k): float(v) for k, v in dist.items()}
            }

            if target_type == "classification" and nunique_y >= 2:
                min_pct = min(dist.values())
                if min_pct < 0.1:
                    self.insights["warnings"].append({
                        "type": "imbalance",
                        "column": self.target_col,
                        "message": self.t["imbalance_warning"].format(col=self.target_col, pct=min_pct*100)
                    })

            # 3. Feature Screening & Leakage
            for col in df.columns:
                if col == self.target_col:
                    continue

                # Basic leakage name check
                if self.target_col.lower() in col.lower() and col.lower() != self.target_col.lower():
                    self.insights["warnings"].append({
                        "type": "leakage_name",
                        "column": col,
                        "message": self.t["leakage_name"].format(col=col)
                    })

                # Utility screening
                utility = 0.0
                if is_numeric_y and pd.api.types.is_numeric_dtype(df[col]):
                    # Correlation for numeric-numeric
                    utility = abs(df[col].corr(y))
                    if np.isnan(utility): utility = 0.0

                self.insights["features"].append({
                    "column": col,
                    "utility": float(utility)
                })

                # Near perfect signal leakage
                if utility > 0.98:
                    self.insights["warnings"].append({
                        "type": "leakage_signal",
                        "column": col,
                        "message": self.t["leakage_duplicate"].format(col=col)
                    })

        # 4. Multicollinearity
        numeric_df = df.select_dtypes(include=[np.number])
        if len(numeric_df.columns) > 1:
            corr_matrix = numeric_df.corr().abs()
            upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
            for col in upper.columns:
                for idx, val in upper[col].items():
                    if val > 0.95:
                        self.insights["warnings"].append({
                            "type": "multicollinearity",
                            "columns": [str(idx), str(col)],
                            "message": self.t["multicollinearity"].format(col1=idx, col2=col, corr=val)
                        })

    def save_artifacts(self):
        root = project_root()
        reports_dir = root / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)

        # JSON artifact
        json_path = reports_dir / "data-insights.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self.insights, f, indent=2, ensure_ascii=False)

        # CSV screening
        csv_path = reports_dir / "feature-screening.csv"
        feat_df = pd.DataFrame(self.insights["features"])
        if not feat_df.empty:
            feat_df.sort_values("utility", ascending=False).to_csv(csv_path, index=False)

        # Markdown report
        md_path = reports_dir / "data-quality-report.md"
        md = [
            f"# {self.t['report_title']}",
            "",
            self.t["summary_section"],
            f"- **{self.t['rows']}:** {self.insights['quality']['rows']}",
            f"- **{self.t['columns']}:** {self.insights['quality']['columns']}",
            "",
            "| Column | Type | Unique | Missing % | Status |",
            "| :--- | :--- | :--- | :--- | :--- |"
        ]

        for col in self.insights["quality"]["column_inventory"]:
            status = self.t["ok"]
            col_name = col["column"]
            if any(w.get("column") == col_name for w in self.insights["warnings"]):
                status = f"**{self.t['warning']}**"
            md.append(f"| {col_name} | {col['type']} | {col['nunique']} | {col['missing_pct']:.1%}| {status} |")

        md.append("")
        md.append(self.t["target_section"])
        if self.insights["target"]:
            md.append(f"- **Column:** {self.insights['target']['column']}")
            md.append(f"- **Inferred Task:** {self.insights['target']['type_guess']}")
            md.append(f"- **Distribution:** {self.insights['target']['distribution']}")
        else:
            md.append(f"_{self.t['target_not_found'].format(col=self.target_col)}_")

        md.append("")
        md.append(self.t["warnings_section"])
        if not self.insights["warnings"]:
            md.append(f"_{self.t['ok']}_")
        else:
            for w in self.insights["warnings"]:
                md.append(f"- [{w['type'].upper()}] {w['message']}")

        md.append("")
        md.append(self.t["explanation_section"])
        md.append(f"### {self.t['missing_values']}")
        md.append(self.t["missing_desc"])
        md.append(f"### Leakage")
        md.append(self.t["leakage_desc"])
        md.append(f"### Multicollinearity")
        md.append(self.t["multicollinearity_desc"])

        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(md))

        print(f"Dataset Intelligence artifacts created:")
        print(f"- {json_path}")
        print(f"- {csv_path}")
        print(f"- {md_path}")

def main():
    if not DEPENDENCIES_AVAILABLE:
        print("pandas and numpy are required for Dataset Intelligence.")
        sys.exit(1)

    try:
        config = load_config()
    except Exception:
        print("Error: Configuration not found. Run from project root.")
        sys.exit(1)

    raw_path = config.get("data", {}).get("raw_path")
    target_col = config.get("target", {}).get("column")

    # Language detection
    lang = "en"
    profile_path = project_root() / "configs/problem_profile.json"
    if profile_path.exists():
        try:
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
            lang = profile.get("language", "en")
        except: pass

    if not raw_path:
        print("Error: Dataset path not configured.")
        sys.exit(1)

    path = project_root() / raw_path
    if not path.exists():
        print(f"Error: Dataset not found at {path}")
        sys.exit(1)

    df = pd.read_csv(path)
    insights = DataInsights(df, target_col, lang=lang)
    insights.analyze()
    insights.save_artifacts()

if __name__ == "__main__":
    main()
