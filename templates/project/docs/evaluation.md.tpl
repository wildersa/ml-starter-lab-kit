# Evaluation Guide — {{PROJECT_NAME}}

This guide explains how to measure the results of your `{{TASK}}` project.

## Evaluation Flow

To trust your model, you should follow this standard flow:

1.  **Dataset Split**: Divide your data into Training and Test sets. Never evaluate on the same data used for training.
2.  **Target**: The actual value you want to predict (ground truth).
3.  **Prediction**: The value produced by your model.
4.  **Baseline**: A simple rule (like "always predict the average") to compare against. If your model isn't better than the baseline, it's not ready.
5.  **Metric**: A mathematical formula that summarizes how close predictions are to targets.
6.  **Interpretation**: Understanding what the metric means for your business or problem.
7.  **Next Experiment**: Using the results to decide how to improve (e.g., adding features or changing the model).

{% if TASK == "supervised" %}
{% if DEMO_SUBTYPE == "classification" %}
## Classification Evaluation

Since you are predicting categories, focus on these concepts:

### Confusion Matrix
The foundation of classification. It shows:
- **True Positives (TP)**: Correctly predicted positive.
- **True Negatives (TN)**: Correctly predicted negative.
- **False Positives (FP)**: Wrongly predicted positive (False Alarm).
- **False Negatives (FN)**: Wrongly predicted negative (Missed Opportunity).

### Key Metrics
- **Precision**: Of all predicted positives, how many were right? Use this when **False Positives** are expensive.
- **Recall**: Of all actual positives, how many did we find? Use this when **False Negatives** are expensive.
- **F1-Score**: The balance between Precision and Recall.

### Thresholds and Costs
Most models output a probability (0.0 to 1.0). By default, we use **0.5** as a threshold.
- If a **False Positive** is very costly (e.g., blocking a good customer), increase the threshold (e.g., to 0.8).
- If a **False Negative** is very costly (e.g., missing a disease), decrease the threshold (e.g., to 0.2).
{% else %}
## Regression Evaluation

Since you are predicting numbers, focus on these metrics:

- **MAE (Mean Absolute Error)**: The average error in the same units as your target. Very easy to interpret.
- **RMSE (Root Mean Squared Error)**: Similar to MAE but penalizes large errors more heavily.
- **MAPE (Mean Absolute Percentage Error)**: Shows the error as a percentage (e.g., "the model is off by 10% on average").

**Avoid Accuracy**: Do not use "accuracy" for regression. A prediction of 95 when the target is 100 is "wrong" in accuracy terms, but "close" in regression terms.
{% endif %}
{% endif %}

{% if TASK == "timeseries" %}
## Time Series Evaluation

Evaluating time series requires special care because order matters.

- **Backtesting**: Instead of a random split, use a "cut-off" point in time. Train on the past, test on the "future".
- **Forecast Horizon**: Measure how performance drops as you try to predict further into the future.
- **Metrics**: Use MAE, RMSE, or MAPE, similar to regression, but calculate them per time step.
{% endif %}

{% if TASK == "unsupervised" %}
## Unsupervised Evaluation

Since there is no "target", we measure how well the model finds patterns.

- **Clustering (e.g., K-Means)**: Use the **Silhouette Score** to see how well-separated your groups are.
- **Internal Consistency**: Do items in the same group actually look similar to a human expert?
- **Stability**: If you run the model again with slightly different data, do the groups stay the same?
{% endif %}

{% if TASK == "vision" %}
## Vision Evaluation

- **Image Classification**: Uses the same metrics as Classification (Precision, Recall, F1).
- **Object Detection**: Uses **mAP (mean Average Precision)**, which accounts for how well the "box" overlaps with the object.
{% endif %}

{% if TASK == "bandit" or GENERATE_BANDIT == "true" %}
## Multi-Armed Bandit Evaluation

Bandits learn while doing, so we measure "learning efficiency":

- **Cumulative Reward**: The total sum of rewards obtained over time.
- **Regret**: The difference between the reward you *could* have gotten with the best arm and what you actually got. Lower is better.
- **Arm Selection**: Are we converging on the best option over many rounds?
{% endif %}

{% if TASK == "generic" %}
## Generic Evaluation

Define your success criteria based on your specific goal.
1. Identify your target.
2. Choose a metric that penalizes the "wrong" behavior for your use case.
3. Compare against a "common sense" baseline.
{% endif %}

## References
For more details on specific metrics, visit the [Metrics Documentation](../../docs/metrics/README.md).
