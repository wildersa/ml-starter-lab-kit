---
id: rl-foundations-01-mdp
title: Agent, Environment, and Markov Decision Processes
track: reinforcement-learning
node_id: rl-agent-env-mdp
prerequisites: [probability-basics, sequential-decision-concepts]
unlocks: [rl-policies-and-value-functions]
sources_ref: sources-and-licenses.md
---

# Agent, Environment, and Markov Decision Processes

## 1. Intuition

Imagine an autonomous survival agent foraging in a harsh environment. At every discrete time step, the agent must make decisions:
- Should it expend energy to hunt for food?
- Should it hide from a lurking threat?
- Should it consume immediate low-value berries or travel to a high-yield food source?

In supervised learning, a fixed model receives an input $x$ and predicts a label $y$ with immediate feedback. In contrast, an autonomous RL agent lives in a **loop of interaction**. The consequences of an agent's actions may not be felt immediately: eating contaminated food might yield momentary relief (positive reward) but lead to severe illness 5 time steps later (delayed negative reward).

Reinforcement Learning provides the mathematical framework for learning optimal behavior through sequential trial-and-error interaction with an uncertain environment.

```text
               ┌────────────────────────┐
               │                        │
               │      Environment       │
               │                        │
               └───┬────────────────┬───┘
                   │                │
      Reward R_{t} │                │ Observation O_{t} / State S_{t}
                   │                │
                   ▼                ▼
               ┌────────────────────────┐
               │                        │
               │         Agent          │
               │                        │
               └───────────┬────────────┘
                           │
                  Action A_{t}
                           │
                           ▼
```

---

## 2. Theory & Vocabulary

### Core Vocabulary

1. **Agent**: The autonomous decision-maker (e.g., foraging agent, robot, game character).
2. **Environment**: Everything outside the agent with which it interacts (world dynamics, weather, predators, terrain).
3. **Action ($A_t \in \mathcal{A}$)**: A decision chosen by the agent at time step $t$ (e.g., `FORAGE`, `HIDE`, `REST`).
4. **Reward ($R_{t+1} \in \mathbb{R}$)**: A scalar feedback signal returned by the environment after action $A_t$, measuring immediate success.
5. **Episode**: A complete sequence of interactions from start state to terminal state (e.g., a single survival day ending in death or safety).
6. **Trajectory ($\tau$)**: The sequence of states, actions, and rewards over an episode:
   $$\tau = (S_0, A_0, R_1, S_1, A_1, R_2, \dots, S_T)$$

### State vs. Observation

- **State ($S_t \in \mathcal{S}$)**: The complete, true physical condition of the world at step $t$.
- **Observation ($O_t \in \Omega$)**: The partial or noisy sensor data accessible to the agent.
  - **Fully Observable (MDP)**: $O_t = S_t$. The agent sees everything (e.g., exact health, exact predator coordinates).
  - **Partially Observable (POMDP)**: $O_t \neq S_t$. The agent sees only its local field of view; a threat may lurk outside vision.

### Reward vs. Return

- **Immediate Reward ($R_{t+1}$)**: The short-term feedback received at step $t+1$.
- **Cumulative Return ($G_t$)**: The total sum of rewards received from time step $t$ into the future:
  $$G_t = R_{t+1} + R_{t+2} + R_{t+3} + \dots + R_T = \sum_{k=0}^{T-t-1} R_{t+k+1}$$

### Discount Factor ($\gamma \in [0, 1)$)

To handle infinite-horizon episodes and represent the principle that immediate rewards are often preferable/more reliable than far-future rewards, we introduce the **discount factor** $\gamma$:

$$G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \dots = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}$$

Recursive relationship for Return:
$$G_t = R_{t+1} + \gamma G_{t+1}$$

Why discount future rewards?
1. **Mathematical Convergence**: Ensures $G_t$ remains finite even in infinite non-terminating episodes ($\sum_{k=0}^\infty \gamma^k = \frac{1}{1-\gamma}$).
2. **Uncertainty & Survival**: A survival agent in danger may not live to collect rewards 100 steps in the future ($\gamma$ models effective survival probability per step).

### The Markov Property

A state $S_t$ satisfies the **Markov Property** if the future transition depends *only* on the current state $S_t$ and action $A_t$, independent of past history $(S_0, A_0, \dots, S_{t-1}, A_{t-1})$:

$$\mathbb{P}(S_{t+1} = s', R_{t+1} = r \mid S_t = s, A_t = a, S_{t-1} = s_{t-1}, \dots) = \mathbb{P}(S_{t+1} = s', R_{t+1} = r \mid S_t = s, A_t = a)$$

*"The present state contains all necessary information to predict the future."*

### Markov Decision Process (MDP) Definition

A formal MDP is defined by a 5-tuple $(\mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R}, \gamma)$:
- $\mathcal{S}$: Set of all valid states.
- $\mathcal{A}$: Set of all valid actions.
- $\mathcal{P}(s' \mid s, a) = \mathbb{P}(S_{t+1} = s' \mid S_t = s, A_t = a)$: State transition probability matrix.
- $\mathcal{R}(s, a, s') = \mathbb{E}[R_{t+1} \mid S_t = s, A_t = a, S_{t+1} = s']$: Reward function.
- $\gamma \in [0, 1)$: Discount factor.

---

## 3. Worked Example: Survival Agent Trajectory

Consider a survival agent in a 3-step episode with discount factor $\gamma = 0.8$:

