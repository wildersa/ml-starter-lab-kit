# Initial ML Checklist

Use this checklist before training anything.

## 1. Define the problem

- Classification: predict a class.
- Regression: predict a number.
- Clustering: find groups.
- Time series: forecast future values.
- Bandit/RL: choose actions and learn from rewards.

## 2. Understand the data

Check:

- number of rows and columns;
- missing values;
- duplicated rows;
- target distribution;
- date columns;
- categorical columns;
- possible data leakage.

## 3. Create a baseline

A baseline is a simple reference.

Examples:

- majority class;
- average value;
- last known value;
- random policy;
- fixed business rule.

A complex model is only useful if it beats the baseline.

## 4. Split correctly

- Random split is fine for many tabular problems.
- Time series needs chronological split.
- User/event data may need grouped split.

## 5. Evaluate with the right metric

Examples:

- Accuracy: simple classification.
- F1: imbalanced classification.
- AUC: ranking/probability quality.
- MAE/RMSE: regression.
- MAPE: forecast error, when safe.
- Regret/reward: bandits.

## 6. Document limitations

Always write what the model should not be used for.
