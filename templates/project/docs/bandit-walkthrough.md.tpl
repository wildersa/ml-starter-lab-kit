# Bandit Walkthrough — From Supervised to Adaptive Decisions

So you have a dataset and you want to use it for a Multi-Armed Bandit experiment. This guide will help you map traditional supervised learning concepts to the world of adaptive decisions.

## 1. The Core Mapping

In Supervised Learning, you usually have a fixed dataset where each row is an independent example. In a Bandit Lab, we treat each decision as an **event** (or impression).

| Supervised Concept | Bandit Concept | Description |
| :--- | :--- | :--- |
| Features | **Context** | Information available *before* making a decision (e.g., user profile, device, time). |
| - | **Arm / Action** | The decision you make (e.g., which ad to show, which price to set). |
| Target (y) | **Reward** | The outcome you want to maximize, observed *after* taking an action. |
| Model | **Policy** | The strategy that chooses the best arm based on current knowledge. |
| Evaluation (Test Set) | **Simulation** | Replaying events to see how a policy would have performed compared to a baseline. |

## 2. The "Supervised Target" Trap ⚠️

**CRITICAL WARNING:** You cannot simply use the `y` (target) from a supervised dataset as your Bandit reward without a clear "Action" mapping.

In Supervised Learning, `y` is usually what happened regardless of your model. In a Bandit experiment, the **Reward** is what happens *because* you chose a specific **Arm**.

To run a valid Bandit Lab, you need:
1. **Impressions/Events**: A stream of opportunities to make a choice.
2. **Actions**: A finite set of options you could have chosen.
3. **Rewards**: A metric (binary or continuous) that measures success for a specific action.

## 3. Key Bandit Concepts in Detail

### Context
This is everything you know about the situation before you choose an arm.
*Example*: User is from "New York", using "Mobile", at "10:00 AM".

### Arm / Action
One of the discrete choices available to the policy.
*Example*: Showing "Discount Voucher A" vs "Discount Voucher B".

### Reward
The feedback from the environment.
*Example*: Did the user click? (1 for Yes, 0 for No).

### Policy
The "brain" that decides which arm to pull. It balances **Exploration** (trying new things) and **Exploitation** (using what works).

### Baseline
A simple policy used for comparison, usually a **Random** policy or a fixed "Always choose Arm 1" policy.

### Regret and Lift
* **Regret**: The difference between the best possible reward and what your policy actually got. We want to minimize this.
* **Lift**: The percentage improvement of your policy over the baseline.

### Delayed Reward
In many real-world scenarios, the reward isn't instant.
*Example*: You show an ad now, but the purchase (reward) happens 3 days later. This delay makes learning harder.

### Drift
Just like in supervised learning, the environment changes. A "Best Arm" today might be the "Worst Arm" next month because of seasonal trends or changing user behavior.

## 4. How to use this in the Bandit Lab

When you run `python -m {{PACKAGE_NAME}}.lab bandit`, the simulator uses your configuration to test different policies against each other. It calculates the **Cumulative Reward** and **Regret** over time, helping you see which policy learns the fastest.
