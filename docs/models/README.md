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

## Model families

| Family | Use when | Start here |
|---|---|---|
| Supervised learning | You have input data and known answers | [Supervised learning](supervised.md) |
| Unsupervised learning | You do not have a target and want structure | [Unsupervised learning](unsupervised.md) |
| Time series | The order of events matters | [Time series and LSTM](time-series.md) |
| Image models | The input is an image or visual frame | [Image models / Computer Vision](vision.md) |
| Reinforcement Learning | An agent learns through actions and rewards | [Reinforcement Learning](reinforcement-learning.md) |
| Bandits | You choose among options and learn from feedback | [Multi-Armed Bandits](bandits.md) |

## Shared topics

- [Feature engineering](feature-engineering.md)
- [Feature measurement](../workflows/feature-measurement.md)
- [Metrics overview](../metrics/README.md)
- [Common mistakes](../common-mistakes/README.md)

## Shared project skeleton

Most ML projects start with the same basic structure:

```text
problem -> data -> EDA -> cleaning -> features -> baseline -> model -> evaluation
```

The starter kit creates the skeleton. The problem type defines the details.
