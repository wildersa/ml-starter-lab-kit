# Pre-Modeling Analysis

Before training complex models, it is essential to understand your data. Pre-modeling analysis is a diagnostic workflow that helps you identify bugs, signals, and risks early.

This guide organizes these analyses into a logical learning flow to help you decide if a dataset is ready for baseline modeling.

## Learning Flow

1.  **Understand the Dataset**: Get a high-level view of what you have.
2.  **Understand Distributions**: Look at individual columns in isolation.
3.  **Understand Feature Relationships**: See how columns interact with each other.
4.  **Protect Validation**: Ensure your evaluation strategy is robust against leakage.
5.  **Measure Early Predictive Signal**: Check if features actually relate to the target.
6.  **Inspect Segment-level Risk**: Look for imbalances or biases in specific groups.
7.  **Decision**: Determine if the data quality and signal are sufficient to proceed.

---

## Analysis Families

### 1. Data Profiling & Statistical Summary
This is the "bird's-eye view" of your data. It includes checking the number of records, the number of features, and basic statistics (mean, median, standard deviation, min/max).
- **Goal**: Detect obvious scale issues or data entry errors.

### 2. Structural Integrity
Check for technical debt in the data:
- **Data Types**: Are numbers stored as strings? Are dates correctly recognized?
- **Missing Values**: How much data is absent? Is it missing at random?
- **Cardinality**: Do categorical features have too many unique values (e.g., a unique ID per row)?
- **Duplicates**: Are there redundant rows that might inflate your performance metrics?

### 3. Distribution Analysis
Use histograms and density plots to see how values are spread.
- **Goal**: Identify outliers, skewed distributions, or unexpected gaps in the data.
- **Application**: Crucial for supervised learning and clustering.

### 4. Visual Relationship Checks
Use scatter plots or box plots to visualize the relationship between two variables.
- **Goal**: Identify non-linear patterns or clusters that summary statistics might miss.

### 5. Correlation & Redundancy
Measure how much features move together (e.g., using Pearson or Spearman correlation).
- **Multicollinearity**: High correlation between inputs can make some models unstable or their explanations harder to trust.
- **Redundancy**: If two features are nearly identical, you might only need one.

### 6. Leakage & Availability
This is the most critical check for supervised learning.
- **Target Leakage**: Does a feature contain information from the future? If a feature "predicts" the target perfectly, it is likely a bug.
- **Availability**: Will this feature actually be available at the exact moment the model needs to make a prediction in production?

### 7. Univariate Predictive Screening
Test each feature individually to see how well it predicts the target (e.g., using a simple proxy model or information gain).
- **Goal**: Identify the most promising candidates and potential leakage early.

### 8. Quick Baseline / Probe Model
Train a very simple model (like a shallow tree or linear model) on a subset of features.
- **Goal**: Set a "floor" for performance. If a simple model performs well, the problem might not need a complex solution.

### 9. Segment-Level Checks
Analyze performance and data distribution across different groups (e.g., by region, category, or demographic).
- **Class Imbalance**: Is one category much rarer than others?
- **Bias**: Are there groups where the data quality is lower or the signal is missing?

### 10. Temporal Consistency
For time-series or temporally ordered data, check how distributions change over time.
- **Goal**: Ensure that your validation split (e.g., "past vs future") matches the real-world use case.

---

## Problem-Specific Application

| Analysis Family | Supervised Tabular | Time Series | Clustering | Vision / Text | Bandit / RL |
|---|---|---|---|---|---|
| Structural Integrity | Essential | Essential | Essential | Relevant | Essential |
| Distributions | Essential | Essential | Essential | Metadata only | Essential |
| Target Leakage | Critical | Critical | N/A | Relevant | Critical |
| Temporal Checks | Relevant | Critical | Relevant | Relevant | Essential |
| Segment Checks | Essential | Essential | Essential | Relevant | Essential |

## Learn More

- [scikit-learn: Common pitfalls in the interpretation of coefficients](https://scikit-learn.org/stable/auto_examples/inspection/plot_linear_model_coefficient_interpretation.html)
- [scikit-learn: Visualizing data](https://scikit-learn.org/stable/visualizations.html)

## Limitations

- **Analysis is not Training**: These checks find problems; they don't fix them. You still need to perform proper preprocessing and feature engineering.
- **False Signals**: High correlation does not imply causation. A "strong feature" in analysis might fail if the underlying process changes.
- **Cost of Analysis**: Avoid "analysis paralysis." The goal is to reach a reliable baseline quickly, not to find every possible correlation.
