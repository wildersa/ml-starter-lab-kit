# Multi-Armed Bandit Metrics

Multi-Armed Bandits (MAB) focus on the trade-off between **Exploration** (trying new things) and **Exploitation** (using what you know works).

For a deeper dive into how to measure model performance and how it relates to business value, see the [Evaluation and Monitoring](../concepts/evaluation-and-monitoring.md) guide.

## Reward

- **What it answers:** Did the chosen action result in a success?
- **When to use:** To measure the immediate feedback from a single decision.
- **When to avoid:** When the outcome takes a very long time to manifest (delayed reward).
- **Common trap:** Choosing a reward that is easy to optimize but doesn't drive business value (e.g., clicks vs. actual sales).
- **Example:** A user clicking an ad (binary reward) or the amount of revenue from a purchase (continuous reward).

## Cumulative Reward

- **What it answers:** How much total value has the policy generated over time?
- **When to use:** To compare the long-term performance of different strategies.
- **When to avoid:** When comparing runs of different lengths without normalizing.
- **Common trap:** Comparing cumulative rewards from runs with different total rounds.
- **Example:** Strategy A earned $5,000 over 1,000 rounds, while Strategy B earned $4,500.

## Regret

- **What it answers:** How much reward was "lost" because we chose a sub-optimal action instead of the best possible one?
- **When to use:** To measure the efficiency of the learning process. Lower regret means the policy found the best action faster.
- **When to avoid:** In production environments where you don't know the "true" probabilities of each arm.
- **Common trap:** Regret is usually only calculable in simulations where you already know the "true" best action.
- **Example:** If the best arm gives 10% conversion and we chose an arm that gives 2%, we have 8% regret for that round.

## Lift vs. Baseline

- **What it answers:** How much better is the Bandit policy than a simple static rule (like always showing the most popular item)?
- **When to use:** To justify the complexity of using a Bandit system.
- **When to avoid:** When the baseline is so strong that the bandit overhead isn't worth it.
- **Common trap:** Using a very weak baseline that is easy to beat.
- **Example:** The Bandit increased conversion by 15% compared to the previous static "Featured Product" list.

## Arm Selection Distribution

- **What it answers:** How often is each option (arm) being chosen?
- **When to use:** To ensure the model is actually converging to the best option and not getting "stuck" on a sub-optimal one.
- **When to avoid:** In the very early stages of exploration when distribution is naturally random.
- **Common trap:** Expecting 100% convergence immediately; exploration takes time.
- **Example:** Seeing that the model eventually chooses the "Best Offer" 90% of the time.

## Exploration Cost and User Drift

- **What it answers:** How much are we "paying" (in lost immediate reward) to learn about new options, and is the best option changing over time?
- **When to use:** To balance the risk of showing a bad option to a user against the need to learn.
- **When to avoid:** When the environment is perfectly static and you already know the optimal choice.
- **Common trap:** Not accounting for **User Drift**. What was the best arm last month might not be the best arm today.
- **Example:** Realizing that the "Summer Sale" arm is losing its effectiveness as autumn approaches.
