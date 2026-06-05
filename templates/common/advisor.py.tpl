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
        self.results = {
            "signals": [],
            "recommendations": [],
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
                "Small dataset detected",
                f"The dataset has only {n_rows} rows.",
                "Use simple baselines and cross-validation to avoid overfitting. Deep learning or complex ensembles might not perform well here.",
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
                    f"Missing values in '{col}'",
                    f"Column '{col}' has {missing_count} missing values ({missing_pct:.1f}%).",
                    f"Use SimpleImputer(strategy='{strategy}') for this column.",
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
                        f"Outliers detected in '{col}'",
                        f"Found {len(outliers)} potential outliers in '{col}' using IQR method.",
                        "Consider using RobustScaler or applying a log transformation if the distribution is highly skewed.",
                        "Machine learning outlier detection, RobustScaler vs StandardScaler"
                    )

            elif self._is_date_like(series):
                self.results["columns"]["date"].append(col)
                self._add_signal(
                    f"Date-like column '{col}'",
                    f"Detected '{col}' as a date or time column.",
                    "Extract features like year, month, day of week, or hour to use this in a model.",
                    "Feature engineering for datetime columns, pandas dt accessor"
                )
            else:
                # Categorical / Text
                nunique = series.nunique()
                if nunique / n_rows >= 0.8 and n_rows > 20:
                    self.results["columns"]["text"].append(col)
                    self._add_signal(
                        f"Potential text/ID column '{col}'",
                        f"'{col}' has very high cardinality ({nunique} unique values).",
                        "If this is an ID, drop it. If it's natural language, use TF-IDF or word embeddings.",
                        "High cardinality features, TF-IDF vectorization"
                    )
                else:
                    self.results["columns"]["categorical"].append(col)
                    if nunique <= 10:
                        self.results["columns"]["low_cardinality"].append(col)
                    else:
                        self.results["columns"]["high_cardinality"].append(col)
                        self._add_signal(
                            f"High cardinality categorical '{col}'",
                            f"'{col}' has {nunique} unique values.",
                            "One-hot encoding might create too many features. Consider target encoding, hashing, or grouping rare categories.",
                            "Encoding high cardinality categorical features"
                        )

        # Numeric scale check (global)
        num_df = self.df[self.results["columns"]["numeric"]]
        if not num_df.empty:
            std_devs = num_df.std()
            if std_devs.max() / (std_devs.min() + 1e-6) > 10:
                self._add_signal(
                    "Significant scale differences",
                    "Numeric features have very different standard deviations.",
                    "Use StandardScaler or MinMaxScaler to ensure features contribute equally to the model, especially for linear models, SVMs, or KNN.",
                    "Feature scaling importance, Scikit-learn StandardScaler"
                )

        # Correlation check
        if len(self.results["columns"]["numeric"]) > 1:
            corr = num_df.corr().abs()
            upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
            to_drop = [column for column in upper.columns if any(upper[column] > 0.9)]
            if to_drop:
                self._add_signal(
                    "High numeric correlation",
                    f"Highly correlated features detected: {to_drop}",
                    "Redundant features can sometimes hurt model interpretability or performance. Consider removing one of the pair or using PCA.",
                    "Multicollinearity in machine learning, Feature selection correlation"
                )

        # Target imbalance
        if self.target_col and self.target_col in self.df.columns:
            target_counts = self.df[self.target_col].value_counts(normalize=True)
            if target_counts.min() < 0.2:
                self._add_signal(
                    "Imbalanced target",
                    f"Target classes are imbalanced: {target_counts.to_dict()}",
                    "Use stratified splitting and consider metrics like F1-score or PR-AUC instead of accuracy. You might also try class weighting.",
                    "Imbalanced classification techniques, StratifiedKFold, SMOTE"
                )

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
                    "why": f"You prioritized {priority}. These models are highly interpretable and provide a clear baseline.",
                    "search": "LogisticRegression sklearn, DecisionTreeClassifier interpretability"
                })
            elif "imbalanced" in priority:
                recommendations.append({
                    "model": "Random Forest / HistGradientBoosting (with class_weight='balanced')",
                    "why": f"You prioritized {priority}. Tree-based ensembles handle non-linear relationships well and support class weighting.",
                    "search": "sklearn Random Forest class_weight, handling imbalanced data"
                })
            else:
                recommendations.append({
                    "model": "Random Forest / Gradient Boosting",
                    "why": "Tree-based ensembles are strong general-purpose performers for tabular classification.",
                    "search": "RandomForestClassifier vs HistGradientBoostingClassifier"
                })

        elif is_regression:
            if "interpretability" in priority:
                recommendations.append({
                    "model": "Linear Regression / Ridge / Lasso",
                    "why": f"You prioritized {priority}. Linear models show clear feature coefficients.",
                    "search": "LinearRegression sklearn, Ridge regression tutorial"
                })
            else:
                recommendations.append({
                    "model": "Random Forest / Gradient Boosting",
                    "why": "Tree-based ensembles are effective at capturing non-linear patterns in regression.",
                    "search": "RandomForestRegressor vs HistGradientBoostingRegressor"
                })

        elif is_timeseries:
            recommendations.append({
                "model": "Naive Seasonal / Exponential Smoothing",
                "why": "Always start with a naive baseline for time series to measure the value added by complex models.",
                "search": "Time series naive baseline, ExponentialSmoothing statsmodels"
            })
            recommendations.append({
                "model": "Prophet / ARIMA / Random Forest (with lag features)",
                "why": "Prophet is great for seasonality; ARIMA for trend; Random Forest is a strong tabular alternative if you engineer lag features.",
                "search": "facebook prophet tutorial, ARIMA vs Prophet, time series lag features"
            })

        elif is_unsupervised:
            recommendations.append({
                "model": "K-Means / HDBSCAN",
                "why": "K-Means is the standard baseline; HDBSCAN is better if clusters have varying densities.",
                "search": "KMeans sklearn, HDBSCAN clustering tutorial"
            })

        elif is_vision_text:
            recommendations.append({
                "model": "Pre-trained CNN (Vision) / Transformer (Text)",
                "why": "For complex data like images or text, transfer learning with pre-trained models is the modern standard.",
                "search": "pytorch transfer learning vision, huggingface transformers getting started"
            })

        # Dataset size adjustments
        if size == "small" or len(self.df) < 100:
            recommendations.append({
                "model": "Cross-validation + Simple Models",
                "why": f"With a {size} dataset, complex models are prone to overfitting. Use StratifiedKFold and prefer simpler baselines.",
                "search": "machine learning small dataset strategy, StratifiedKFold cross-validation"
            })

        # Error cost adjustments
        if "false negative" in error_cost:
            recommendations.append({
                "model": "Adjust Decision Threshold",
                "why": "Since false negatives are more costly, you should evaluate the model using Recall or PR-AUC and consider lowering the decision threshold.",
                "search": "precision recall trade-off, precision_recall_curve sklearn"
            })
        elif "false positive" in error_cost:
            recommendations.append({
                "model": "Adjust Decision Threshold",
                "why": "Since false positives are more costly, you should prioritize Precision and consider raising the decision threshold.",
                "search": "optimizing for precision sklearn, confusion matrix false positives"
            })

        # Final Baseline suggestion
        if prefer_baseline:
            recommendations.append({
                "model": "DummyClassifier / DummyRegressor",
                "why": "You preferred a simple baseline first. Use these to establish the minimum performance any 'real' model must beat.",
                "search": "DummyClassifier sklearn, DummyRegressor baseline"
            })

        if recommendations:
            report_section = "\n## Suggested Starting Models\n"
            report_section += "Based on your problem framing and initial data analysis:\n\n"
            for rec in recommendations:
                report_section += f"### {rec['model']}\n"
                report_section += f"- **Why**: {rec['why']}\n"
                report_section += f"- **Search terms**: `{rec['search']}`\n\n"

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
- **What I found**: {found}
- **Recommendation**: {recommendation}
- **Why this matters**: This helps improve model stability and performance by addressing specific data characteristics.
- **Search terms**: `{search_terms}`
""")

    def write_reports(self):
        report_path = project_root() / "reports/dataset-advice.md"
        content = f"# Dataset Advisor Report\n\nGenerated for project: {{PROJECT_NAME}}\n\n"
        if not self.results["signals"]:
            content += "No major issues detected. Your dataset looks clean!\n"
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
    advisor.write_pipeline_code("{{PACKAGE_NAME}}")


if __name__ == "__main__":
    main()
