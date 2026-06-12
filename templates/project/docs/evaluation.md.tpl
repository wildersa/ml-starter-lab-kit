# Evaluation Concepts

This page explains how to measure if your model is working and how to ensure it is useful.

## 1. Evaluation (Offline)

Evaluation happens **before** the model goes to production. You use historical data (test set) to see how the model *would have* performed.

**Example**:
Imagine a model that predicts if a bank transaction is fraudulent. You test the model on last month's data and see it caught 90% of known frauds.

## 2. The Baseline: Your Performance Floor

A **baseline** is the simplest possible way to solve the problem without a complex model. You must beat the baseline for your model to be considered useful.

- **Examples**:
    - Predict the average value (Regression).
    - Predict the most frequent class (Classification).
    - Predict that tomorrow's weather will be exactly the same as today's (Time Series).

**Why it matters**: If your complex Neural Network has 70% accuracy, but a simple rule "always predict Yes" has 75% accuracy, your model is worse than doing nothing.

## 3. Technical vs. Business Metrics

Models are trained on math, but they are used for business.

- **Technical Metric**: Measures the mathematical error (e.g., Mean Squared Error, F1-Score).
- **Business Metric**: Measures the real-world impact (e.g., Saved money, reduced churn, increased clicks).

## 4. Thresholds: Deciding when to act

Most models output a **probability** (e.g., "85% chance this is spam") rather than a simple Yes/No. A **threshold** is the cutoff point you choose to take an action.

- **High Threshold (0.9)**: You only flag spam if you are very sure. You miss some spam (Lower Recall), but you never block a real email (Higher Precision).
- **Low Threshold (0.1)**: You flag almost everything. You catch all spam (Higher Recall), but many real emails are wrongly blocked (Lower Precision).

## 5. Overfitting and Underfitting

These terms describe how well the model learned the "noise" vs. the "pattern".

- **Underfitting**: The model is too simple. It performs poorly on both training and test data.
- **Overfitting**: The model is too complex and "memorized" the training data. It looks perfect during training but fails on new data.

## 6. Metrics Mapping by Problem Type

| Family | Task | Common Metrics |
|---|---|---|
| **Classification** | Predicting a category | Accuracy, Precision, Recall, F1-Score, AUC-ROC |
| **Regression** | Predicting a number | MAE, RMSE, R-squared |
| **Time Series** | Predicting values over time | MAE, MAPE, WAPE |
| **Clustering** | Grouping similar items | Silhouette Score, Inertia |
| **Vision** | Finding objects in images | mAP, IoU |
| **Bandits** | Sequential decision making | Cumulative Reward, Regret |
