# Time Series Metrics

Time series forecasting requires special metrics because data has a temporal order. You cannot simply shuffle your rows.

For a deeper dive into how to measure model performance and how it relates to business value, see the [Evaluation and Monitoring](../concepts/evaluation-and-monitoring.md) guide.

## Backtesting (Walk-forward evaluation)

- **What it answers:** How would my model have performed if I had used it in the past to predict the future?
- **When to use:** Always for time series. Instead of a random split, you train on "Past" and test on "Future".
- **When to avoid:** Never. Traditional cross-validation (randomly picking rows) will leak future information into the past.
- **Common trap:** Using random K-fold cross-validation. This is a top cause of "fake" high performance in time series.
- **Example:** Training on data from Jan-Oct to predict November, then Jan-Nov to predict December.

## Horizon and Window Evaluation

- **What it answers:** Does the model's accuracy change as we try to predict further into the future (Short-term vs Long-term)?
- **When to use:** When your business needs to plan multiple steps ahead (e.g., inventory for the next 7 days).
- **When to avoid:** When you only ever care about the very next time step.
- **Common trap:** Reporting a single error number for a 30-day forecast. Usually, day 1 is much more accurate than day 30.
- **Example:** Measuring MAE specifically for "1-day ahead", "7-days ahead", and "30-days ahead".

## MAE and RMSE (Time series context)

- **What it answers:** The same as in regression, but analyzed over time.
- **When to use:** To understand the absolute scale of the error in your forecast.
- **Common trap:** Not checking if the error is "biased" (e.g., the model always under-predicts during weekends).

## MAPE and sMAPE

- **What it answers:** Percentage error, allowing comparison across products with different sales volumes.
- **When to use:** When you need to compare the forecast quality of a high-volume item vs a low-volume item.
- **When to avoid:** **Limitation:** Like in regression, avoid when values can be zero. **sMAPE** (Symmetric MAPE) handles zeros slightly better but is harder to interpret.
- **Common trap:** Relying on MAPE for "lumpy" demand (items that sell zero most days).
- **Example:** A 10% error on a product that sells 1000 units is the same "score" as a 10% error on one that sells 10 units.
