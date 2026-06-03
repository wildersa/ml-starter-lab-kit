# Supervised Learning

Use supervised learning when you have examples with known answers.

```text
features -> target
```

Examples:

- predict if a customer will convert;
- predict house price;
- classify fraud;
- predict churn.

## Main types

| Type | Target | Example metric |
|---|---|---|
| Classification | category/class | accuracy, F1, AUC |
| Regression | number | MAE, RMSE, R² |

## Typical workflow

```text
data -> EDA -> split -> preprocessing -> baseline -> model -> evaluation
```

## Common models

- Logistic Regression
- Decision Tree
- Random Forest
- XGBoost/LightGBM/CatBoost
- Neural networks, when justified

## Practical advice

Start with a simple baseline before using a powerful model.

For tabular data, tree-based models are usually a strong first serious option.

## Common mistakes

- Using future data as features.
- Evaluating only on training data.
- Ignoring class imbalance.
- Choosing accuracy when F1/AUC would be more useful.
