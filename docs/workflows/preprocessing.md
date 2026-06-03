# Preprocessing

Preprocessing prepares raw data before feature engineering and model training.

It is not the same as feature engineering. Preprocessing usually fixes the data. Feature engineering creates new useful signals.

## Common preprocessing steps

| Step | Purpose |
|---|---|
| Type conversion | convert dates, numbers, booleans |
| Missing values | fill, flag, or remove missing values |
| Encoding | convert categories into numeric representation |
| Scaling | put numeric values on comparable scales |
| Deduplication | remove repeated rows when appropriate |
| Leakage removal | remove columns not available at prediction time |

## Does every model need scaling?

No.

Scaling is important for models that depend on distance, variance, gradients, or numerical optimization.

## Scaling usually matters for

- K-Means;
- PCA;
- KNN;
- SVM;
- Logistic Regression with regularization;
- Linear Regression with regularization;
- Neural networks;
- LSTM;
- DBSCAN;
- image pixel normalization.

## Scaling usually does not matter much for

- Decision Trees;
- Random Forest;
- XGBoost;
- LightGBM;
- CatBoost;
- simple rule-based baselines.

## Practical rule

Do not create a `scaler.py` for everything. A better module name is:

```text
preprocessing.py
```

Because scaling is only one part of preprocessing.
