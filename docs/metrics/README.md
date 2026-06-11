# Metrics Overview

Metrics tell you if the model is useful for the problem.

Do not choose a metric only because it is popular. Choose it because it matches the **decision** you need to make and the **cost of being wrong**.

## Quick map

| Problem | Recommended Metrics |
|---|---|
| Classification | [Accuracy, Precision, Recall, F1, AUC](classification.md) |
| Regression | [MAE, RMSE, R², MAPE](regression.md) |
| Clustering | [Silhouette, Inertia, Interpretation](clustering.md) |
| Time series | [MAE, RMSE, sMAPE, Backtesting](time-series.md) |
| Bandits | [Reward, Regret, Lift, Exploration](bandits.md) |
| Vision | [mAP, IoU, Dice, F1](vision.md) |

## Related guides

- [Metric mismatch](../common-mistakes/metric-mismatch.md)
- [Feature measurement](../workflows/feature-measurement.md)
- [Before evaluation checklist](../checklists/before-evaluation.md)

## Practical rule

A good metric should answer:

> "Did the model improve the decision I care about?"

If your metric improves but your business outcome doesn't, you are measuring the wrong thing.
- Review the [Evaluation and Monitoring](../concepts/evaluation-and-monitoring.md) concept for the full lifecycle.
