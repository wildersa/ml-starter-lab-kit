# Bandit Metrics

Use these metrics when a policy chooses actions and receives rewards.

## Reward

Immediate feedback from an action.

Example: click, conversion, revenue, score.

## Cumulative reward

Total reward accumulated over time.

Useful to compare policies.

## Regret

How much reward was lost compared to a better possible choice.

Lower regret is better.

## Exploration rate

How often the policy tests uncertain options.

Too low may stop learning. Too high may waste traffic.

## Exposure fairness

Checks if eligible segments receive reasonable exposure.

Important when actions affect users differently.
