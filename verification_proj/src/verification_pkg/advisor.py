from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import pandas as pd
import numpy as np

from .config import load_config, project_root

def get_dataset(config: dict[str, Any]) -> pd.DataFrame:
    raw_path = project_root() / config["data"]["raw_path"]
    if not raw_path.exists():
        raise FileNotFoundError(f"Dataset not found at {raw_path}. Please place your data there first.")

    # Try to load with pandas
    if raw_path.suffix == ".csv":
        return pd.read_csv(raw_path)
    elif raw_path.suffix in [".xls", ".xlsx"]:
        return pd.read_excel(raw_path)
    else:
        # Fallback to csv if unknown extension but readable
        return pd.read_csv(raw_path)

class DatasetAdvisor:
    def __init__(self, df: pd.DataFrame, target_col: str | None = None, problem_profile: dict[str, str] | None = None):
        self.df = df
        self.target_col = target_col
        self.problem_profile = problem_profile
        self.lang = (problem_profile or {}).get("language", "en")
        self.t = {
            "en": {
                "report_title": "Dataset Advisor Report",
                "summary": "Summary",
                "dataset_shape": "Dataset shape",
                "target_column": "Target column",
                "total_signals": "Total findings",
                "model_recommendations_count": "Model recommendations",
                "top_next_steps": "Top next steps",
                "generated_for": "Generated for project",
                "clean_dataset": "No major issues detected. Your dataset looks clean!",
                "why_matters": "Why this matters",
                "why_matters_text": "This helps improve model stability and performance by addressing specific data characteristics.",
                "search_terms": "Search terms",
                "found": "What I found",
                "recommendation": "Recommendation",
                "suggested_models": "Suggested Starting Models",
                "based_on": "Based on your problem framing and initial data analysis",
                "user_intent": "User intent",
                "data_finding": "Data finding",
                "why_suggested": "Why suggested",
                "small_dataset_title": "Small dataset detected",
                "small_dataset_found": "The dataset has only {n_rows} rows.",
                "small_dataset_rec": "Use simple baselines and cross-validation to avoid overfitting. Deep learning or complex ensembles might not perform well here.",
                "missing_values_title": "Missing values in '{col}'",
                "missing_values_found": "Column '{col}' has {missing_count} missing values ({missing_pct:.1f}%).",
                "missing_values_rec": "Use SimpleImputer(strategy='{strategy}') for this column.",
                "outliers_title": "Outliers detected in '{col}'",
                "outliers_found": "Found {len_outliers} potential outliers in '{col}' using IQR method.",
                "outliers_rec": "Consider using RobustScaler or applying a log transformation if the distribution is highly skewed.",
                "date_col_title": "Date-like column '{col}'",
                "date_col_found": "Detected '{col}' as a date or time column.",
                "date_col_rec": "Extract features like year, month, day of week, or hour to use this in a model.",
                "text_col_title": "Potential text/ID column '{col}'",
                "text_col_found": "'{col}' has very high cardinality ({nunique} unique values).",
                "text_col_rec": "If this is an ID, drop it. If it's natural language, use TF-IDF or word embeddings.",
                "high_card_title": "High cardinality categorical '{col}'",
                "high_card_found": "'{col}' has {nunique} unique values.",
                "high_card_rec": "One-hot encoding might create too many features. Consider target encoding, hashing, or grouping rare categories.",
                "scale_diff_title": "Significant scale differences",
                "scale_diff_found": "Numeric features have very different standard deviations.",
                "scale_diff_rec": "Use StandardScaler or MinMaxScaler to ensure features contribute equally to the model, especially for linear models, SVMs, or KNN.",
                "correlation_title": "High numeric correlation",
                "correlation_found": "Highly correlated features detected: {to_drop}",
                "correlation_rec": "Redundant features can sometimes hurt model interpretability or performance. Consider removing one of the pair or using PCA.",
                "imbalance_title": "Imbalanced target",
                "imbalance_found": "Target classes are imbalanced: {target_counts}",
                "imbalance_rec": "Use stratified splitting and consider metrics like F1-score or PR-AUC instead of accuracy. You might also try class weighting.",
            },
            "pt-BR": {
                "report_title": "Relatório do Dataset Advisor",
                "summary": "Resumo",
                "dataset_shape": "Formato do dataset",
                "target_column": "Coluna alvo",
                "total_signals": "Total de descobertas",
                "model_recommendations_count": "Recomendações de modelos",
                "top_next_steps": "Principais próximos passos",
                "generated_for": "Gerado para o projeto",
                "clean_dataset": "Nenhum problema grave detectado. Seu dataset parece limpo!",
                "why_matters": "Por que isso importa",
                "why_matters_text": "Isso ajuda a melhorar a estabilidade e o desempenho do modelo ao lidar com características específicas dos dados.",
                "search_terms": "Termos de busca",
                "found": "O que eu encontrei",
                "recommendation": "Recomendação",
                "suggested_models": "Modelos Iniciais Sugeridos",
                "based_on": "Com base na definição do seu problema e na análise inicial dos dados",
                "user_intent": "Intenção do usuário",
                "data_finding": "Descoberta nos dados",
                "why_suggested": "Por que foi sugerido",
                "small_dataset_title": "Dataset pequeno detectado",
                "small_dataset_found": "O dataset tem apenas {n_rows} linhas.",
                "small_dataset_rec": "Use baselines simples e validação cruzada para evitar overfitting. Deep learning ou ensembles complexos podem não funcionar bem aqui.",
                "missing_values_title": "Valores ausentes em '{col}'",
                "missing_values_found": "A coluna '{col}' tem {missing_count} valores ausentes ({missing_pct:.1f}%).",
                "missing_values_rec": "Use SimpleImputer(strategy='{strategy}') para esta coluna.",
                "outliers_title": "Outliers detectados em '{col}'",
                "outliers_found": "Encontrados {len_outliers} potenciais outliers em '{col}' usando o método IQR.",
                "outliers_rec": "Considere usar RobustScaler ou aplicar uma transformação logarítmica se a distribuição for altamente assimétrica.",
                "date_col_title": "Coluna de data '{col}'",
                "date_col_found": "Detectada '{col}' como uma coluna de data ou hora.",
                "date_col_rec": "Extraia características como ano, mês, dia da semana ou hora para usar isso em um modelo.",
                "text_col_title": "Potencial coluna de texto/ID '{col}'",
                "text_col_found": "'{col}' tem cardinalidade muito alta ({nunique} valores únicos).",
                "text_col_rec": "Se for um ID, remova-o. Se for linguagem natural, use TF-IDF ou word embeddings.",
                "high_card_title": "Categoria com alta cardinalidade '{col}'",
                "high_card_found": "'{col}' tem {nunique} valores únicos.",
                "high_card_rec": "One-hot encoding pode criar muitas features. Considere target encoding, hashing ou agrupar categorias raras.",
                "scale_diff_title": "Diferenças significativas de escala",
                "scale_diff_found": "As características numéricas têm desvios padrão muito diferentes.",
                "scale_diff_rec": "Use StandardScaler ou MinMaxScaler para garantir que as características contribuam igualmente para o modelo, especialmente para modelos lineares, SVMs ou KNN.",
                "correlation_title": "Alta correlação numérica",
                "correlation_found": "Características altamente correlacionadas detectadas: {to_drop}",
                "correlation_rec": "Características redundantes às vezes podem prejudicar a interpretabilidade ou o desempenho do modelo. Considere remover uma do par ou usar PCA.",
                "imbalance_title": "Alvo desbalanceado",
                "imbalance_found": "As classes do alvo estão desbalanceadas: {target_counts}",
                "imbalance_rec": "Use divisão estratificada e considere métricas como F1-score ou PR-AUC em vez de acurácia. Você também pode tentar ponderação de classes.",
            }
        }[self.lang]
        self.results = {
            "summary": {},
            "next_steps": [],
            "signals": [],
            "model_recommendations": [],
            "columns": {
                "numeric": [],
                "categorical": [],
                "date": [],
                "text": [],
                "low_cardinality": [],
                "high_cardinality": []
            },
            "pipeline_steps": {
                "numeric": [],
                "categorical": []
            }
        }
        self.report_sections = []

    def run_checks(self):
        # 0. Problem Framing Recommendations
        self._add_model_recommendations()

        # 1. Basic Stats
        n_rows = len(self.df)
        n_cols = len(self.df.columns)

        # Small dataset risk
        if n_rows < 100:
            self._add_signal(
                self.t["small_dataset_title"],
                self.t["small_dataset_found"].format(n_rows=n_rows),
                self.t["small_dataset_rec"],
                "Small dataset machine learning, Cross-validation strategies, Overfitting prevention"
            )

        # 2. Column Classification & Missing Values
        for col in self.df.columns:
            if col == self.target_col:
                continue

            series = self.df[col]
            missing_count = series.isnull().sum()
            missing_pct = (missing_count / n_rows) * 100

            # Missing values signal
            if missing_count > 0:
                strategy = "median" if pd.api.types.is_numeric_dtype(series) else "most_frequent"
                self._add_signal(
                    self.t["missing_values_title"].format(col=col),
                    self.t["missing_values_found"].format(col=col, missing_count=missing_count, missing_pct=missing_pct),
                    self.t["missing_values_rec"].format(strategy=strategy),
                    f"Handling missing data sklearn, SimpleImputer strategy {strategy}"
                )

            # Type detection
            if pd.api.types.is_numeric_dtype(series):
                self.results["columns"]["numeric"].append(col)

                # Numeric scale differences
                if series.max() - series.min() > 1000 or (series.std() > 100 and series.mean() != 0):
                    # Heuristic for different scales: we'll check this globally later or per column
                    pass

                # Outliers (simple IQR check)
                q1 = series.quantile(0.25)
                q3 = series.quantile(0.75)
                iqr = q3 - q1
                outliers = series[(series < (q1 - 1.5 * iqr)) | (series > (q3 + 1.5 * iqr))]
                if len(outliers) > 0:
                    self._add_signal(
                        self.t["outliers_title"].format(col=col),
                        self.t["outliers_found"].format(col=col, len_outliers=len(outliers)),
                        self.t["outliers_rec"],
                        "Machine learning outlier detection, RobustScaler vs StandardScaler"
                    )

            elif self._is_date_like(series):
                self.results["columns"]["date"].append(col)
                self._add_signal(
                    self.t["date_col_title"].format(col=col),
                    self.t["date_col_found"].format(col=col),
                    self.t["date_col_rec"],
                    "Feature engineering for datetime columns, pandas dt accessor"
                )
            else:
                # Categorical / Text
                nunique = series.nunique()
                if nunique / n_rows >= 0.8 and n_rows > 20:
                    self.results["columns"]["text"].append(col)
                    self._add_signal(
                        self.t["text_col_title"].format(col=col),
                        self.t["text_col_found"].format(col=col, nunique=nunique),
                        self.t["text_col_rec"],
                        "High cardinality features, TF-IDF vectorization"
                    )
                else:
                    self.results["columns"]["categorical"].append(col)
                    if nunique <= 10:
                        self.results["columns"]["low_cardinality"].append(col)
                    else:
                        self.results["columns"]["high_cardinality"].append(col)
                        self._add_signal(
                            self.t["high_card_title"].format(col=col),
                            self.t["high_card_found"].format(col=col, nunique=nunique),
                            self.t["high_card_rec"],
                            "Encoding high cardinality categorical features"
                        )

        # Numeric scale check (global)
        num_df = self.df[self.results["columns"]["numeric"]]
        if not num_df.empty:
            std_devs = num_df.std()
            if std_devs.max() / (std_devs.min() + 1e-6) > 10:
                self._add_signal(
                    self.t["scale_diff_title"],
                    self.t["scale_diff_found"],
                    self.t["scale_diff_rec"],
                    "Feature scaling importance, Scikit-learn StandardScaler"
                )

        # Correlation check
        if len(self.results["columns"]["numeric"]) > 1:
            corr = num_df.corr().abs()
            upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
            to_drop = [column for column in upper.columns if any(upper[column] > 0.9)]
            if to_drop:
                self._add_signal(
                    self.t["correlation_title"],
                    self.t["correlation_found"].format(to_drop=to_drop),
                    self.t["correlation_rec"],
                    "Multicollinearity in machine learning, Feature selection correlation"
                )

        # Target imbalance
        if self.target_col and self.target_col in self.df.columns:
            target_counts = self.df[self.target_col].value_counts(normalize=True)
            if target_counts.min() < 0.2:
                self._add_signal(
                    self.t["imbalance_title"],
                    self.t["imbalance_found"].format(target_counts=target_counts.to_dict()),
                    self.t["imbalance_rec"],
                    "Imbalanced classification techniques, StratifiedKFold, SMOTE"
                )

        # 3. Final Summary Metadata
        self.results["summary"] = {
            "project_name": "verification_proj",
            "dataset_shape": [n_rows, n_cols],
            "target_column": self.target_col,
            "total_signals": len(self.results["signals"]),
            "model_recommendations": len(self.results.get("model_recommendations", []))
        }

        # 4. Top next steps from findings
        self.results["next_steps"] = [s["recommendation"] for s in self.results["signals"][:5]]

    def _is_date_like(self, series):
        if pd.api.types.is_datetime64_any_dtype(series):
            return True

        if series.dtype == object or str(series.dtype) == "string":
            # Heuristic: strings that look like dates
            # We'll try to convert a small sample
            sample = series.dropna().head(10)
            if len(sample) == 0:
                return False

            # Simple regex check for common date formats before trying to_datetime
            # (YYYY-MM-DD, DD/MM/YYYY, etc.)
            date_patterns = [
                r"^\d{4}-\d{2}-\d{2}",
                r"^\d{2}/\d{2}/\d{4}",
                r"^\d{4}/\d{2}/\d{2}"
            ]

            sample_str = sample.astype(str, copy=False)
            matches = any(sample_str.str.match(pattern).any() for pattern in date_patterns)

            if matches:
                try:
                    pd.to_datetime(sample, errors="raise")
                    return True
                except:
                    return False
        return False

    def _add_model_recommendations(self):
        if not self.problem_profile:
            return

        goal = self.problem_profile.get("goal", "").lower()
        priority = self.problem_profile.get("priority", "").lower()
        error_cost = self.problem_profile.get("error_cost", "").lower()
        size = self.problem_profile.get("dataset_size", "").lower()
        prefer_baseline = self.problem_profile.get("prefer_baseline", "").lower() == "yes"

        recommendations = []

        # Determine task type from goal
        is_classification = "category" in goal
        is_regression = "number" in goal
        is_unsupervised = "group" in goal or "cluster" in goal
        is_timeseries = "forecast" in goal
        is_vision_text = "images" in goal or "text" in goal

        # Initial recommendations based on goal and priority
        if is_classification:
            if "interpretability" in priority:
                recommendations.append({
                    "model": "Logistic Regression / Decision Tree",
                    "user_intent": f"Prioritize {priority}",
                    "data_finding": "Tabular classification task",
                    "why": "These models are highly interpretable and provide a clear baseline for categorical predictions.",
                    "search": "LogisticRegression sklearn, DecisionTreeClassifier interpretability"
                })
            elif "imbalanced" in priority:
                recommendations.append({
                    "model": "Random Forest / HistGradientBoosting (with class_weight='balanced')",
                    "user_intent": f"Handle {priority}",
                    "data_finding": "Target imbalance expected or detected",
                    "why": "Tree-based ensembles handle non-linear relationships well and natively support class weighting to focus on the minority class.",
                    "search": "sklearn Random Forest class_weight, handling imbalanced data"
                })
            else:
                recommendations.append({
                    "model": "Random Forest / Gradient Boosting",
                    "user_intent": f"Goal: {goal}",
                    "data_finding": "General tabular classification",
                    "why": "Tree-based ensembles are strong general-purpose performers for tabular classification with minimal scaling required.",
                    "search": "RandomForestClassifier vs HistGradientBoostingClassifier"
                })

        elif is_regression:
            if "interpretability" in priority:
                recommendations.append({
                    "model": "Linear Regression / Ridge / Lasso",
                    "user_intent": f"Prioritize {priority}",
                    "data_finding": "Tabular regression task",
                    "why": "Linear models show clear feature coefficients, making it easy to see which variables drive the outcome.",
                    "search": "LinearRegression sklearn, Ridge regression tutorial"
                })
            else:
                recommendations.append({
                    "model": "Random Forest / Gradient Boosting",
                    "user_intent": f"Goal: {goal}",
                    "data_finding": "General tabular regression",
                    "why": "Tree-based ensembles are effective at capturing non-linear patterns in regression without complex feature engineering.",
                    "search": "RandomForestRegressor vs HistGradientBoostingRegressor"
                })

        elif is_timeseries:
            recommendations.append({
                "model": "Naive Seasonal / Exponential Smoothing",
                "user_intent": f"Forecast future values",
                "data_finding": "Time series task detected",
                "why": "Always start with a naive baseline for time series to measure the value added by complex models. Often hard to beat!",
                "search": "Time series naive baseline, ExponentialSmoothing statsmodels"
            })
            recommendations.append({
                "model": "Prophet / ARIMA / Random Forest (with lag features)",
                "user_intent": f"Goal: {goal}",
                "data_finding": "Sequential data patterns",
                "why": "Prophet handles seasonality well; ARIMA is a statistical standard; Random Forest is a strong tabular alternative if you engineer lag features.",
                "search": "facebook prophet tutorial, ARIMA vs Prophet, time series lag features"
            })

        elif is_unsupervised:
            recommendations.append({
                "model": "K-Means / HDBSCAN",
                "user_intent": f"Group similar records",
                "data_finding": "Clustering task",
                "why": "K-Means is the standard baseline; HDBSCAN is better if you expect clusters of different shapes and densities.",
                "search": "KMeans sklearn, HDBSCAN clustering tutorial"
            })

        elif is_vision_text:
            recommendations.append({
                "model": "Pre-trained CNN (Vision) / Transformer (Text)",
                "user_intent": f"Goal: {goal}",
                "data_finding": "Unstructured data (images/text)",
                "why": "For complex data like images or text, transfer learning with pre-trained models is the modern standard for performance.",
                "search": "pytorch transfer learning vision, huggingface transformers getting started"
            })

        # Dataset size adjustments
        if size == "small" or len(self.df) < 100:
            recommendations.append({
                "model": "Cross-validation + Simple Models",
                "user_intent": f"Dataset size: {size}",
                "data_finding": f"Dataset has {len(self.df)} rows",
                "why": "With small datasets, complex models are prone to overfitting. Use StratifiedKFold and prefer simpler baselines to ensure generalization.",
                "search": "machine learning small dataset strategy, StratifiedKFold cross-validation"
            })

        # Error cost adjustments
        if "false negative" in error_cost:
            recommendations.append({
                "model": "Recall-optimized Evaluation",
                "user_intent": f"Costly error: {error_cost}",
                "data_finding": "Intent to minimize missed cases",
                "why": "Since false negatives are more costly, you should evaluate using Recall or PR-AUC and consider lowering the model's decision threshold.",
                "search": "precision recall trade-off, precision_recall_curve sklearn"
            })
        elif "false positive" in error_cost:
            recommendations.append({
                "model": "Precision-optimized Evaluation",
                "user_intent": f"Costly error: {error_cost}",
                "data_finding": "Intent to minimize false alarms",
                "why": "Since false positives are more costly, you should prioritize Precision and consider raising the model's decision threshold.",
                "search": "optimizing for precision sklearn, confusion matrix false positives"
            })

        # Final Baseline suggestion
        if prefer_baseline:
            recommendations.append({
                "model": "Dummy Models (Baseline)",
                "user_intent": "Prefer simple baseline first",
                "data_finding": "Initial experiment setup",
                "why": "Use DummyClassifier or DummyRegressor to establish the minimum performance any 'real' model must beat.",
                "search": "DummyClassifier sklearn, DummyRegressor baseline"
            })

        if recommendations:
            report_section = f"\n## {self.t['suggested_models']}\n"
            report_section += f"{self.t['based_on']}:\n\n"
            for rec in recommendations:
                report_section += f"### {rec['model']}\n"
                report_section += f"- **{self.t['user_intent']}**: {rec['user_intent']}\n"
                report_section += f"- **{self.t['data_finding']}**: {rec['data_finding']}\n"
                report_section += f"- **{self.t['why_suggested']}**: {rec['why']}\n"
                report_section += f"- **{self.t['search_terms']}**: `{rec['search']}`\n\n"

            self.report_sections.append(report_section)
            self.results["model_recommendations"] = recommendations

    def _add_signal(self, title, found, recommendation, search_terms):
        self.results["signals"].append({
            "title": title,
            "found": found,
            "recommendation": recommendation,
            "search_terms": search_terms
        })
        self.report_sections.append(f"""
### {title}
- **{self.t['found']}**: {found}
- **{self.t['recommendation']}**: {recommendation}
- **{self.t['why_matters']}**: {self.t['why_matters_text']}
- **{self.t['search_terms']}**: `{search_terms}`
""")

    def write_reports(self):
        report_path = project_root() / "reports/dataset-advice.md"

        # Build polished report
        content = f"# {self.t['report_title']}\n\n"
        content += f"{self.t['generated_for']}: verification_proj\n\n"

        # Summary Section
        summary = self.results["summary"]
        content += f"## {self.t['summary']}\n"
        content += f"- **{self.t['dataset_shape']}**: {summary['dataset_shape']}\n"
        content += f"- **{self.t['target_column']}**: {summary['target_column']}\n"
        content += f"- **{self.t['total_signals']}**: {summary['total_signals']}\n"
        content += f"- **{self.t['model_recommendations_count']}**: {summary['model_recommendations']}\n\n"

        # Top Next Steps
        if self.results["next_steps"]:
            content += f"## {self.t['top_next_steps']}\n"
            for i, step in enumerate(self.results["next_steps"], 1):
                content += f"{i}. {step}\n"
            content += "\n"

        if not self.results["signals"]:
            content += f"{self.t['clean_dataset']}\n"
        else:
            content += "".join(self.report_sections)

        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(content, encoding="utf-8")
        print(f"Advice report written to {report_path}")

        # JSON summary
        json_path = project_root() / "configs/suggested_pipeline.json"
        json_path.write_text(json.dumps(self.results, indent=2), encoding="utf-8")
        print(f"Pipeline config written to {json_path}")

    def write_pipeline_code(self, package_name: str):
        pipeline_path = project_root() / f"src/{package_name}/suggested_pipeline.py"

        # Determine steps based on signals
        num_imputer = "SimpleImputer(strategy='median')"
        cat_imputer = "SimpleImputer(strategy='most_frequent')"
        scaler = "StandardScaler()"
        encoder = "OneHotEncoder(handle_unknown='ignore', sparse_output=False)"

        # Check if we should use RobustScaler
        if any("Outliers detected" in s["title"] for s in self.results["signals"]):
            scaler = "RobustScaler()"

        numeric_cols = self.results["columns"]["numeric"]
        categorical_cols = self.results["columns"]["categorical"]
        date_cols = self.results["columns"]["date"]

        code = f'''from __future__ import annotations

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, RobustScaler

def get_suggested_pipeline() -> Pipeline:
    """
    Returns a scikit-learn Pipeline based on Dataset Advisor recommendations.
    This is a starting point and should be adapted to your needs.
    """
    numeric_features = {numeric_cols}
    categorical_features = {categorical_cols}

    numeric_transformer = Pipeline(steps=[
        ("imputer", {num_imputer}),
        ("scaler", {scaler})
    ])

    categorical_transformer = Pipeline(steps=[
        ("imputer", {cat_imputer}),
        ("encoder", {encoder})
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
            # Date columns: {date_cols}
            # Note: You may need a custom transformer for dates
        ],
        remainder="drop"  # or "passthrough"
    )

    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        # Add your estimator here, e.g., ("model", LogisticRegression())
    ])

    return pipeline

if __name__ == "__main__":
    pipeline = get_suggested_pipeline()
    print("Suggested pipeline created:")
    print(pipeline)
'''
        pipeline_path.write_text(code, encoding="utf-8")
        print(f"Suggested pipeline code written to {pipeline_path}")

def main():
    # P0.1: Gate advisor behind EDA artifact
    eda_summary_path = project_root() / "configs/eda_summary.json"
    if not eda_summary_path.exists():
        print("\n[STOPSHIP] Dataset Advisor requires an EDA summary to provide data-driven suggestions.")
        print("Please run the Exploratory Data Analysis (EDA) step first:")
        print(f"  python -m verification_pkg.lab eda")
        print("  OR")
        print(f"  python -m verification_pkg.eda")
        return

    config = load_config()
    target_col = config.get("target", {}).get("column")

    problem_profile = None
    profile_path = project_root() / "configs/problem_profile.json"
    if profile_path.exists():
        try:
            problem_profile = json.loads(profile_path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"Warning: Could not load problem_profile.json: {e}")

    try:
        df = get_dataset(config)
    except FileNotFoundError as e:
        print(e)
        return

    print(f"Analyzing dataset with {len(df)} rows and {len(df.columns)} columns...")

    advisor = DatasetAdvisor(df, target_col, problem_profile)
    advisor.run_checks()
    advisor.write_reports()
    advisor.write_pipeline_code("verification_pkg")

if __name__ == "__main__":
    main()
