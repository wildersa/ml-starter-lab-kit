---
id: rl-foundations-02-policies-values
title: Policies, Value Functions, and Bellman Equations
track: reinforcement-learning
node_id: rl-policies-and-value-functions
prerequisites: [rl-agent-env-mdp]
unlocks: [rl-temporal-difference-and-control]
sources_ref: sources-and-licenses.md
---

# Policies, Value Functions, and Bellman Equations

## 1. Intuition

An autonomous survival agent faces a decision in state $S_t$:
- How good is it to be in this state ($S_t = \text{Near Predator}$) versus another state ($S_t = \text{Inside Shelter}$)?
- If the agent takes action $A_t = \text{FORAGE}$ from $S_t = \text{Hungry}$, what is the expected long-term outcome?

To make principled decisions without calculating multi-step trajectories from scratch every time, the agent computes **Value Functions**. Value functions estimate the expected long-term return from a state or state-action pair under a given behavior strategy called a **Policy**.

The core mathematical tool for computing value functions is the **Bellman Equation**, which breaks down the value of a state into two components:
1. The **immediate reward** received right now.
2. The **discounted expected value** of the next state.

```text
               State s
                  │
          ┌───────┴───────┐
          │  Action a     │  (Policy \pi(a|s))
          ▼               ▼
      Action-Value Q(s,a_1)   Action-Value Q(s,a_2)
          │
      ┌───┴───┐ (Transition P(s'|s,a))
      ▼       ▼
   State s'_1  State s'_2
```

---

## 2. Theory & Equations

### Policy ($\pi$)

A **policy** $\pi$ defines the agent's behavior strategy:
- **Stochastic Policy**: $\pi(a \mid s) = \mathbb{P}(A_t = a \mid S_t = s)$ (probability distribution over actions given state).
- **Deterministic Policy**: $a = \pi(s)$ (maps each state directly to a single action).

### State-Value Function ($V^\pi(s)$)

The **state-value function** $V^\pi(s)$ is the expected return starting from state $s$ and following policy $\pi$ thereafter:

$$V^\pi(s) = \mathbb{E}_\pi \left[ G_t \mid S_t = s \right] = \mathbb{E}_\pi \left[ \sum_{k=0}^{\infty} \gamma^k R_{t+k+1} \;\middle|\; S_t = s \right]$$

### Action-Value Function ($Q^\pi(s,a)$)

The **action-value function** $Q^\pi(s,a)$ is the expected return starting from state $s$, taking action $a$, and thereafter following policy $\pi$:

$$Q^\pi(s,a) = \mathbb{E}_\pi \left[ G_t \mid S_t = s, A_t = a \right] = \mathbb{E}_\pi \left[ \sum_{k=0}^{\infty} \gamma^k R_{t+k+1} \;\middle|\; S_t = s, A_t = a \right]$$

### Relationship Between $V^\pi(s)$ and $Q^\pi(s,a)$

1. **Expressing $V^\pi(s)$ in terms of $Q^\pi(s,a)$**:
   $$V^\pi(s) = \sum_{a \in \mathcal{A}} \pi(a \mid s) Q^\pi(s,a)$$
   *(The value of a state is the weighted average of action values under the policy.)*

