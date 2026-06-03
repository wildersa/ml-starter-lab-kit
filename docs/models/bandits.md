# Multi-Armed Bandits

Bandits are used when a system must choose between options and learn from feedback.

They are useful when you need to balance:

- exploration: test uncertain options;
- exploitation: use options that already work well.

## Basic idea

```text
context -> choose arm -> observe reward -> update policy
```

## Examples

- choose which offer to show;
- choose which banner to display;
- choose email subject variations;
- route traffic between alternatives;
- test recommendations with controlled exploration.

## Common algorithms

| Algorithm | Use when |
|---|---|
| Epsilon-greedy | you want a very simple baseline |
| Thompson Sampling | you want probabilistic exploration |
| UCB | you want exploration based on uncertainty |
| LinUCB | you want to use context features |

## Useful metrics

See [bandit metrics](../metrics/bandits.md).

Common metrics:

- reward;
- cumulative reward;
- regret;
- exploration rate;
- conversion rate;
- exposure fairness.

## Difference from A/B testing

A/B testing usually waits until the end of the experiment to choose a winner.

Bandits update decisions during the experiment.

## Practical warning

Do not optimize only clicks if the business goal is conversion, safety, suitability, or user trust.
