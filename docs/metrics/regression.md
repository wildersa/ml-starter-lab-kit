# Regression Metrics

Use regression metrics when the model predicts a continuous number (e.g., price, temperature, or distance).

For a deeper dive into how to measure model performance and how it relates to business value, see the [Evaluation and Monitoring](../concepts/evaluation-and-monitoring.md) guide.

## MAE (Mean Absolute Error)

- **What it answers:** On average, how far off are the predictions from the actual values?
- **When to use:** When you want an error metric that is in the same units as your target and is easy to explain to non-technical stakeholders.
- **When to avoid:** When large outlier errors are much more "painful" than small ones.
- **Common trap:** Comparing MAE across different datasets with different scales.
- **Example:** If you predict house prices and your MAE is $10,000, your predictions are off by $10,000 on average.

## RMSE (Root Mean Squared Error)

- **What it answers:** What is the average magnitude of the error, with a heavier penalty on large misses?
- **When to use:** When large errors are particularly undesirable (e.g., being off by 10 days on a delivery is much worse than being off by 1 day 10 times).
- **When to avoid:** When your data has many outliers that are actually correct but will dominate the metric.
- **Common trap:** Expecting RMSE to be as easy to interpret as MAE. It is always higher than or equal to MAE.
- **Example:** A $50,000 error in a $200,000 house prediction will increase RMSE significantly more than it would increase MAE.

## MAPE (Mean Absolute Percentage Error)

- **What it answers:** What is the average percentage error relative to the actual values?
- **When to use:** When you need to communicate error to people who don't know the scale of the data (e.g., "The model is 95% accurate on average").
- **When to avoid:** **Crucial Limitation:** When actual values are zero or very close to zero, as the division will lead to undefined or extreme values.
- **Common trap:** Using MAPE on data that can be zero (like rainfall or daily sales for a small store).
- **Example:** Predicting 110 for an actual value of 100 gives a 10% MAPE.

## R² (R-Squared)

- **What it answers:** How much of the variance in the target is explained by the model?
- **When to use:** To get a sense of how much better your model is than just predicting the average value.
- **When to avoid:** When you care about the absolute error rather than the relative explanation of variance.
- **Common trap:** A high R² does not mean the model is "good" if the underlying data is very noisy or if the model is overfitted.
- **Example:** An R² of 0.8 means your model explains 80% of the movement in the data.
