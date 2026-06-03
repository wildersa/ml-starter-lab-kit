# Metrics Overview

Metrics tell you if the model is useful for the problem.

Do not choose a metric only because it is popular. Choose it because it matches the decision.

## Quick map

| Problem | Start with |
|---|---|
| Classification | [Accuracy, F1, AUC](classification.md) |
| Regression | [MAE, RMSE, R²](regression.md) |
| Clustering | [Silhouette, inertia](clustering.md) |
| Time series | [MAE, RMSE, MAPE](time-series.md) |
| Bandits | [Reward, regret](bandits.md) |
| Vision | [F1, mAP, IoU, Dice](vision.md) |

## Related guides

- [Metric mismatch](../common-mistakes/metric-mismatch.md)
- [Feature measurement](../workflows/feature-measurement.md)
- [Before evaluation checklist](../checklists/before-evaluation.md)

## Practical rule

A good metric should answer:

```text
Did the model improve the decision I care about?
```
