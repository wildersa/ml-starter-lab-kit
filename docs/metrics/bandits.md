# Bandit Metrics

Multi-Armed Bandits (MAB) evaluate the trade-off between **Exploration** (gathering information) and **Exploitation** (using known information to maximize reward).

## Reward

- **What it answers**: What is the immediate result of an action?
- **When to use it**: To define success (e.g., click, purchase, satisfied user).
- **Example**: A reward of 1 for a click and 0 for no click.

## Cumulative Reward

- **What it answers**: How much total value has the policy generated over time?
- **When to use it**: To compare the overall performance of different strategies.
- **Example**: Strategy A earned 1500 total clicks, while Strategy B earned 1200.

## Regret

- **What it answers**: How much reward did I lose by not picking the best possible arm every time?
- **When to use it**: To understand the cost of learning. Lower regret means the policy found the best option quickly.
- **Common trap**: Zero regret is impossible during learning, but a good policy shows a "plateauing" cumulative regret curve.

## Lift vs. Baseline

- **What it answers**: How much better is the bandit than a random choice or a static business rule?
- **When to use it**: To justify the use of a bandit system over a simpler approach.
- **Example**: The Thompson Sampling policy achieved a 15% lift in conversion compared to the random baseline.

## Arm Distribution

- **What it answers**: Which options (arms) is the model choosing the most?
- **When to use it**: To detect if the model is stuck on one option or if it is exploring fairly.

## Exploration Cost and User Drift

- **Exploration Cost**: The temporary loss in reward incurred while testing uncertain options.
- **User Behavior Drift**: Bandits are sensitive to changes in user preferences over time. If your reward rate suddenly drops, your users might have changed their behavior, requiring the model to "re-learn".

---

### Practical Tip

Always check the [Before Evaluation Checklist](../checklists/before-evaluation.md) and monitor the bandit's performance over time, as its environment is dynamic.
