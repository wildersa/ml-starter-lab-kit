# Scaling Mistakes

Scaling is useful, but not always necessary.

## Common mistakes

- scaling after using all data, before the split;
- forgetting scaling for K-Means or PCA;
- assuming XGBoost needs scaling by default;
- scaling IDs or categorical codes as if they were numeric values.

## Practical rule

Scale when the model uses distance, variance, gradients, or numerical optimization.

Do not scale blindly.
