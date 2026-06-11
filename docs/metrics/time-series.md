# Time Series Metrics

Time series evaluation requires a special focus on the temporal order of data. You must evaluate how the model performs on "future" data relative to what it saw during training.

## Recommended Metrics

Time series often use the same metrics as regression (MAE, RMSE, MAPE), but with a different evaluation strategy.

- **MAE**: Best for general accuracy in the same units.
- **RMSE**: Best when large forecasting misses are catastrophic.
- **sMAPE (Symmetric MAPE)**: A variation of MAPE that is more robust when actual values are small or zero.

## Evaluation Strategy: Backtesting

- **What it answers**: If I had used this model in the past, how would it have performed?
- **When to use it**: Always for time series. Instead of random splits, use a **Sliding Window** or **Expanding Window** (Time Series Cross-Validation).
- **Common trap**: Evaluating on random rows (shuffling) causes "Temporal Leakage", where the model sees the future to predict the past, leading to unrealistic performance.

## Forecast Horizon and Window

- **Horizon**: How far into the future are you predicting? (e.g., predict the next 7 days). Metrics often degrade as the horizon increases.
- **Window**: The amount of past data used to make a prediction (e.g., use the last 30 days to predict the next 1).

---

### Next Steps

Always check the [Before Evaluation Checklist](../checklists/before-evaluation.md) to ensure your temporal split is correct and you are not "leaking" future information into the past.
- Review the [Evaluation and Monitoring](../concepts/evaluation-and-monitoring.md) concept for the full lifecycle.
