# Module 04: Hierarchical RL & Layered Agent Architecture

## 1. The Need for Abstraction & Hierarchical RL (HRL)

Flat Reinforcement Learning updates primitive motor actions $a \in \mathcal{A}$ at every time step $t$ (e.g., controlling individual joint torques at 100 Hz). For complex tasks requiring 10,000 steps (e.g., "assemble furniture"), flat RL faces exponential exploration decay and severe credit assignment dilution.

**Hierarchical Reinforcement Learning (HRL)** decomposes long-horizon tasks into temporal abstractions: high-level policies select macro-goals, while low-level policies execute primitive action sequences to achieve those goals.

---

## 2. Options Framework & Semi-MDPs (SMDP)

The **Options Framework** (Sutton, Precup, & Singh, 1999) formalizes temporal abstraction. An **Option** $o \in \mathcal{O}$ generalizes a primitive action to a closed-loop multi-step subroutine.

### The 3 Components of an Option

An option $o$ is defined by a 3-tuple $o = (\mathcal{I}_o, \pi_o, \beta_o)$:

$$\text{Option } o = (\mathcal{I}_o, \, \pi_o, \, \beta_o)$$

1. **Initiation Set ($\mathcal{I}_o \subseteq \mathcal{S}$)**: The set of states in which option $o$ can be initiated. ($S_t \in \mathcal{I}_o$).
2. **Internal Option Policy ($\pi_o(a \vert s)$)**: A low-level policy mapping internal states to primitive actions $a \in \mathcal{A}$ while option $o$ is active.
3. **Termination Condition ($\beta_o(s) \in [0, 1]$)**: Probability that option $o$ terminates upon reaching state $s$.

```text
High-Level Policy over Options Ω(o | s):
[ State s0 ] ──────────► Select Option o_nav ("Navigate to Door")
                              │
                              ▼ Option Executing for τ steps
                   Low-level policy π_{o_nav}(a | s)
                   s0 -> a_1 -> s_1 -> a_2 -> s_2 ... -> s_τ
                              │
                              ▼ Termination β_{o_nav}(s_τ) = 1.0 (Door Reached)
[ State s_τ ] ──────────► Select Next Option o_open ("Open Door")
```

### Semi-Markov Decision Process (SMDP)

When an agent chooses options rather than primitive actions, transitions take variable time durations $\tau \in \{1, 2, 3, \dots\}$. The decision process becomes a **Semi-MDP (SMDP)**.

The SMDP Bellman Optimality equation for options accounts for variable transition steps $\tau$ and cumulative discounted option rewards $R_t^\tau$:

$$Q^*(s, o) = \mathbb{E}\left[ R_t^\tau + \gamma^\tau \max_{o' \in \mathcal{O}} Q^*(S_{t+\tau}, o') \;\middle|\; S_t = s, O_t = o \right]$$

where $R_t^\tau = \sum_{k=0}^{\tau-1} \gamma^k r_{t+k}$ is the accumulated return during option execution.

---

## 3. Separation of Responsibilities: Behavior Trees vs. Planners vs. Learned Policies

A common misconception in deep RL is attempting to force a single end-to-end neural network to solve perception, safety, control flow, and long-horizon planning simultaneously. Production-grade autonomous agents enforce strict **separation of responsibilities**.

