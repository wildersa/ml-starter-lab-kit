---
id: rl-foundations-04-worked-examples
title: Worked Calculations and Independent Checkpoints
track: reinforcement-learning
node_id: rl-worked-examples-and-checkpoints
prerequisites: [rl-temporal-difference-and-control]
unlocks: [value-based-rl-mastery]
sources_ref: sources-and-licenses.md
---

# Worked Calculations and Independent Checkpoints

## Overview

This specification provides hands-on worked calculations, guided practice sets, and independent checkpoints to satisfy the portal quality criteria. The learner must complete and verify four core mathematical operations:

1. **Discounted Return Calculation ($G_0$)**
2. **One Bellman Backup Calculation ($V(s)$ or $Q(s,a)$)**
3. **One TD Update Calculation ($V(s)$)**
4. **One Q-Learning Update Calculation ($Q(s,a)$)**

---

## 1. Discounted Return Calculation ($G_0$)

### Problem Statement
An autonomous foraging agent completes a 5-step episode. At each time step $t \in \{0, 1, 2, 3, 4\}$, the environment provides rewards:
- $R_1 = -2.0$ (energy spent moving across rough terrain)
- $R_2 = -1.0$ (searching bush)
- $R_3 = +10.0$ (finding berries)
- $R_4 = +5.0$ (eating remaining berries)
- $R_5 = +20.0$ (reaching shelter safely)

The discount factor is set to $\gamma = 0.8$. Compute the discounted returns $G_4, G_3, G_2, G_1, G_0$.

### Worked Step-by-Step Solution

#### Backward Iteration ($G_t = R_{t+1} + \gamma G_{t+1}$):

1. **Step $t=4$**:
   $$G_4 = R_5 = 20.0$$

2. **Step $t=3$**:
   $$G_3 = R_4 + \gamma G_4 = 5.0 + (0.8 \times 20.0) = 5.0 + 16.0 = 21.0$$

3. **Step $t=2$**:
   $$G_2 = R_3 + \gamma G_3 = 10.0 + (0.8 \times 21.0) = 10.0 + 16.8 = 26.8$$

4. **Step $t=1$**:
   $$G_1 = R_2 + \gamma G_2 = -1.0 + (0.8 \times 26.8) = -1.0 + 21.44 = 20.44$$

5. **Step $t=0$**:
   $$G_0 = R_1 + \gamma G_1 = -2.0 + (0.8 \times 20.44) = -2.0 + 16.352 = 14.352$$

#### Direct Sum Verification:
$$G_0 = R_1 + \gamma R_2 + \gamma^2 R_3 + \gamma^3 R_4 + \gamma^4 R_5$$
$$G_0 = -2.0 + (0.8 \times -1.0) + (0.64 \times 10.0) + (0.512 \times 5.0) + (0.4096 \times 20.0)$$
$$G_0 = -2.0 - 0.8 + 6.4 + 2.56 + 8.192 = 14.352$$

---

### Checkpoint Exercise 1.1 (Independent)
A survival agent receives rewards $R_1 = -5, R_2 = 0, R_3 = +15, R_4 = +50$ with discount factor $\gamma = 0.5$.
Compute $G_0$.

**Expected Answer**:
- $G_3 = 50.0$
- $G_2 = 15 + 0.5(50) = 40.0$
- $G_1 = 0 + 0.5(40) = 20.0$
- $G_0 = -5 + 0.5(20) = 5.0$

---

## 2. One Bellman Backup Calculation

### Problem Statement
An autonomous agent is in state $S_0 = \text{Cave Entrance}$.
- Discount factor: $\gamma = 0.9$.
- Available actions: $\mathcal{A} = \{a_1 = \text{REST}, a_2 = \text{VENTURE}\}$.
- Stochastic policy: $\pi(a_1 \mid S_0) = 0.4$, $\pi(a_2 \mid S_0) = 0.6$.

**Transition Dynamics**:
1. Action $a_1 = \text{REST}$:
   - $100\%$ probability of remaining in $S_0$. Reward $R = +1.0$.
   - Current value estimate: $V(S_0) = 10.0$.
2. Action $a_2 = \text{VENTURE}$:
   - $70\%$ probability of reaching $S_1 = \text{Food Water}$ with reward $R = +15.0$. Known $V(S_1) = 30.0$.
   - $30\%$ probability of reaching $S_2 = \text{Trapped Zone}$ with reward $R = -10.0$. Known $V(S_2) = 2.0$.

Calculate:
1. $Q^\pi(S_0, a_1)$
2. $Q^\pi(S_0, a_2)$
3. Bellman Expectation Backup $V^\pi(S_0)$
4. Bellman Optimality Backup $V^*(S_0)$

