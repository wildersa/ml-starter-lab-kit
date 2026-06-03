# Feature Engineering

Feature engineering means creating useful input columns for a model.

A feature is useful when it gives information that would be available at prediction time.

## Common feature types

| Type | Example | Useful for |
|---|---|---|
| Ratio | `price / quantity` | tabular models |
| Difference | `revenue - cost` | business metrics |
| Date parts | day, month, weekday | seasonality |
| Lag | value from 1 or 7 periods ago | time series |
| Rolling mean | average over last 7 days | trend/smoothing |
| Group aggregate | average by customer | behavior summary |

## Data leakage warning

Do not create features using information from the future.

Bad example:

```text
use total purchases after the campaign to predict campaign conversion
```

Better example:

```text
use purchases before the campaign to predict campaign conversion
```

## Practical rule

Before adding a feature, ask:

```text
Would I know this value at the moment of prediction?
```

If the answer is no, the feature is probably leaking information.