2. **Expressing $Q^\pi(s,a)$ in terms of $V^\pi(s')$**:
   $$Q^\pi(s,a) = \sum_{s' \in \mathcal{S}} \mathcal{P}(s' \mid s, a) \left[ \mathcal{R}(s,a,s') + \gamma V^\pi(s') \right]$$

### Bellman Expectation Equation for $V^\pi(s)$

Combining the two relationships yields the recursive **Bellman Expectation Equation** for $V^\pi(s)$:

$$V^\pi(s) = \sum_{a \in \mathcal{A}} \pi(a \mid s) \sum_{s' \in \mathcal{S}} \mathcal{P}(s' \mid s, a) \left[ \mathcal{R}(s,a,s') + \gamma V^\pi(s') \right]$$

### Optimal Value Functions & Bellman Optimality Equations

An optimal policy $\pi^*$ achieves the maximum expected return across all states.
- **Optimal State-Value Function**: $V^*(s) = \max_\pi V^\pi(s)$
- **Optimal Action-Value Function**: $Q^*(s,a) = \max_\pi Q^\pi(s,a)$

**Bellman Optimality Equations**:

$$V^*(s) = \max_{a \in \mathcal{A}} Q^*(s,a) = \max_{a \in \mathcal{A}} \sum_{s' \in \mathcal{S}} \mathcal{P}(s' \mid s, a) \left[ \mathcal{R}(s,a,s') + \gamma V^*(s') \right]$$

$$Q^*(s,a) = \sum_{s' \in \mathcal{S}} \mathcal{P}(s' \mid s, a) \left[ \mathcal{R}(s,a,s') + \gamma \max_{a' \in \mathcal{A}} Q^*(s', a') \right]$$

Notice the critical difference: **Bellman Expectation** averages over actions ($\sum_{a} \pi(a|s)$), while **Bellman Optimality** takes the maximum over actions ($\max_{a}$).

---

## 3. Worked Example: One Bellman Backup Calculation

Consider a survival agent evaluating state $S_1 = \text{Clear Area}$.

**Problem Setup**:
- Action Space: $\mathcal{A} = \{\text{SEARCH}, \text{REST}\}$
- Policy: $\pi(\text{SEARCH} \mid S_1) = 0.7$, $\pi(\text{REST} \mid S_1) = 0.3$
- Discount Factor: $\gamma = 0.9$

**Environment Dynamics**:
1. Action $a = \text{SEARCH}$:
   - $80\%$ chance to reach $S_{\text{Food}}$ ($R = +10$). Known $V(S_{\text{Food}}) = 20.0$.
   - $20\%$ chance to stay in $S_1$ ($R = -2$). Known $V(S_1) = 5.0$.
2. Action $a = \text{REST}$:
   - $100\%$ chance to remain in $S_1$ ($R = +1$). Known $V(S_1) = 5.0$.

Let's compute $Q^\pi(S_1, \text{SEARCH})$, $Q^\pi(S_1, \text{REST})$, and perform one Bellman backup for $V^\pi(S_1)$:

1. **Calculate $Q^\pi(S_1, \text{SEARCH})$**:
   $$Q(S_1, \text{SEARCH}) = 0.8 \times [10 + 0.9(20.0)] + 0.2 \times [-2 + 0.9(5.0)]$$
   $$= 0.8 \times [10 + 18.0] + 0.2 \times [-2 + 4.5]$$
   $$= 0.8 \times [28.0] + 0.2 \times [2.5] = 22.4 + 0.5 = 22.9$$

2. **Calculate $Q^\pi(S_1, \text{REST})$**:
   $$Q(S_1, \text{REST}) = 1.0 \times [1 + 0.9(5.0)] = 1.0 \times [1 + 4.5] = 5.5$$

3. **Bellman Expectation Backup for $V^\pi(S_1)$**:
   $$V^\pi(S_1) = \pi(\text{SEARCH} \mid S_1) Q^\pi(S_1, \text{SEARCH}) + \pi(\text{REST} \mid S_1) Q^\pi(S_1, \text{REST})$$
   $$V^\pi(S_1) = (0.7 \times 22.9) + (0.3 \times 5.5) = 16.03 + 1.65 = 17.68$$

4. **Bellman Optimality Backup $V^*(S_1)$**:
   $$V^*(S_1) = \max_a Q(S_1, a) = \max(22.9, 5.5) = 22.9$$

---

## 4. Manual / Guided Exercise

A survival agent is at state $S = \text{Cave Entrance}$ with $\gamma = 0.8$.
Available actions: $A = \{\text{EXPLORE}, \text{STAY}\}$.

1. Action $\text{EXPLORE}$:
   - Transitions to $S' = \text{Deep Cave}$ with probability $1.0$.
   - Immediate reward $R = -1$.
   - Known value $V(S') = 50.0$.

   Calculate $Q(S, \text{EXPLORE})$:
   $$Q(S, \text{EXPLORE}) = 1.0 \times [-1 + 0.8 \times (\text{\_\_\_\_})] = \text{\_\_\_\_}$$

2. Action $\text{STAY}$:
   - Transitions to $S' = \text{Cave Entrance}$ with probability $1.0$.
   - Immediate reward $R = 0$.
   - Known value $V(S) = 10.0$.

   Calculate $Q(S, \text{STAY})$:
   $$Q(S, \text{STAY}) = 1.0 \times [0 + 0.8 \times (\text{\_\_\_\_})] = \text{\_\_\_\_}$$

3. Compute the optimal value $V^*(S)$:
   $$V^*(S) = \max(Q(S, \text{EXPLORE}), Q(S, \text{STAY})) = \text{\_\_\_\_}$$

*Self-Check Solution*:
- $Q(S, \text{EXPLORE}) = -1 + 0.8(50.0) = -1 + 40.0 = 39.0$
- $Q(S, \text{STAY}) = 0 + 0.8(10.0) = 8.0$
- $V^*(S) = \max(39.0, 8.0) = 39.0$

---

## 5. Prediction Challenge

**Scenario**: An agent is evaluating a state $S$ where taking action $A_1$ yields $R = +100$ immediately, but leads to a death state $S_{\text{dead}}$ where $V(S_{\text{dead}}) = 0$.
Taking action $A_2$ yields $R = 0$ immediately, but leads to a thriving colony $S_{\text{safe}}$ where $V(S_{\text{safe}}) = 200$.

Given $\gamma = 0.9$:
Which action will the optimal policy $\pi^*$ choose?

- **Option A**: $A_1$ because immediate reward is higher ($+100 > 0$).
- **Option B**: $A_2$ because $Q^*(S, A_2) = 180 > Q^*(S, A_1) = 100$.
- **Option C**: Both actions are equally valued.

*Answer & Explanation*: **Option B**. $Q^*(S, A_1) = 100 + 0.9(0) = 100$. $Q^*(S, A_2) = 0 + 0.9(200) = 180$. An optimal value-based agent evaluates total future expected return, properly selecting long-term survival over immediate greedy reward.

---

## 6. Guided Experiment Idea

Using dynamic programming / value iteration on a 4x4 Gridworld environment:
1. Run Value Iteration with $\gamma = 0.9$ until convergence ($|V_{k+1}(s) - V_k(s)| < 10^{-4}$).
2. Track the number of Bellman updates required for convergence.
3. Lower $\gamma$ to $0.1$ and rerun. Observe how value iteration converges much faster (fewer backups required), but the optimal policy becomes short-sighted.

---

## 7. Independent Checkpoint

Given state $S_0$, discount factor $\gamma = 0.5$, and deterministic transition dynamics:
- $Q(S_0, a_1) = 10$
- $Q(S_0, a_2) = 25$
- $Q(S_0, a_3) = 18$

1. If policy $\pi$ selects actions uniformly at random ($\pi(a_i \mid S_0) = \frac{1}{3}$ for $i \in \{1,2,3\}$), compute $V^\pi(S_0)$.
2. Compute $V^*(S_0)$ under the optimal greedy policy.

**Step-by-step Solution**:
1. $V^\pi(S_0) = \frac{1}{3}(10) + \frac{1}{3}(25) + \frac{1}{3}(18) = \frac{53}{3} \approx 17.67$
2. $V^*(S_0) = \max(10, 25, 18) = 25.0$

---

## 8. Common Misconceptions

- `MISC_V_VS_Q`: Confusing $V(s)$ with $Q(s,a)$.
  - *Correction*: $V(s)$ is the value of being in state $s$. $Q(s,a)$ is the value of taking action $a$ specifically while in state $s$.
- `MISC_BELLMAN_MAX_VS_AVG`: Using $\max_a$ when computing $V^\pi(s)$ under a non-greedy policy.
  - *Correction*: For a fixed policy $\pi$, $V^\pi(s)$ is the *weighted expectation* over policy probabilities $\sum_a \pi(a|s) Q^\pi(s,a)$. $\max_a$ is used *only* for optimal value functions $V^*(s)$ and $Q^*(s,a)$.

---

## 9. Review Variant

**Retrieval Challenge**:
How does the Bellman Optimality Equation for $Q^*(s,a)$ lay the exact foundation for the tabular Q-Learning algorithm?

*Key Answer*: The Bellman Optimality equation $Q^*(s,a) = \mathbb{E}[R + \gamma \max_{a'} Q^*(s', a')]$ defines the target value. Q-Learning uses sample transitions $(s, a, r, s')$ to incrementally update $Q(s,a)$ toward this exact target without needing an environment model $\mathcal{P}(s'|s,a)$.
