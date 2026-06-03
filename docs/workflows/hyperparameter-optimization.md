# Hyperparameter Optimization

Hyperparameters are settings chosen before training.

Examples:

- tree depth;
- learning rate;
- number of estimators;
- regularization;
- batch size;
- number of epochs.

## Start simple

1. Train a baseline.
2. Change one or two important parameters.
3. Compare with the same validation method.
4. Keep notes.

## Common approaches

| Approach | Use when |
|---|---|
| Manual search | learning or small projects |
| Grid search | few parameters and small search space |
| Random search | larger search space |
| Bayesian optimization | more advanced tuning |

## Practical warning

Do not tune on the final test set. Use validation data or cross-validation.
