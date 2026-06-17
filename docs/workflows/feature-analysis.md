# Model-Assisted Feature Analysis

Feature analysis is a diagnostic step where you use simple models to understand the relationship between your input columns and the target. It happens after EDA and before final model tuning.

## Engineering vs. Analysis vs. Selection

| Term | Goal |
|---|---|
| **Feature Engineering** | Creating new columns (e.g., ratios, aggregations, encodings). |
| **Feature Analysis** | Studying how much signal each feature provides to a model. |
| **Feature Selection** | Choosing the best subset of features to reduce noise or cost. |

## 1. Univariate Predictive Screening

This technique involves training a very small "proxy" model (like a shallow Decision Tree or Logistic Regression) using only **one feature at a time**.

- **Why:** It estimates if a feature has signal on its own.
- **Interpretation:** If a single feature yields a high metric (e.g., high AUC or low MAE), it is a strong predictor.
- **Warning:** If a feature shows nearly perfect results alone, it often indicates **target leakage** (information from the future that won't be available at prediction time).

## 2. Model-Based Importance

Once you have a baseline model trained with many features, you can extract "importance" scores (like Gini importance in Random Forests).

- **Why:** It shows which features the model relied on most during training.
- **Limitation:** High importance doesn't always mean the feature is "good"; it just means the model used it. If the feature is leaked, it will have high importance but fail in production.

## 3. Permutation Importance

This method measures how much the validation metric drops when you randomly shuffle a single feature's values.

- **Why:** It calculates the actual impact of the feature on the model's performance on unseen data.
- **Benefit:** It is more robust than raw training importance because it uses the validation set.

## Key Diagnostic Principles

### These are tools, not "The Truth"
Feature analysis helps you find bugs and signal, but it doesn't prove a feature is globally essential. It only shows how the feature behaves with a specific model and dataset.

### Interactions Matter
A feature might have a "low signal" in univariate screening but become extremely powerful when combined with another feature (interaction). Do not discard features based on univariate results alone.

### Leakage Detection
If a feature that should be "weak" (like a random ID or a zip code) shows high predictive power, investigate immediately. You might be looking at a leakage bug.

### Split and Metric Consistency
Your feature analysis must use the same **split strategy** (e.g., temporal split for time-series) and **metric** (e.g., F1-score for imbalanced classes) as your final evaluation. Using different settings will lead to misleading conclusions.
