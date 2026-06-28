# Pre-Modeling Analysis

Before training complex models, it is essential to understand your data. Pre-modeling analysis is a diagnostic workflow that helps you identify bugs, signals, and risks early.

This guide organizes these analyses into a logical learning flow to help you decide if a dataset is ready for baseline modeling.

## Learning Flow

1. **Understand the Dataset**: Get a high-level view of what you have.
2. **Understand Distributions**: Look at individual columns in isolation.
3. **Understand Feature Relationships**: See how columns interact with each other.
4. **Protect Validation**: Ensure your evaluation strategy is robust against leakage.
5. **Measure Early Predictive Signal**: Check if features actually relate to the target.
6. **Inspect Segment-level Risk**: Look for imbalances or biases in specific groups.
7. **Decision**: Determine if the data quality and signal are sufficient to proceed.

---

## First Decision: Do You Have a Target?

Most pre-modeling analysis starts with one question:

```text
Do I have a historical answer/gabarito for each row?
```

If yes, the problem is usually **supervised**. You can ask whether the features help predict that target.

If no, the problem is **unsupervised**. You cannot measure predictive power against a target, so the analysis changes: you look for structure, groups, redundancy, anomalies, or useful representations.

```text
Have a target?
|
|-- Yes -> supervised pre-analysis
|          features + target -> quick model -> metrics + feature importance
|
`-- No  -> unsupervised pre-analysis
           features only -> structure, clusters, anomalies, variance, visualization
