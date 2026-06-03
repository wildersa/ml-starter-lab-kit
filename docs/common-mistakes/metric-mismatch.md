# Metric Mismatch

Metric mismatch happens when the metric does not match the real decision.

## Examples

- using accuracy on a very imbalanced classification problem;
- optimizing clicks when the business cares about conversion;
- using MAPE when actual values can be zero;
- reporting only global score when segment behavior matters.

## Practical rule

Choose the metric that best represents the cost of being wrong.
