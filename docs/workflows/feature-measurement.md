# Feature Measurement

Feature measurement is the practice of checking whether a new feature actually improves the model.

The goal is to avoid keeping features that add noise, leakage, cost, or complexity.

## Basic process

```text
baseline features -> train/evaluate -> add candidate feature -> train/evaluate -> compare delta
```

Use the same:

- data split;
- validation method;
- random seed;
- model family;
- metric.

## What to measure

| Check | Question |
|---|---|
| Metric delta | Did the validation metric improve? |
| Segment delta | Did it help all important segments or only one? |
| Stability | Does the feature behave similarly in train/validation/test? |
| Leakage risk | Would this value exist at prediction time? |
| Missingness | Is the feature often missing? |
| Cost | Is it expensive to compute or serve? |
| Interpretability | Can the feature be explained? |

## Simple decision rule

Keep a feature when it has:

- measurable validation gain;
- no obvious leakage;
- acceptable missingness;
- acceptable complexity.

Remove or quarantine a feature when it has:

- suspiciously large improvement;
- future information;
- unstable behavior;
- no measurable gain.

## Suggested report

```text
Feature: customer_avg_purchase_30d
Metric before: 0.712
Metric after: 0.728
Delta: +0.016
Decision: keep
Reason: stable gain, no obvious leakage
```

## Practical warning

A feature that improves training score but not validation score probably did not help.