### Worked Step-by-Step Solution

1. **Calculate $Q^\pi(S_0, a_1)$**:
   $$Q^\pi(S_0, a_1) = 1.0 \times [R + \gamma V(S_0)] = 1.0 \times [1.0 + 0.9 \times 10.0] = 1.0 + 9.0 = 10.0$$

2. **Calculate $Q^\pi(S_0, a_2)$**:
   $$Q^\pi(S_0, a_2) = \mathcal{P}(S_1 \mid S_0, a_2)[R_{S1} + \gamma V(S_1)] + \mathcal{P}(S_2 \mid S_0, a_2)[R_{S2} + \gamma V(S_2)]$$
   $$Q^\pi(S_0, a_2) = 0.7 \times [15.0 + 0.9(30.0)] + 0.3 \times [-10.0 + 0.9(2.0)]$$
   $$Q^\pi(S_0, a_2) = 0.7 \times [15.0 + 27.0] + 0.3 \times [-10.0 + 1.8]$$
   $$Q^\pi(S_0, a_2) = 0.7 \times [42.0] + 0.3 \times [-8.2] = 29.4 - 2.46 = 26.94$$

3. **Bellman Expectation Backup $V^\pi(S_0)$**:
   $$V^\pi(S_0) = \pi(a_1 \mid S_0) Q^\pi(S_0, a_1) + \pi(a_2 \mid S_0) Q^\pi(S_0, a_2)$$
   $$V^\pi(S_0) = (0.4 \times 10.0) + (0.6 \times 26.94) = 4.0 + 16.164 = 20.164$$

4. **Bellman Optimality Backup $V^*(S_0)$**:
   $$V^*(S_0) = \max_a Q^*(S_0, a) = \max(10.0, 26.94) = 26.94$$

---

### Checkpoint Exercise 2.1 (Independent)
State $S = \text{Bush}$. $\gamma = 0.5$. Actions: $a_1, a_2$.
- $Q(S, a_1) = 8.0$
- $a_2$ transitions with $50\%$ probability to $S'$ ($R = 4, V(S') = 20$) and $50\%$ probability to $S''$ ($R = -2, V(S'') = 0$).
Compute $Q(S, a_2)$ and $V^*(S)$.

**Expected Answer**:
- $Q(S, a_2) = 0.5[4 + 0.5(20)] + 0.5[-2 + 0.5(0)] = 0.5[14] + 0.5[-2] = 7.0 - 1.0 = 6.0$
- $V^*(S) = \max(8.0, 6.0) = 8.0$

---

## 3. One Temporal Difference (TD) Update Calculation

### Problem Statement
An autonomous agent uses TD(0) value prediction with parameters $\alpha = 0.1, \gamma = 0.9$.
Current state-value table:
- $V(S_{\text{hill}}) = 12.0$
- $V(S_{\text{river}}) = 25.0$

The agent executes a transition: $(S_{\text{hill}}) \xrightarrow{R = +3.0} (S_{\text{river}})$.

Compute:
1. TD Target
2. TD Error $\delta_t$
3. Updated value $V(S_{\text{hill}})$

### Worked Step-by-Step Solution

1. **Calculate TD Target**:
   $$\text{TD Target} = R_{t+1} + \gamma V(S_{\text{river}}) = 3.0 + 0.9 \times 25.0 = 3.0 + 22.5 = 25.5$$

2. **Compute TD Error $\delta_t$**:
   $$\delta_t = \text{TD Target} - V(S_{\text{hill}}) = 25.5 - 12.0 = +13.5$$

3. **Apply Value Update**:
   $$V(S_{\text{hill}}) \leftarrow V(S_{\text{hill}}) + \alpha \delta_t = 12.0 + 0.1 \times (13.5) = 12.0 + 1.35 = 13.35$$

---

### Checkpoint Exercise 3.1 (Independent)
Given $V(S_1) = 50.0$, $V(S_2) = 20.0$, learning rate $\alpha = 0.2$, discount factor $\gamma = 0.8$.
The agent transitions: $S_1 \xrightarrow{R = -5.0} S_2$.
Compute the new value $V(S_1)$.

**Expected Answer**:
- $\text{TD Target} = -5.0 + 0.8(20.0) = -5.0 + 16.0 = 11.0$
- $\delta_t = 11.0 - 50.0 = -39.0$
- $V(S_1) \leftarrow 50.0 + 0.2(-39.0) = 50.0 - 7.8 = 42.2$

---

## 4. One Q-Learning Update Calculation

