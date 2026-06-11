# Metrics Overview

Metrics tell you if the model is useful for the problem.

Do not choose a metric only because it is popular. Choose it because it matches the decision you need to make.

## Quick map

| Problem | Key Metrics |
|---|---|
| **[Classification](classification.md)** | Confusion Matrix, Accuracy, Precision, Recall, F1, AUC, Thresholds |
| **[Regression](regression.md)** | MAE, RMSE, MAPE, R² |
| **[Time series](time-series.md)** | MAE, RMSE, MAPE, Backtesting, Horizon evaluation |
| **[Clustering](clustering.md)** | Inertia, Silhouette Score, Qualitative Interpretation |
| **[Vision](vision.md)** | mAP, IoU, Dice Score, Image Classification metrics |
| **[Bandits](bandits.md)** | Reward, Cumulative Reward, Regret, Lift, User Drift |

## Core Principles

For a deeper dive into the fundamental concepts of measuring ML success, see the **[Evaluation and Monitoring](../concepts/evaluation-and-monitoring.md)** guide.

### Related guides

- [Metric mismatch](../common-mistakes/metric-mismatch.md)
- [Feature measurement](../workflows/feature-measurement.md)
- [Before evaluation checklist](../checklists/before-evaluation.md)

### Practical rule

A good metric should answer:
> **"Did the model improve the decision I care about?"**
