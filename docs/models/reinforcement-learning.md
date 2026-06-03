# Reinforcement Learning

Reinforcement Learning, or RL, is used when an agent learns by interacting with an environment.

The agent takes actions, receives rewards, and tries to improve future decisions.

## Basic idea

```text
state -> action -> reward -> new state
```

## Use RL when

- decisions affect future situations;
- feedback comes as rewards;
- exploration is part of the problem;
- there is a simulator or safe environment.

## Examples

- game playing;
- robot control;
- dynamic pricing simulation;
- resource allocation;
- sequential decision systems.

## Important concepts

| Concept | Meaning |
|---|---|
| Agent | the decision maker |
| Environment | the world where actions happen |
| State | current situation |
| Action | what the agent chooses |
| Reward | feedback signal |
| Policy | rule used to choose actions |

## Practical warning

RL is usually harder than supervised learning.

If the problem can be solved with [supervised learning](supervised.md), a rule, or a [bandit](bandits.md), start there first.
