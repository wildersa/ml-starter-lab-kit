# Evaluation and Monitoring

This page explains how to measure if your model is working and how to ensure it stays useful after it is deployed.

## 1. Evaluation vs. Monitoring

Beginners often confuse these two concepts, but they happen at different stages of the ML lifecycle.

- **Evaluation** (Offline): Happens **before** the model goes to production. You use historical data (test set) to see how the model *would have* performed.
- **Monitoring** (Online): Happens **after** the model is in production. You track how it *is* performing on real, live data.

**Example**:
Imagine a model that predicts if a bank transaction is fraudulent.
- **Evaluation**: You test the model on last month's data and see it caught 90% of known frauds.
- **Monitoring**: Today, you notice the model is only flagging 50% of transactions as fraud compared to yesterday. Something might be wrong with the live data.

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

**Practical Example**:
A model predicts engine failure.
- **Technical**: 95% Recall (it catches 95% of failures).
- **Business**: $10,000 saved per month in avoided emergency repairs.

## 4. Thresholds: Deciding when to act

Most models output a **probability** (e.g., "85% chance this is spam") rather than a simple Yes/No. A **threshold** is the cutoff point you choose to take an action.

- **High Threshold (0.9)**: You only flag spam if you are very sure. You miss some spam (Lower Recall), but you never block a real email (Higher Precision).
- **Low Threshold (0.1)**: You flag almost everything. You catch all spam (Higher Recall), but many real emails are wrongly blocked (Lower Precision).

## 5. Overfitting and Underfitting

These terms describe how well the model learned the "noise" vs. the "pattern".

- **Underfitting**: The model is too simple. It performs poorly on both training and test data. *Example: Trying to predict house prices using only the color of the front door.*
- **Overfitting**: The model is too complex and "memorized" the training data. It looks perfect during training but fails on new data. *Example: A student memorizing the answers to a specific practice exam but failing the real exam because the questions changed slightly.*

## 6. Drift and Retraining

A model's performance usually gets worse over time because the world changes. This is called **Drift**.

- **Data Drift**: The input data changes. *Example: Your model was trained on data from iPhone users, but now most of your users are on Android.*
- **Concept Drift**: The relationship between input and output changes. *Example: Before a pandemic, people bought travel insurance; after it starts, their buying behavior changes completely.*
- **Performance Drift**: The model's accuracy starts dropping in the real world.

**Retraining Trigger**: You should retrain your model when you detect significant drift or when performance drops below a predefined threshold.

## 7. Metrics Mapping by Problem Type

| Family | Task | Common Metrics |
|---|---|---|
| **Classification** | Predicting a category (Spam/Not Spam) | Accuracy, Precision, Recall, F1-Score, AUC-ROC |
| **Regression** | Predicting a number (Price, Temperature) | MAE, RMSE, R-squared |
| **Time Series** | Predicting values over time | MAE, MAPE, WAPE |
| **Clustering** | Grouping similar items | Silhouette Score, Inertia |
| **Vision** | Finding objects in images | mAP (Mean Average Precision), IoU (Intersection over Union) |
| **Bandits** | Sequential decision making | Cumulative Reward, Regret |
