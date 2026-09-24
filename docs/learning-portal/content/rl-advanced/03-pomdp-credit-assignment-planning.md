# Module 03: Partial Observability, Delayed Credit Assignment, & Planning

## 1. Partial Observability: MDP vs. POMDP

In fully observable Markov Decision Processes (MDPs), the state $S_t$ contains all historical information necessary to predict future states and rewards (the **Markov Property**):

$$P(S_{t+1} \vert S_t, A_t, S_{t-1}, A_{t-1}, \dots) = P(S_{t+1} \vert S_t, A_t)$$

In real-world autonomous systems, agents rarely have access to complete state $S_t$. Cameras have limited field-of-view, sensors produce noisy readings, and external agents hide internal intentions. These environments are **Partially Observable Markov Decision Processes (POMDPs)**.

### Formal POMDP Definition

A POMDP is defined by the 7-tuple $(\mathcal{S}, \mathcal{A}, T, R, \Omega, O, \gamma)$:
- $\mathcal{S}$: True underlying environment state space (unobserved).
- $\mathcal{A}$: Discrete or continuous action space.
- $T(s' \vert s, a) = P(S_{t+1}=s' \vert S_t=s, A_t=a)$: State transition probability.
- $R(s, a)$: Reward function.
- $\Omega$: Observation space containing raw sensor signals $o \in \Omega$.
- $O(o \vert s', a) = P(O_{t+1}=o \vert S_{t+1}=s', A_t=a)$: Observation probability distribution emitted by state $s'$.
- $\gamma \in [0, 1)$: Discount factor.

```text
Full MDP:
[ True State s_t ] ──────────────────────────────────────────► Agent Decision

POMDP:
[ True State s_t ] ──► Emission O(o|s,a) ──► [ Observation o_t ] ──► [ Belief Update b_t ] ──► Agent Decision
```

### Observation vs. State vs. Belief State

1. **State ($s_t$)**: Complete physical configuration of the world. (e.g., exact 3D positions, velocities, and battery charge of all robots).
2. **Observation ($o_t$)**: Raw, localized, noisy sensor input received by the agent at step $t$. (e.g., a single 2D camera frame or LiDAR scan).
3. **Belief State ($b_t$)**: A probability distribution over possible underlying states $s \in \mathcal{S}$ maintained by the agent given past observations and actions:
   $$b_t(s) = P(S_t = s \vert o_t, a_{t-1}, o_{t-1}, \dots, o_0)$$

In practice, autonomous agents handle POMDPs by maintaining a memory vector $h_t$ (via Recurrent Neural Networks like LSTM/GRU, Transformer memory, or explicit Kalman filters) that approximates $b_t$:

$$h_t = \text{RNN}(h_{t-1}, [o_t, a_{t-1}])$$

---

## 2. Delayed Reward & Temporal Credit Assignment

Autonomous tasks often feature delayed sparse rewards: a mobile robot drives through 500 navigation steps before receiving a single $+1.0$ reward for reaching the goal destination.

How do we assign credit or blame to intermediate actions taken 300 steps prior?

```text
Step:     t=0          t=100          t=300          t=500 (Goal Reached)
Action:   Start        Turn Right     Accelerate     Stop
Reward:   r=0          r=0            r=0            r=+100

Which action was responsible for reaching the goal?
- 1-Step TD (TD(0)): Propagates r=+100 backward 1 step per episode (Extremely Slow).
- Monte Carlo: Assigns full return to all steps (High Variance).
- n-Step / TD(λ): Balances bias and variance to propagate credit efficiently.
```

### $n$-Step Returns

Rather than updating value estimates using 1 step ($r_t + \gamma V(s_{t+1})$) or full episodes ($G_t$), $n$-step returns look ahead $n$ environment transitions:

$$G_{t:t+n} = r_t + \gamma r_{t+1} + \gamma^2 r_{t+2} + \dots + \gamma^{n-1} r_{t+n-1} + \gamma^n V(s_{t+n})$$

- $n = 1$: Standard 1-step Temporal Difference ($\text{TD}(0)$). Low variance, high bias.
- $n = \infty$: Full-episode Monte Carlo return. Zero bias, extremely high variance.
- $n \in [3, 10]$: Optimal intermediate tradeoff for deep RL navigation and control.

### $\text{TD}(\lambda)$ & Eligibility Traces

$\text{TD}(\lambda)$ computes an exponentially weighted average over all $n$-step returns using decay parameter $\lambda \in [0, 1]$:

