---
id: rl-foundations-03-td-and-control
title: Temporal Difference Learning, Q-Learning, and SARSA
track: reinforcement-learning
node_id: rl-temporal-difference-and-control
prerequisites: [rl-policies-and-value-functions]
unlocks: [rl-worked-examples-and-checkpoints, deep-q-networks]
sources_ref: sources-and-licenses.md
---

# Temporal Difference Learning, Q-Learning, and SARSA

## 1. Intuition

In dynamic survival environments, an autonomous agent rarely knows the complete world transition probabilities $\mathcal{P}(s' \mid s, a)$ or reward function $\mathcal{R}(s,a)$. A survival agent cannot pause time to run dynamic programming calculations over all possible outcomes—it must **learn online directly from experience**.

How do humans and biological agents learn from experience?
When you take an action, you form an immediate expectation of the outcome. If the next step is better or worse than expected, you experience a **surprise** (prediction error). You immediately adjust your value estimate for the previous state *before waiting for the end of the episode*.

This concept is **Temporal Difference (TD) Learning**. TD methods combine the best ideas of Monte Carlo (learning from raw sample experience without a world model) and Dynamic Programming (bootstrapping: updating estimates based on other learned estimates).

```text
Monte Carlo:     Wait until end of episode T  ───> Update V(S_t) using actual G_t
TD(0) Learning:  Take 1 step, observe R_{t+1}, S_{t+1} ───> Update V(S_t) using R_{t+1} + \gamma V(S_{t+1})
```

---

## 2. Theory & Algorithms

### TD Prediction: $TD(0)$

To estimate $V(S_t)$ from sample transitions $(S_t, A_t, R_{t+1}, S_{t+1})$:

$$V(S_t) \leftarrow V(S_t) + \alpha \delta_t$$

Where:
- $\alpha \in (0, 1]$ is the **learning rate**.
- $\delta_t$ is the **TD Error**:
  $$\delta_t = \underbrace{R_{t+1} + \gamma V(S_{t+1})}_{\text{TD Target}} - \underbrace{V(S_t)}_{\text{Current Estimate}}$$

The **TD Target** ($R_{t+1} + \gamma V(S_{t+1})$) serves as an estimate of the true return $G_t$.

### Exploration vs. Exploitation & $\epsilon$-Greedy Policy

An autonomous agent must balance:
- **Exploitation**: Selecting the action that currently has the highest estimated value ($\arg\max_a Q(s,a)$).
- **Exploration**: Trying alternative actions to discover higher rewards or avoid hidden traps.

An **$\epsilon$-Greedy Policy** selects:
$$\pi(a \mid s) = \begin{cases}
1 - \epsilon + \frac{\epsilon}{|\mathcal{A}|} & \text{if } a = \arg\max_{a'} Q(s, a') \quad \text{(Greedy Action)} \\
\frac{\epsilon}{|\mathcal{A}|} & \text{if } a \neq \arg\max_{a'} Q(s, a') \quad \text{(Random Action)}
\end{cases}$$

In practice, $\epsilon$ starts high (e.g., $\epsilon = 1.0$) to explore the environment, and decays over time (e.g., $\epsilon \leftarrow \max(0.01, \epsilon \times 0.995)$) as estimates stabilize.

---

### Q-Learning: Off-Policy TD Control

Q-Learning (Watkins, 1989) directly approximates the optimal action-value function $Q^*$ regardless of the policy being followed during exploration (**Off-Policy**).

**Q-Learning Update Rule**:
$$Q(S_t, A_t) \leftarrow Q(S_t, A_t) + \alpha \left[ \underbrace{R_{t+1} + \gamma \max_{a'} Q(S_{t+1}, a')}_{\text{Q-Learning Target}} - Q(S_t, A_t) \right]$$

Key Feature: The target uses $\max_{a'} Q(S_{t+1}, a')$, assuming optimal action choice in step $t+1$, even if the agent actually takes an exploratory random action $A_{t+1}$ in step $t+1$.

---

### SARSA: On-Policy TD Control

SARSA (Rummery & Niranjan, 1994) updates action values based on the action $A_{t+1}$ actually executed by the current exploratory policy (**On-Policy**). Name comes from the tuple: $(S_t, A_t, R_{t+1}, S_{t+1}, A_{t+1})$.

**SARSA Update Rule**:
$$Q(S_t, A_t) \leftarrow Q(S_t, A_t) + \alpha \left[ \underbrace{R_{t+1} + \gamma Q(S_{t+1}, A_{t+1})}_{\text{SARSA Target}} - Q(S_t, A_t) \right]$$

---

### Detailed Comparison: Q-Learning vs. SARSA in Autonomous Survival

Consider an agent navigating a cliff path to reach food:

```text
[Start] ─── [Safe Path (Long)] ────────────────────────┐
   │                                                   │
[Cliff Path (Short)] ─── [Dangerous Cliff (-100)] ───> [Food Source (+50)]
```

- **Q-Learning (Off-Policy)** learns the *optimal* short path right along the cliff edge because it assumes future greedy choices ($\max_{a'} Q$). However, during training with $\epsilon > 0$, random exploration causes the agent to occasionally step off the cliff!
- **SARSA (On-Policy)** accounts for its own exploratory mistakes. It learns that walking near the cliff edge is dangerous under an exploratory policy, so it chooses the safer long path during training.

| Feature | Q-Learning | SARSA |
| :--- | :--- | :--- |
| **Policy Type** | Off-Policy (learns $Q^*$ while executing $\epsilon$-greedy) | On-Policy (learns $Q^\pi$ for the active $\epsilon$-greedy policy) |
| **Target Equation** | $R_{t+1} + \gamma \max_{a'} Q(S_{t+1}, a')$ | $R_{t+1} + \gamma Q(S_{t+1}, A_{t+1})$ |
| **Risk Preference** | Aggressive / Optimal path (ignores exploration risks in target) | Conservative / Safe path (factors exploration risks into value) |
| **Convergence** | Converges to $Q^*$ directly | Converges to $Q^\pi$; converges to $Q^*$ as $\epsilon \to 0$ |

---

## 3. Worked Example: One Q-Learning Update

An agent is in $S_1 = \text{Foraging Ground}$ and takes action $A_1 = \text{DIG}$.

**Initial Q-Table**:
- $Q(S_1, \text{DIG}) = 5.0$
- $Q(S_2, \text{EAT}) = 12.0$
- $Q(S_2, \text{REST}) = 4.0$

**Step Event**:
- Receives reward $R_2 = +2.0$.
- Environment transitions to $S_2 = \text{Food Discovered}$.
- Learning parameters: $\alpha = 0.2$, $\gamma = 0.9$.

**Execution**:
1. Find max Q-value in successor state $S_2$:
   $$\max_{a'} Q(S_2, a') = \max(12.0, 4.0) = 12.0$$

2. Calculate Q-Learning Target:
   $$\text{Target} = R_2 + \gamma \max_{a'} Q(S_2, a') = 2.0 + (0.9 \times 12.0) = 2.0 + 10.8 = 12.8$$

3. Compute TD Error $\delta_1$:
   $$\delta_1 = \text{Target} - Q(S_1, \text{DIG}) = 12.8 - 5.0 = 7.8$$

4. Apply Q-Update:
   $$Q(S_1, \text{DIG}) \leftarrow Q(S_1, \text{DIG}) + \alpha \delta_1$$
   $$Q(S_1, \text{DIG}) \leftarrow 5.0 + (0.2 \times 7.8) = 5.0 + 1.56 = 6.56$$

New $Q(S_1, \text{DIG}) = 6.56$.

---

## 4. Manual / Guided Exercise

Using the same transition $(S_1, \text{DIG}) \xrightarrow{R=2.0} S_2$, suppose the agent's $\epsilon$-greedy policy selected $A_2 = \text{REST}$ for the next step in $S_2$ (a random exploration step).

Calculate the **SARSA update** for $Q(S_1, \text{DIG})$ given initial $Q(S_1, \text{DIG}) = 5.0$, $Q(S_2, \text{REST}) = 4.0$, $\alpha = 0.2$, $\gamma = 0.9$:

1. Calculate SARSA Target:
   $$\text{Target}_{\text{SARSA}} = R_2 + \gamma Q(S_2, \text{REST}) = 2.0 + 0.9 \times (\text{\_\_\_\_}) = \text{\_\_\_\_}$$

2. Compute TD Error $\delta_{\text{SARSA}}$:
   $$\delta_{\text{SARSA}} = \text{Target}_{\text{SARSA}} - 5.0 = \text{\_\_\_\_}$$

3. Calculate new $Q(S_1, \text{DIG})$:
   $$Q(S_1, \text{DIG}) \leftarrow 5.0 + 0.2 \times (\text{\_\_\_\_}) = \text{\_\_\_\_}$$

*Self-Check Solution*:
- $\text{Target}_{\text{SARSA}} = 2.0 + 0.9(4.0) = 2.0 + 3.6 = 5.6$
- $\delta_{\text{SARSA}} = 5.6 - 5.0 = 0.6$
- $Q(S_1, \text{DIG}) \leftarrow 5.0 + 0.2(0.6) = 5.0 + 0.12 = 5.12$

Notice: SARSA increased $Q(S_1, \text{DIG})$ to only $5.12$ (reflecting the exploratory action taken), whereas Q-Learning updated it to $6.56$ (reflecting optimal potential).

---

## 5. Prediction Challenge

**Question**: If learning rate $\alpha = 1.0$ and $\gamma = 0.0$:
What does the Q-Learning update rule reduce to?

- **Option A**: $Q(S_t, A_t) \leftarrow R_{t+1}$
- **Option B**: $Q(S_t, A_t) \leftarrow Q(S_t, A_t)$
- **Option C**: $Q(S_t, A_t) \leftarrow \max_{a'} Q(S_{t+1}, a')$

*Answer & Explanation*: **Option A**. When $\alpha = 1.0$ and $\gamma = 0.0$, the update becomes $Q(S_t, A_t) \leftarrow Q(S_t, A_t) + 1.0 \times [R_{t+1} + 0 - Q(S_t, A_t)] = R_{t+1}$. The Q-table immediately overwrites its value with the latest instantaneous reward.

---

## 6. Guided Experiment Idea

In a 2D Survival Gridworld with a hazardous river zone:
1. Train a **Q-Learning agent** with $\epsilon = 0.2$. Plot the trajectory during training. Observe how it walks right along the river bank.
2. Train a **SARSA agent** with $\epsilon = 0.2$. Plot the trajectory during training. Observe how it walks 2 cells away from the river bank.
3. Reduce $\epsilon \to 0$ after 1000 episodes and observe both agents' final paths.

---

## 7. Bridge to Deep Q-Networks (DQN)

In tabular Q-Learning, we store a lookup table of shape $(|\mathcal{S}|, |\mathcal{A}|)$.
In complex continuous or high-dimensional autonomous environments (e.g., visual camera inputs, complex health/stamina vectors), state space $|\mathcal{S}|$ is effectively infinite!

**The Deep RL Solution**:
Replace the Q-table with a **Neural Network Function Approximator** $Q(s, a; \theta)$ parameterized by weights $\theta$.

Instead of tabular updates, we optimize the neural network by minimizing the Mean Squared Bellman Error (MSBE) Loss:

$$L(\theta) = \mathbb{E}_{(s, a, r, s') \sim \mathcal{D}} \left[ \left( \underbrace{r + \gamma \max_{a'} Q(s', a'; \theta^-)}_{\text{DQN Target}} - Q(s, a; \theta) \right)^2 \right]$$

Where:
- $\mathcal{D}$ is an **Experience Replay Buffer** storing past transitions $(s, a, r, s')$.
- $\theta^-$ represents parameters of a stable **Target Network**.

Every tabular concept learned in this module (TD target, TD error, $\epsilon$-greedy, off-policy Q-updates) forms the exact core of DQN!

---

## 8. Common Misconceptions

- `MISC_Q_MAX_VS_POLICY`: Thinking Q-Learning requires the agent to actually execute action $\arg\max_{a'} Q(S_{t+1}, a')$ in step $t+1$.
  - *Correction*: Q-Learning uses $\max_{a'} Q$ *only* to construct the target calculation. The actual executed action $A_{t+1}$ can be chosen by $\epsilon$-greedy exploration.
- `MISC_SARSA_ON_POLICY`: Believing SARSA is off-policy.
  - *Correction*: SARSA evaluates the policy currently being executed, including exploratory actions. It is an on-policy method.
- `MISC_TD_VS_MC`: Thinking TD learning requires waiting until the episode terminates.
  - *Correction*: TD updates state values step-by-step ($1$-step lookahead) via bootstrapping, making it suitable for long or non-terminating survival tasks.

---

## 9. Review Variant

**Retrieval Challenge**:
Explain why Q-Learning can re-use old historical transitions logged 10,000 steps ago from an experience replay buffer, whereas standard SARSA cannot.

*Key Answer*: Q-Learning is **off-policy**: its target $r + \gamma \max_{a'} Q(s', a')$ depends only on state transitions and rewards, not on which policy generated the historical action $a'$. SARSA's target requires $Q(s', a')$, where $a'$ was chosen by the specific policy active at that past step, making uncorrected historical buffer replay invalid.