```

---

## Supervised Pre-Analysis: Predictive Signal

Use this when the dataset has a target column.

Examples:

- `churn`: did the customer cancel?
- `fraud`: was the transaction fraudulent?
- `price`: observed sale price.
- `delivery_time`: observed delivery time.
- `conversion`: did the user convert?

Main question:

```text
Do these features help predict this target?
```

A quick supervised probe model is useful here. It is not the final model. It is a diagnostic step.

Common probe models:

- XGBoost
- LightGBM
- Random Forest
- shallow Decision Tree
- Logistic Regression
- Linear Regression
- simple AutoML run

This can reveal:

- whether the dataset has predictive signal;
- whether the initial score is plausible;
- which features appear useful;
- whether a feature may be leaking future information;
- whether the problem looks simple, hard, noisy, or badly formulated;
- whether it is worth moving to proper training and evaluation.

Typical flow:

```text
dataset with target
-> minimal preprocessing
-> quick supervised probe model
-> initial metrics
-> feature importance
-> leakage and feature sanity review
-> decision: continue, fix data, or reformulate the problem
```

For tabular data, XGBoost or another tree-boosting model is often a strong default probe because it can capture non-linear relationships and feature interactions with little manual feature engineering. Still, it is only a diagnostic baseline, not proof that the final model should be XGBoost.

---

## Unsupervised Pre-Analysis: Structure Without a Target

Use this when there is no target column.

In this case, do not ask:

```text
Which feature predicts the target best?
```

There is no target. Ask instead:

```text
Is there useful structure in the data?
```

Common questions:

- Are there natural groups?
- Are there unusual records?
- Are some columns redundant?
- Can the data be simplified into fewer dimensions?
- Do patterns become visible in 2D or 3D?
- Which features help separate profiles or explain variance?

Useful tools:

| Goal | Common tools |
|---|---|
| Find simple groups | K-Means |
| Find irregular groups or noise | DBSCAN, HDBSCAN |
| Reduce dimensionality | PCA |
| Visualize structure | UMAP, t-SNE |
| Detect anomalies | Isolation Forest, Local Outlier Factor, One-Class SVM |
| Evaluate cluster separation | Silhouette Score, Davies-Bouldin, Calinski-Harabasz |
| Find redundant features | Correlation, VIF, collinearity checks |

Typical flow:

```text
dataset without target
-> EDA and data cleaning
-> encoding and scaling when needed
-> PCA or UMAP for structure exploration
-> clustering or anomaly detection
-> human interpretation of groups/patterns
-> decision: segment, label, collect target, or continue exploration
```

Important limitation:

```text
The algorithm can produce group 0, group 1, and group 2.
The analyst gives those groups business meaning.
```

Unsupervised analysis is usually less conclusive than supervised feature importance because there is no ground-truth answer to optimize against.

---

## Feature Importance Means Different Things

In supervised learning:

```text
important feature = helps predict the target
```

In unsupervised learning:

```text
important feature = helps explain variance, separation, grouping, or anomaly behavior
```

This difference matters. A supervised feature importance chart answers a more direct question because it is anchored to a known target.

Without a target, feature relevance is more exploratory and depends on the analysis objective.

---

## Where Neural Networks Fit

Neural networks are not a separate learning type. They are model architectures.

A neural network can be used for:

- supervised classification;
- supervised regression;
- time-series forecasting;
- text, image, and audio tasks;
- embeddings;
- autoencoders;
- anomaly detection;
- self-supervised representation learning.

For regular tabular data, neural networks are usually not the first pre-analysis tool because they are often heavier, more sensitive to preprocessing, less interpretable, and require more tuning than tree-based models.

For unstructured data, neural networks are often central:

```text
text/image/audio
-> pretrained neural model
-> embedding
-> classifier, search, clustering, anomaly detection, or downstream model
```

Practical rule:

```text
Tabular supervised pre-analysis -> quick tree/linear probe first.
Text/image/audio pre-analysis -> embeddings or pretrained neural models may be the first useful representation.
```

---

## Analysis Families

### 1. Data Profiling & Statistical Summary

This is the "bird's-eye view" of your data. It includes checking the number of records, the number of features, and basic statistics such as mean, median, standard deviation, min, and max.

- **Goal**: Detect obvious scale issues or data entry errors.

### 2. Structural Integrity

Check for technical debt in the data:

- **Data Types**: Are numbers stored as strings? Are dates correctly recognized?
- **Missing Values**: How much data is absent? Is it missing at random?
- **Cardinality**: Do categorical features have too many unique values, such as a unique ID per row?
- **Duplicates**: Are there redundant rows that might inflate your performance metrics?

### 3. Distribution Analysis

Use histograms and density plots to see how values are spread.

- **Goal**: Identify outliers, skewed distributions, or unexpected gaps in the data.
- **Application**: Crucial for supervised learning and clustering.

### 4. Visual Relationship Checks

Use scatter plots or box plots to visualize the relationship between two variables.

- **Goal**: Identify non-linear patterns or clusters that summary statistics might miss.

### 5. Correlation & Redundancy

Measure how much features move together, for example with Pearson or Spearman correlation.

- **Multicollinearity**: High correlation between inputs can make some models unstable or their explanations harder to trust.
- **Redundancy**: If two features are nearly identical, you might only need one.

### 6. Leakage & Availability

This is the most critical check for supervised learning.

- **Target Leakage**: Does a feature contain information from the future? If a feature "predicts" the target perfectly, it is likely a bug.
- **Availability**: Will this feature actually be available at the exact moment the model needs to make a prediction in production?

### 7. Univariate Predictive Screening

Test each feature individually to see how well it predicts the target, for example using a simple proxy model or information gain.

- **Goal**: Identify the most promising candidates and potential leakage early.

### 8. Quick Baseline / Probe Model

Train a simple model or a fast tabular model on a controlled subset of features.

- **Goal**: Set a performance floor and measure early predictive signal.
- **Examples**: shallow tree, linear/logistic regression, Random Forest, XGBoost, LightGBM.
- **Caution**: A strong quick score can also indicate leakage. Always inspect feature availability.

### 9. Segment-Level Checks

Analyze performance and data distribution across different groups, such as region, category, channel, or customer segment.

- **Class Imbalance**: Is one category much rarer than others?
- **Bias**: Are there groups where the data quality is lower or the signal is missing?

### 10. Temporal Consistency

For time-series or temporally ordered data, check how distributions change over time.

- **Goal**: Ensure that your validation split, such as "past vs future", matches the real-world use case.

---

## Problem-Specific Application

| Analysis Family | Supervised Tabular | Time Series | Clustering | Vision / Text | Bandit / RL |
|---|---|---|---|---|---|
| Structural Integrity | Essential | Essential | Essential | Relevant | Essential |
| Distributions | Essential | Essential | Essential | Metadata only | Essential |
| Target Leakage | Critical | Critical | N/A | Relevant | Critical |
| Temporal Checks | Relevant | Critical | Relevant | Relevant | Essential |
| Segment Checks | Essential | Essential | Essential | Relevant | Essential |
| Quick Probe Model | Useful | Useful with temporal split | N/A | Useful after embeddings | Useful offline only |
| PCA / UMAP | Optional | Optional | Useful | Useful after embeddings | Optional |
| Clustering | Optional for segmentation | Optional | Core | Useful after embeddings | Optional |
| Anomaly Detection | Optional | Useful | Useful | Useful | Useful for monitoring |

---

## Practical Decision Map

```text
I have a dataset.
|
|-- Do I have a target?
|   |
|   |-- Yes
|   |   |-- Is the target categorical? -> supervised classification
|   |   |-- Is the target numeric?      -> supervised regression
|   |   `-- Pre-analysis: quick probe model, metrics, feature importance, leakage checks
|   |
|   `-- No
|       |-- Want groups?       -> clustering
|       |-- Want compression?  -> dimensionality reduction
|       |-- Want weird points? -> anomaly detection
|       `-- Pre-analysis: PCA/UMAP, clustering, anomaly detection, redundancy checks
```

---

## Learn More

- [scikit-learn: Common pitfalls in the interpretation of coefficients](https://scikit-learn.org/stable/auto_examples/inspection/plot_linear_model_coefficient_interpretation.html)
- [scikit-learn: Visualizing data](https://scikit-learn.org/stable/visualizations.html)
- [scikit-learn: Clustering](https://scikit-learn.org/stable/modules/clustering.html)
- [scikit-learn: Novelty and Outlier Detection](https://scikit-learn.org/stable/modules/outlier_detection.html)
- [XGBoost documentation](https://xgboost.readthedocs.io/)

## Limitations

- **Analysis is not Training**: These checks find problems; they do not fix them. You still need proper preprocessing, feature engineering, training, and evaluation.
- **False Signals**: High correlation or high feature importance does not imply causation. A "strong feature" in analysis might fail if the underlying process changes.
- **Unsupervised Ambiguity**: Clusters and anomalies are not automatically meaningful. They need human interpretation and validation.
- **Neural Network Cost**: Neural approaches can be powerful, especially for unstructured data, but they may be overkill for early tabular diagnostics.
- **Cost of Analysis**: Avoid analysis paralysis. The goal is to reach a reliable baseline quickly, not to find every possible correlation.