$$G_t^\lambda = (1 - \lambda) \sum_{n=1}^{\infty} \lambda^{n-1} G_{t:t+n}$$

In backward-view updates, this is implemented using **Eligibility Traces** $e_t(s)$, which record how recently and frequently state $s$ was visited:

$$e_t(s) = \gamma \lambda e_{t-1}(s) + \mathbb{I}(S_t = s)$$

When a delayed reward occurs, states with high eligibility trace values receive immediate proportional credit updates without waiting for $N$ full episode iterations.

---

## 3. Model-Free vs. Model-Based RL

```text
                              ┌───────────────────────────────┐
                              │  Reinforcement Learning Path  │
                              └───────────────┬───────────────┘
                                              │
                     ┌────────────────────────┴────────────────────────┐
                     ▼                                                 ▼
        ┌─────────────────────────┐                       ┌─────────────────────────┐
        │      Model-Free RL      │                       │     Model-Based RL      │
        └────────────┬────────────┘                       └────────────┬────────────┘
                     │                                                 │
        ┌────────────┴────────────┐                       ┌────────────┴────────────┐
        ▼                         ▼                       ▼                         ▼
┌──────────────┐          ┌──────────────┐        ┌──────────────┐          ┌──────────────┐
│ Value-Based  │          │ Policy-Based │        │ Given Model  │          │ Learned Model│
│ (DQN, Double)│          │ (PPO, SAC)   │        │ (Physics/Sim)│          │ (World Model)│
└──────────────┘          └──────────────┘        └──────────────┘          └──────────────┘
```

### Model-Free RL
- **Concept**: The agent learns $Q(s,a)$ or $\pi(a|s)$ directly through trial-and-error environment interaction without building an explicit internal world transition model.
- **Pros**: High performance ceilings, no model-bias errors, lower runtime inference cost per decision.
- **Cons**: High sample complexity (requires millions of steps).

### Model-Based RL
- **Concept**: The agent learns or is provided with an explicit environment transition model $P(s' \vert s, a)$ and reward function $R(s, a)$.
- **Pros**: Sample efficient; allows internal planning and "what-if" trajectory rollouts without executing dangerous actions in the physical world.
- **Cons**: Subject to **model exploitation** (errors in learned dynamics accumulate during multi-step rollouts, causing planners to find false shortcuts).

---

## 4. Planning, Rollouts, & Monte Carlo Tree Search (MCTS)

### Rollout Simulation

Given a world model $\hat{P}(s' \vert s, a)$ and policy $\pi$, a **rollout** simulates future trajectory steps in imaginary space:

$$\tau_{\text{imagined}} = (s_0, a_0, r_0, s_1, a_1, r_1, \dots, s_K)$$

Simulating $M$ parallel rollouts from current state $s_0$ evaluates action consequences prior to executing physical motors.

### Monte Carlo Tree Search (MCTS)

MCTS is a decision-time model-based planning algorithm that builds an asymmetric search tree over state-action spaces through 4 iterative phases:

```text
 1. SELECTION               2. EXPANSION             3. SIMULATION            4. BACKPROPAGATION
    (UCT Rule)                                           (Rollout Policy)

      ( S0 )                  ( S0 )                   ( S0 )                  ( S0 )  r=+1
      /    \                  /    \                   /    \                  /    \
   (S1)   (S2)             (S1)   (S2)              (S1)   (S2)             (S1)   (S2)
    |                       |      |                 |      |                |      |
   (S3)*                   (S3)   (S2,a1)           (S3)   (S2,a1)          (S3)   (S2,a1)
                                                            ┊                        ┊
                                                       Simulated                Update Q & N
                                                       Trajectory               counts along
                                                        (s -> Goal)             path
```

1. **Selection**: Starting from root node $s_0$, recursively traverse child nodes using the Upper Confidence Bound for Trees (UCT) selection rule:
   $$\text{UCT}(s, a) = Q(s, a) + c_{\text{puct}} \cdot P(a \vert s) \cdot \frac{\sqrt{N(s)}}{1 + N(s, a)}$$
2. **Expansion**: Upon reaching an unvisited leaf node $s_l$, expand one or more valid action child states.
3. **Simulation**: Execute a fast rollout policy (or query a neural value net) from the expanded node to estimate future trajectory value $v$.
4. **Backpropagation**: Propagate the evaluation return $v$ backward up the tree path, updating visit counts $N(s, a)$ and mean value estimates $Q(s, a)$ for all ancestor nodes.

Decision-time planning via MCTS provides dramatic accuracy improvements over raw network policy priors, enabling agents to solve complex strategic and spatial tasks.