### Problem Statement
An autonomous agent uses Q-Learning with $\alpha = 0.25, \gamma = 0.8$.
Current Q-table:
- $Q(S_{\text{hungry}}, \text{FORAGE}) = 4.0$
- $Q(S_{\text{eating}}, \text{CHEW}) = 15.0$
- $Q(S_{\text{eating}}, \text{STORE}) = 8.0$
- $Q(S_{\text{eating}}, \text{LOOK\_AROUND}) = 2.0$

The agent takes action $\text{FORAGE}$ from $S_{\text{hungry}}$, receives reward $R = +6.0$, and transitions to $S_{\text{eating}}$.

Compute:
1. Max successor value $\max_{a'} Q(S_{\text{eating}}, a')$
2. Q-Learning Target
3. TD Error $\delta_t$
4. Updated $Q(S_{\text{hungry}}, \text{FORAGE})$

### Worked Step-by-Step Solution

1. **Find $\max_{a'} Q(S_{\text{eating}}, a')$**:
   $$\max(15.0, 8.0, 2.0) = 15.0$$

2. **Calculate Q-Learning Target**:
   $$\text{Target} = R + \gamma \max_{a'} Q(S_{\text{eating}}, a') = 6.0 + 0.8 \times 15.0 = 6.0 + 12.0 = 18.0$$

3. **Compute TD Error $\delta_t$**:
   $$\delta_t = \text{Target} - Q(S_{\text{hungry}}, \text{FORAGE}) = 18.0 - 4.0 = 14.0$$

4. **Apply Q-Update**:
   $$Q(S_{\text{hungry}}, \text{FORAGE}) \leftarrow Q(S_{\text{hungry}}, \text{FORAGE}) + \alpha \delta_t$$
   $$Q(S_{\text{hungry}}, \text{FORAGE}) \leftarrow 4.0 + 0.25 \times (14.0) = 4.0 + 3.5 = 7.5$$

---

### Checkpoint Exercise 4.1 (Independent)
Initial Q-table:
- $Q(S_A, a_1) = 10.0$
- $Q(S_B, b_1) = 5.0$, $Q(S_B, b_2) = 30.0$
Parameters: $\alpha = 0.5, \gamma = 0.9$.
Transition: $(S_A, a_1) \xrightarrow{R = +2.0} S_B$.
Compute the new $Q(S_A, a_1)$.

**Expected Answer**:
- $\max_{a'} Q(S_B, a') = \max(5.0, 30.0) = 30.0$
- $\text{Target} = 2.0 + 0.9(30.0) = 2.0 + 27.0 = 29.0$
- $\delta_t = 29.0 - 10.0 = 19.0$
- $Q(S_A, a_1) \leftarrow 10.0 + 0.5(19.0) = 10.0 + 9.5 = 19.5$

---

## Python Verification Script

To deterministically verify all calculations programmatically:

```python
def verify_rl_foundations():
    # 1. Discounted Return
    rewards = [-2.0, -1.0, 10.0, 5.0, 20.0]
    gamma = 0.8
    G0 = 0.0
    for r in reversed(rewards):
        G0 = r + gamma * G0
    assert abs(G0 - 14.352) < 1e-5, f"Return verification failed: {G0}"

    # 2. Bellman Backup
    Q_a1 = 1.0 * (1.0 + 0.9 * 10.0)
    Q_a2 = 0.7 * (15.0 + 0.9 * 30.0) + 0.3 * (-10.0 + 0.9 * 2.0)
    V_exp = 0.4 * Q_a1 + 0.6 * Q_a2
    assert abs(Q_a2 - 26.94) < 1e-5, f"Q_a2 failed: {Q_a2}"
    assert abs(V_exp - 20.164) < 1e-5, f"V_exp failed: {V_exp}"

    # 3. TD Update
    V_hill = 12.0
    V_river = 25.0
    alpha = 0.1
    gamma = 0.9
    td_target = 3.0 + gamma * V_river
    V_hill_new = V_hill + alpha * (td_target - V_hill)
    assert abs(V_hill_new - 13.35) < 1e-5, f"TD Update failed: {V_hill_new}"

    # 4. Q-Learning Update
    Q_hungry = 4.0
    Q_eating_max = 15.0
    alpha_q = 0.25
    gamma_q = 0.8
    q_target = 6.0 + gamma_q * Q_eating_max
    Q_hungry_new = Q_hungry + alpha_q * (q_target - Q_hungry)
    assert abs(Q_hungry_new - 7.5) < 1e-5, f"Q-Learning failed: {Q_hungry_new}"

    print("All RL Foundation calculations verified successfully!")

if __name__ == "__main__":
    verify_rl_foundations()
```
