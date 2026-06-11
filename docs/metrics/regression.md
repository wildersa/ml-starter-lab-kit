# Regression Metrics

Use regression metrics when your model predicts a continuous number (e.g., house prices, temperature, or sales volume).

## MAE (Mean Absolute Error)

- **What it answers**: On average, how far off are the predictions in the same units as the target?
- **When to use it**: When you want an error metric that is easy to explain to non-technical stakeholders. It treats all errors equally.
- **When to avoid it**: When you want to specifically penalize large outliers.
- **Example**: An MAE of 5.0 in house price prediction (in thousands) means the model is off by $5,000 on average.

## RMSE (Root Mean Squared Error)

- **What it answers**: What is the magnitude of the error, with a higher penalty for large misses?
- **When to use it**: When large errors are much more costly than small errors.
- **Common trap**: RMSE is sensitive to outliers. A single huge miss can significantly inflate the RMSE.
- **Example**: If most errors are small but one is very large, RMSE will be much higher than MAE.

## R² (Coefficient of Determination)

- **What it answers**: How much of the variance in the data is explained by the model?
- **When to use it**: To understand how much better your model is than just predicting the average value.
- **When to avoid it**: On its own. A high R² doesn't mean the model is "good" if it's biased or if the data has specific patterns the model misses.
- **Example**: An R² of 0.80 means 80% of the variation in the target is explained by your features.

## MAPE (Mean Absolute Percentage Error)

- **What it answers**: What is the average percentage error?
- **When to use it**: When you need to communicate error in relative terms (e.g., "we are off by 10%").
- **When to avoid it**: When actual values can be zero or very close to zero (as it leads to division by zero or extreme values).
- **Common trap**: MAPE is asymmetric; it penalizes over-predictions less than under-predictions.
- **Example**: A MAPE of 0.10 means your predictions are, on average, 10% away from the actual value.

---

### Next Steps

Always check the [Before Evaluation Checklist](../checklists/before-evaluation.md) to ensure your metrics are reliable and match your business goals.
- Review the [Evaluation and Monitoring](../concepts/evaluation-and-monitoring.md) concept for the full lifecycle.
