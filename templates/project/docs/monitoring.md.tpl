# Monitoring and Drift

This page explains how to ensure your model stays useful after it is deployed.

## 1. Monitoring (Online)

Monitoring happens **after** the model is in production. You track how it *is* performing on real, live data.

**Example**:
Imagine a model that predicts if a bank transaction is fraudulent. Today, you notice the model is only flagging 50% of transactions as fraud compared to yesterday. Something might be wrong with the live data.

## 2. Drift and Retraining

A model's performance usually gets worse over time because the world changes. This is called **Drift**.

- **Data Drift**: The input data changes. *Example: Your model was trained on data from iPhone users, but now most of your users are on Android.*
- **Concept Drift**: The relationship between input and output changes. *Example: Before a pandemic, people bought travel insurance; after it starts, their buying behavior changes completely.*
- **Performance Drift**: The model's accuracy starts dropping in the real world.

**Retraining Trigger**: You should retrain your model when you detect significant drift or when performance drops below a predefined threshold.
