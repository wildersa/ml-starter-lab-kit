# ML Architectures

This folder shows simplified Machine Learning architectures.

The goal is not to be complete. Use these diagrams as starting points to understand how ML projects are usually organized.

## Architecture vs model layers

In ML, the word layer can mean two different things:

1. **Pipeline layers**: data, validation, features, training, evaluation, serving, monitoring.
2. **Neural network layers**: Dense, Conv2D, LSTM, attention blocks, etc.

Most ML projects can have pipeline layers. Only neural network projects have neural network layers.

## Architecture guides

| Guide | Use for |
|---|---|
| [ML pipeline layers](layers.md) | understanding common ML project layers |
| [Basic tabular training](basic-tabular-training.md) | supervised tabular projects |
| [Unsupervised learning pipeline](unsupervised-pipeline.md) | PCA/K-Means/clustering projects |
| [Time series pipeline](time-series-pipeline.md) | forecasting and temporal projects |
| [Image training pipeline](image-training-pipeline.md) | image models and fine-tuning |
| [Bandit decision pipeline](bandit-decision-pipeline.md) | adaptive decision systems |
| [Basic MLOps lifecycle](mlops-lifecycle.md) | training, approval, serving, monitoring |

## Related sections

- [Workflows](../workflows/README.md)
- [Model overview](../models/README.md)
- [Metrics overview](../metrics/README.md)
