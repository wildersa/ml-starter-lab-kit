# Feature Importance Strategy Matrix

Feature importance is not a single "truth." The relevance of a feature depends on the model's architecture, the chosen metric, how the data is split, and what information is available at prediction time.

This guide provides a strategy matrix to help you choose the right analysis technique for your problem.

## Strategy Matrix

| Problem Type | Model Family | Analysis Technique | Primary Metrics | Split Strategy |
|---|---|---|---|---|
| **Classification** | Tree/Boosting | Gini Importance, Permutation | F1-Score, AUC | Stratified Random |
| **Classification** | Linear | Coefficients (Scaled) | Accuracy, Log Loss | Stratified Random |
| **Regression** | Tree/Boosting | Variance Reduction, Permutation | MAE, RMSE | Random |
| **Regression** | Linear | Coefficients (Scaled) | R-squared, MAE | Random |
| **Time Series** | Linear/Tree/Deep | Permutation Importance | MAE, RMSE, WAPE | Time-based (Window) |
| **Clustering** | Distance-based | Centroid analysis, Silhouette | Silhouette Score | None (Full Data) |
| **Adaptive (Bandit)** | Linear/Probabilistic | Weight analysis, Propensity | Reward, Regret, Lift | Logged Policy Split |
| **Vision** | Neural/Deep | Saliency maps, Activation | Accuracy, mAP | Random/Stratified |

## When to Use Each Technique

### 1. Model-Specific Importance
- **Linear Models**: Use coefficients. Features must be on the same scale (e.g., via standard scaling techniques) for the magnitude to be comparable.
- **Tree-Based Models**: Use built-in importance measures based on impurity or gain. These are fast but can be biased toward high-cardinality categorical features.
- **Probabilistic Models**: Use posterior weights or feature impact on probability distribution.

### 2. Model-Agnostic (Permutation Importance)
This technique shuffles a single feature and measures the drop in the model's score.
- **Best for**: Comparing different model families on equal footing.
- **Benefit**: It accounts for interactions and does not depend on model internals.
- **Requirement**: Requires a held-out validation set to avoid measuring how much the model "overfit" to a feature.

### 3. Univariate Predictive Screening
Measuring the relationship between one feature and the target independently (e.g., correlation or mutual information).
- **Useful when**: You have thousands of features and need to remove noise before training.
- **Misleading when**: Features only provide value when combined with others (interactions).

## Domain Challenges

### Time Series
**Never use random splits.** If you use a random split to calculate importance, the model might "leak" information from the future to predict the past, making a feature look more important than it is in production. Always use a temporal split (train on past, test on "future").

### Clustering and Vision
These domains do **not** map cleanly to column-by-column predictive power.
- **Clustering**: Features define the space. Analysis usually involves checking how feature distributions differ between clusters rather than "predicting" a label.
- **Vision**: Importance is spatial (which pixels matter) rather than tabular. Global feature importance is often replaced by heatmaps or saliency maps.

### Contextual Bandits and Adaptive Labs
Analyzing bandit logs requires care because the data is "biased" by the policy that collected it.
- **Propensity**: You must account for the probability that an action was chosen (propensity score).
- **Reward vs. Action**: Feature importance can describe what drives the *reward* or what drives the *action selection*. These are different questions.
- **Logged Policy**: Always evaluate importance relative to a baseline or logging policy.

## Limitations and Caveats

- **Correlation is not Causation**: High importance means the model *used* the feature to lower the error; it does not prove the feature *caused* the outcome in the real world.
- **Collinearity**: If two features are highly correlated, a model might split the "importance" between them, making both look less significant than they actually are.
- **Metric Dependency**: A feature might be vital for optimizing RMSE but irrelevant for optimizing MAE.

## Learn More

Consult standard open-source documentation for your chosen library regarding "Permutation Importance" and "Feature Selection" for further technical details.

*Source: Strategy based on common best practices for model inspection.*