```text
                               ┌────────────────────────────────────────┐
                               │       High-Level Mission Goal          │
                               └───────────────────┬────────────────────┘
                                                   │
                                                   ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  Symbolic Planner (PDDL / Graph Search)                                                              │
│  - Responsibility: Long-horizon discrete reasoning & sub-goal decomposition.                          │
│  - Time Horizon: Minutes to Hours (Global deterministic logic).                                       │
└──────────────────────────────────────────────────┬───────────────────────────────────────────────────┘
                                                   │ Sub-Goal Sequence
                                                   ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  Behavior Tree (Reactive Execution & Safety Enforcement)                                             │
│  - Responsibility: Deterministic control flow, safety preconditions, fallback triggers.              │
│  - Execution Latency: < 10 ms (Verifiable state-machine logic).                                       │
└──────────────────────────────────────────────────┬───────────────────────────────────────────────────┘
                                                   │ Active Action / Option Target
                                                   ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  Learned Deep RL Policy (Continuous Control / Primitive Options)                                      │
│  - Responsibility: High-frequency motor skills, obstacle avoidance, local trajectory optimization.   │
│  - Execution Frequency: 50 Hz - 200 Hz (Neural network forward pass).                                 │
└──────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Architectural Comparison Matrix

| Architectural Subsystem | Primary Responsibility | Best Tooling / Method | Execution Frequency | Key Advantage | Primary Limitation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Symbolic Planner** | Strategic long-horizon task decomposition. | PDDL, STRIPS, A*/MCTS graph search | Low (On goal shift) | Provably complete; handles complex combinatorics. | High computational cost; vulnerable to invalid state abstractions. |
| **Behavior Tree (BT)** | Safety verification, reactive execution & fallback logic. | BT Frameworks (Sequence, Selector, Condition) | High (100 Hz ticker) | Highly modular, human-interpretable, deterministic safety checks. | Manual tree construction; scales poorly to unstructured perceptual tasks. |
| **Learned Policy (RL)** | Continuous motor execution & local obstacle handling. | Deep RL (PPO, SAC, Option-Critic) | Very High (50–200 Hz) | Generates fluid smooth trajectories over noisy continuous sensors. | Lack of formal safety guarantees; black-box failure modes. |

---

## 4. Layered Autonomous-Agent Architecture

To integrate these complementary systems, modern autonomous agents employ a **6-Layer Architecture**:

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ Layer 1: PERCEPTION      Raw Sensors ──► Filtering & Feature Extraction ──► Belief State│
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
┌───────────────────────────────────────────▼────────────────────────────────────────────┐
│ Layer 2: NEEDS           Internal State Assessment (Battery, Heat, Memory, Safety)     │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
┌───────────────────────────────────────────▼────────────────────────────────────────────┐
│ Layer 3: GOAL            Mission Arbitration (Resolve conflict between Needs & Task)   │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
┌───────────────────────────────────────────▼────────────────────────────────────────────┐
│ Layer 4: DECISION/PLAN   High-Level Sub-Goal Decomposition (Symbolic Planner / MCTS)   │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
┌───────────────────────────────────────────▼────────────────────────────────────────────┐
│ Layer 5: BEHAVIOR        Behavior Tree Ticker (Preconditions, Fallbacks, Option Select)│
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
┌───────────────────────────────────────────▼────────────────────────────────────────────┐
│ Layer 6: ACTION          Motor Execution (Learned RL Options / Classical Control)      │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### Detailed Layer Responsibilities

1. **Perception Layer**: Translates raw camera, LiDAR, and IMU data into structured state/belief representations ($b_t$).
2. **Needs Layer**: Monitors internal state parameters (e.g., battery percentage, hardware temperature, storage limits).
3. **Goal Layer**: Dynamically prioritizes objectives. (e.g., if battery $< 10\%$, override "Search Mission Goal" with "Recharge Urgent Goal").
4. **Decision / Planning Layer**: Constructs high-level macro plan steps to satisfy the current Goal (e.g., `[Navigate(ZoneB) -> Pick(Sample3) -> Return(Base)]`).
5. **Behavior Layer**: Evaluates real-time Behavior Tree ticks. Verifies safety preconditions (e.g., `IsPathClear?`). If an anomaly is detected, switches to fallback behaviors without re-planning.
6. **Action Layer**: Runs continuous high-frequency controllers or trained sub-goal RL policies (Options) to output precise low-level actuator commands.

This layered structure ensures that **safety and high-level goal alignment are preserved deterministically**, freeing the deep RL components to focus strictly on local continuous motor skills where neural learning excels.
