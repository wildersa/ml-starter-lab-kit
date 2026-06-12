# Monitoring and Drift

This page explains how to ensure your model stays useful after it is deployed.

## 1. Monitoring (Online)

Monitoring happens **after** the model is in production. You track how it *is* performing on real, live data.

**Example**:
Imagine a model that predicts if a bank transaction is fraudulent. Today, you notice the model is only flagging 50% of transactions as fraud compared to yesterday. Something might be wrong with the live data.

## 2. Drift and Retraining

A model's performance usually gets worse over time because the world changes. This is called **Drift**.

- **Data Drift**: The distribution of input data changes. *Example: Your model was trained on data from iPhone users, but now most of your users are on Android.*
- **Concept Drift**: The relationship between input and output changes. *Example: Before a pandemic, people bought travel insurance; after it starts, their buying behavior changes completely.*
- **Performance Drift**: The model's accuracy starts dropping in the real world compared to what was seen during training.

**Retraining Trigger**: You should retrain your model when you detect significant drift or when performance drops below a predefined threshold.

## 3. Task-Specific Signals

Different types of ML tasks require watching different signals:

- **Classification**: Watch for changes in the distribution of predicted classes and confidence scores. Are you suddenly predicting much more of one class?
- **Regression**: Watch for increases in prediction error (e.g., MAE, RMSE) and changes in the range of predicted values.
- **Time-series**: Watch for changes in seasonality, trends, or sudden outliers that the model hasn't seen before.
- **Clustering**: Watch for the "compactness" of clusters. Are new data points falling far away from existing cluster centers?
- **Vision**: Watch for changes in image quality, lighting conditions, or new types of objects (covariate shift).
- **Bandit/Adaptive**: Watch the "Regret" and "Best Arm Selection Rate". If a previously winning strategy starts failing, the environment might have shifted.

## 4. How to detect Drift?

A simple way to start is to compare the **Training Data** (your baseline) with the **Serving Data** (new data).

1. **Check the Schema**: Did a new category appear? Is a column now missing or full of nulls?
2. **Compare Distributions**: Use histograms or statistics (Mean, Std Dev) to see if the new data "looks" like the training data.
3. **Monitor Predictions**: If you don't have the "true labels" yet, tracking the distribution of your predictions is a great proxy for detecting drift.
