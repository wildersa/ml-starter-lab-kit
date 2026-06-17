# Feature Measurement and Analysis

Feature measurement and analysis help you understand which inputs actually drive your model's performance.

It is important to distinguish between two different activities:
1. **Feature Measurement (Before/After Delta):** Evaluating a specific *candidate* feature by comparing model performance with and without it.
2. **Feature Analysis (Importance/Screening):** Evaluating and ranking *existing* features in a dataset to see which ones appear most useful.

The goal is to avoid keeping features that add noise, leakage, cost, or complexity.

## Measuring a Candidate Feature

To decide if a new feature should be kept, use the **incremental delta** process:

```text
baseline features -> train/evaluate -> add candidate feature -> train/evaluate -> compare delta
```

### Consistency is Key
When comparing the "before" and "after" results, you **must** use the exact same:
- Data split (train/validation/test sets);
- Validation method (e.g., K-Fold);
- Random seed;
- Model family and hyperparameters;
- Evaluation metric.

## Analyzing Existing Features

If you want to rank features already in your dataset, consider these common methods:

| Method | Focus | Best For |
|---|---|---|
| **Univariate Screening** | Individual relationship between a feature and the target. | Quick initial filtering of irrelevant columns. |
| **Model-based Importance** | How much the model relied on a feature during training. | Understanding the internal logic of a specific model. |
| **Permutation Importance** | How much the score drops when a feature's values are shuffled. | Measuring actual impact on prediction error regardless of model type. |

## What to measure

| Check | Question |
|---|---|
| Metric delta | Did the validation metric improve? |
| Segment delta | Did it help all important segments or only one? |
| Stability | Does the feature behave similarly in train/validation/test? |
| Leakage risk | Would this value exist at prediction time? |
| Missingness | Is the feature often missing? |
| Cost | Is it expensive to compute or serve? |
| Interpretability | Can the feature be explained? |

## Simple decision rule

Keep a feature when it has:

- **Measurable validation gain:** A clear improvement in your chosen metric.
- **Stable behavior:** Consistent performance across different data splits.
- **Prediction availability:** The data is guaranteed to exist at inference time.

Remove or investigate a feature when it has:

- **Suspiciously high signal:** If a single feature leads to "perfect" or near-perfect scores, it is likely a sign of **target leakage** (the feature contains information the model is trying to predict).
- **No measurable gain:** Adding the feature increases complexity without improving the metric.
- **Future information:** The feature relies on data that wouldn't be known in production.

## Suggested report

```text
Feature: customer_avg_purchase_30d
Metric before: 0.712
Metric after: 0.728
Delta: +0.016
Decision: keep
Reason: stable gain, no obvious leakage
```

## Practical warning

A feature that improves training score but not validation score probably did not help.
