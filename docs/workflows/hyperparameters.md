# Hyperparameters

Hyperparameters are settings chosen before or around training.

They are not learned directly from the data in the same way model weights are.

## Are hyperparameters the same for every model?

No.

Every model family has its own hyperparameters.

## Common categories

| Category | Examples |
|---|---|
| Model hyperparameters | `max_depth`, `n_estimators`, `n_clusters`, `n_components` |
| Training hyperparameters | `learning_rate`, `epochs`, `batch_size` |
| Preprocessing hyperparameters | scaler type, fill strategy, encoding strategy |
| Search hyperparameters | grid size, number of trials, random seed |

## Examples by model family

| Model/family | Common hyperparameters |
|---|---|
| XGBoost | `max_depth`, `learning_rate`, `n_estimators`, `subsample` |
| K-Means | `n_clusters`, `init`, `max_iter`, `random_state` |
| PCA | `n_components`, whitening option |
| LSTM | number of units, layers, dropout, sequence length, epochs, batch size |
| Random Forest | `n_estimators`, `max_depth`, `min_samples_leaf` |
| Bandits | exploration rate, priors, confidence parameter |

## Practical advice

Start with a small number of important hyperparameters.

Do not tune everything at once.

See also: [hyperparameter optimization](hyperparameter-optimization.md).