- Step $t=0$: Agent in $S_0$ (`Hungry`). Takes $A_0 = \text{FORAGE}$. Receives reward $R_1 = +2$. Transitions to $S_1$ (`Eating`).
- Step $t=1$: Agent in $S_1$ (`Eating`). Takes $A_1 = \text{REST}$. Receives reward $R_2 = +10$. Transitions to $S_2$ (`Satiated`).
- Step $t=2$: Agent in $S_2$ (`Satiated`). Takes $A_2 = \text{SLEEP}$. Receives reward $R_3 = +5$. Episode terminates.

Let's compute the discounted returns $G_2, G_1, G_0$ working backwards:

1. **At step $t=2$**:
   $$G_2 = R_3 = +5.0$$

2. **At step $t=1$**:
   $$G_1 = R_2 + \gamma G_2 = 10 + 0.8 \times 5.0 = 10 + 4.0 = 14.0$$

3. **At step $t=0$**:
   $$G_0 = R_1 + \gamma G_1 = 2 + 0.8 \times 14.0 = 2 + 11.2 = 13.2$$

Direct formula verification for $G_0$:
$$G_0 = R_1 + \gamma R_2 + \gamma^2 R_3 = 2 + (0.8 \times 10) + (0.8^2 \times 5) = 2 + 8 + (0.64 \times 5) = 2 + 8 + 3.2 = 13.2$$

Both recursive and direct methods yield $G_0 = 13.2$.

---

## 4. Manual / Guided Exercise

A survival agent executes a trajectory with rewards:
- $R_1 = -1$ (energy lost moving)
- $R_2 = -1$ (energy lost searching)
- $R_3 = +20$ (food found)

Given discount factor $\gamma = 0.9$:

1. Calculate $G_2$:
   $$G_2 = R_3 = \text{\_\_\_\_}$$
2. Calculate $G_1$:
   $$G_1 = R_2 + 0.9 \times G_2 = -1 + 0.9 \times (\text{\_\_\_\_}) = \text{\_\_\_\_}$$
3. Calculate $G_0$:
   $$G_0 = R_1 + 0.9 \times G_1 = -1 + 0.9 \times (\text{\_\_\_\_}) = \text{\_\_\_\_}$$

*Self-Check Solution*:
- $G_2 = 20.0$
- $G_1 = -1 + 18.0 = 17.0$
- $G_0 = -1 + 0.9 \times 17.0 = -1 + 15.3 = 14.3$

---

## 5. Prediction Challenge

**Question**: Suppose $\gamma$ is changed from $0.9$ to $0.0$ (myopic agent) for the same reward sequence $(-1, -1, +20)$.
What will $G_0$ become?

- **Option A**: $14.3$
- **Option B**: $-1.0$
- **Option C**: $0.0$
- **Option D**: $+20.0$

*Answer & Explanation*: **Option B** ($-1.0$). When $\gamma = 0$, $G_0 = R_1 = -1$. An agent with $\gamma = 0$ considers *only* immediate reward $R_1$ and completely ignores the $+20$ food reward available two steps ahead. It would avoid foraging because searching costs $-1$ energy!

---

## 6. Guided Experiment Idea

In a gridworld survival sandbox:
1. Set $\gamma = 0.1$: Observe how the agent refuses to navigate around a puddle of mud to reach a shelter 4 steps away.
2. Increase $\gamma = 0.95$: Observe how the agent tolerates 3 steps of small negative movement rewards ($-0.1$) to reach a rich food cache yielding $+10$.
3. Measure the agent's **effective planning horizon**: $H \approx \frac{1}{1-\gamma}$ steps.
   - For $\gamma = 0.5 \implies H \approx 2$ steps.
   - For $\gamma = 0.9 \implies H \approx 10$ steps.
   - For $\gamma = 0.99 \implies H \approx 100$ steps.

---

## 7. Independent Checkpoint

**Task**: An agent receives a reward sequence over 4 steps: $R_1 = 0, R_2 = 0, R_3 = -5, R_4 = +100$.
If $\gamma = 0.5$, calculate $G_0$.

**Step-by-step Solution Requirements**:
1. Compute $G_3 = R_4 = 100$
2. Compute $G_2 = R_3 + \gamma G_3 = -5 + 0.5(100) = 45$
3. Compute $G_1 = R_2 + \gamma G_2 = 0 + 0.5(45) = 22.5$
4. Compute $G_0 = R_1 + \gamma G_1 = 0 + 0.5(22.5) = 11.25$

---

## 8. Common Misconceptions

- `MISC_REWARD_VS_RETURN`: Confusing immediate reward $R_{t+1}$ with total return $G_t$.
  - *Correction*: Reward is the immediate single-step scalar ($R_1 = -1$). Return is the discounted sum of all future rewards ($G_0 = 14.3$).
- `MISC_DISCOUNT_RANGE`: Believing $\gamma$ can be $\ge 1.0$ in infinite-horizon MDPs.
  - *Correction*: If $\gamma \ge 1$, returns in non-terminating tasks sum to infinity, making policy comparison mathematically impossible.
- `MISC_MARKOV_MEMORY`: Assuming the Markov property requires the agent to be unaware of time or history.
  - *Correction*: The Markov property states that the *current state state vector* $S_t$ must be constructed to contain all relevant summary information (e.g., if velocity matters, $S_t$ must include velocity, not just position).

---

## 9. Review Variant

**Retrieval Challenge**:
Why does an autonomous survival agent in a partially observable environment (POMDP) fail if treated as a pure Markov state? How can an autonomous agent construct a valid Markov state from observations $O_0, O_1, \dots, O_t$?

*Key Answer*: If key world variables (like predator location) are unobserved in $O_t$, $P(O_{t+1} \mid O_t)$ is non-Markovian. To restore the Markov property, the agent must build a state representation $S_t$ using frame stacking, recurrent memory (RNN/LSTM), or a belief distribution over hidden variables.
