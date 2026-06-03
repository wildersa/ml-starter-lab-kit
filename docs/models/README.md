# Model Overview

This folder gives short, practical notes about common Machine Learning model families.

It is not a deep theory guide. Use it to decide where to start and what each workflow usually needs.

## Start with the question

Before choosing a model, ask:

1. What am I trying to predict, group, rank, or optimize?
2. Do I have a target column?
3. Is time order important?
4. Do decisions affect future data?
5. What metric proves that the model helps?

## Common families

| Family | Use when | Examples |
|---|---|---|
| Supervised learning | You have input data and known answers | XGBoost, Random Forest, Logistic Regression |
| Unsupervised learning | You do not have a target and want structure | K-Means, PCA, clustering |
| Time series | The order of events matters | ARIMA, Prophet, LSTM, temporal features |
| Reinforcement Learning | An agent learns by actions and rewards | Q-learning, policy gradients |
| Bandits | You choose among options and learn from feedback | Thompson Sampling, UCB, LinUCB |

## Shared project skeleton

Most ML projects start with the same basic structure:

```text
problem -> data -> EDA -> cleaning -> features -> baseline -> model -> evaluation
```

The starter kit creates the skeleton. The problem type defines the details.
