# Feature Engineering

Feature engineering is the process of **creating or transforming** input columns to improve model performance.

While **Feature Analysis** evaluates the importance of existing columns, **Feature Engineering** focuses on building new ones from raw data or existing features.

### The Golden Rule
A feature is only valid if it is **available at prediction time**. If a feature relies on information that wouldn't be known when the model is actually used, it causes "data leakage" and creates false confidence in model results.

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

## Measuring if a feature helped

Do not keep a feature only because it looks clever.

Measure it.

Useful checks:

- compare baseline without the feature vs. baseline with the feature;
- use the same split and the same metric;
- inspect improvement by segment, not only global score;
- check if the feature increases leakage risk;
- check if the feature is stable across train, validation, and test;
- remove features that add complexity without measurable gain.

A simple feature impact table can look like this:

| Feature | Metric before | Metric after | Delta | Keep? | Note |
|---|---:|---:|---:|---|---|
| `customer_avg_purchase_30d` | 0.712 | 0.728 | +0.016 | yes | stable gain |
| `campaign_duration` | 0.712 | 0.801 | +0.089 | no | leakage risk |

See [feature measurement](../workflows/feature-measurement.md).

## Practical rule

Before adding a feature, ask:

```text
Would I know this value at the moment of prediction?
```

If the answer is no, the feature is probably leaking information.

Then ask:

```text
Does this feature improve the metric on validation data?
```

If the answer is no, remove it or document why it stays.
