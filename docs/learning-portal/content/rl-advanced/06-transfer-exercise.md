# Module 06: Final Transfer Exercise — Layered Autonomous Agent Architecture

## Mission Context: Autonomous Warehouse Inspection & Repair Rover

You are the Principal Autonomous Systems Architect designing a fleet of heavy-duty autonomous inspection and repair rovers deployed in a 500,000 sq ft industrial warehouse.

The rover must navigate cluttered aisles, inspect high-voltage electrical panels, deliver emergency repair tools to human technicians, monitor internal battery levels, and avoid collisions with human workers and fast-moving forklifts.

```text
                                        WAREHOUSE ENVIRONMENT
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                                  │
│    [Charging Dock] ─── (Aisle 1) ───► [High-Voltage Panel A] ─── (Aisle 2) ───► [Tool Depot]    │
│            ▲                                  │                                    │             │
│            │                                  ▼                                    ▼             │
│            └───────────────────────── [Forklift Zone B] ───────────────────────────┘             │
│                                        (Dynamic Obstacles)                                       │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Part 1: Mapping Architectural Layers

Map each technical component studied across Modules 01–04 onto the **6-Layer Autonomous Agent Architecture**.

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Layer 1: PERCEPTION     ──────► Raw Sensor Fusion & Recurrent Belief State Update (POMDP)        │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Layer 2: NEEDS          ──────► Internal Telemetry & Critical Battery/Heat Threshold Assessment  │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Layer 3: GOAL           ──────► Priority Arbitration (Mission Goals vs. Urgent Internal Needs)   │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Layer 4: DECISION/PLAN  ──────► High-Level Task Decomposition (PDDL / Symbolic / MCTS Graph Search)│
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Layer 5: BEHAVIOR       ──────► Behavior Tree Ticker (Precondition Safety Checks & Fallbacks)    │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Layer 6: ACTION         ──────► Continuous Motor Execution (Learned PPO Options / Motor Controls)│
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Layer 1: Perception (Sensor Fusion & Belief State Update)
- **Primary Mechanism**: Multi-sensor fusion (2D LiDAR, Depth Camera, Wheel Odometry) processed by a Recurrent Neural Network / LSTM memory layer.
- **Architectural Function**: The environment is partially observable (POMDP) due to camera blind spots, dust occlusions, and dynamic obstacles. Layer 1 updates a continuous **Belief Vector** $b_t = \text{RNN}(b_{t-1}, [o_t, a_{t-1}])$ estimating true rover location and forklift motion vectors.

### Layer 2: Needs (Internal State Monitoring)
- **Primary Mechanism**: Hardware telemetry assessment.
- **Architectural Function**: Continuous evaluation of internal health indicators:
  $$\text{Battery State } (\text{SOC} \in [0\%, 100\%]), \quad \text{Motor Temp } (T \in [20^\circ\text{C}, 110^\circ\text{C}]), \quad \text{Storage Memory}$$
- Emits urgency flags when internal health bounds are breached (e.g., `CRITICAL_BATTERY` when SOC $< 15\%$).

### Layer 3: Goal (Mission Arbitration)
- **Primary Mechanism**: Deterministic utility arbitrator.
- **Architectural Function**: Resolves conflicts between external mission requests and internal needs.
  - *Normal State*: Goal = `INSPECT_PANEL_A`.
  - *Conflict State*: If Layer 2 fires `CRITICAL_BATTERY`, Goal Layer pre-empts the mission goal and sets active Goal = `NAVIGATE_TO_CHARGER`.

### Layer 4: Decision & Planning (Macroscopic Task Decomposition)
- **Primary Mechanism**: Symbolic PDDL / MCTS Graph Planner.
- **Architectural Function**: Decomposes the active goal into an ordered sequence of discrete macro-actions (Options/Sub-goals) over a topological map graph:
  $$\text{Plan} = [\text{Option}_{\text{Navigate}}(\text{Aisle1}), \, \text{Option}_{\text{Align}}(\text{PanelA}), \, \text{Option}_{\text{Inspect}}(\text{ThermalCam})]$$

### Layer 5: Behavior Execution (Behavior Tree Control Flow)
- **Primary Mechanism**: Behavior Tree (BT) running at 100 Hz ticker frequency.
- **Architectural Function**: Enforces deterministic safety preconditions and reactive fallbacks before executing motor commands.
  ```text
  Selector (Root)
  ├── Sequence (Emergency Safety)
  │   ├── Condition: IsObstacleDistance < 0.5m?
  │   └── Action: TriggerEmergencyBrake
  └── Sequence (Execute Plan Option)
      ├── Condition: IsPathClear?
      └── Action: StepRLOptionPolicy(v_cmd, ω_cmd)
  ```

### Layer 6: Action (Continuous Motor Execution)
- **Primary Mechanism**: Deep RL Options trained via PPO / Continuous Actor-Critic.
- **Architectural Function**: Takes target sub-goal relative coordinates and outputs high-frequency continuous wheel motor torques $(\tau_{\text{left}}, \tau_{\text{right}}) \in \mathbb{R}^2$ at 50 Hz.

---

## Part 2: Architectural Stress-Testing Scenarios

Analyze how the layered agent handles real-world failure scenarios.

### Scenario A: Delayed Reward during Docking
*Challenge*: The rover receives a positive reward $+100$ only after completing a precise 200-step alignment maneuver into the charging dock.
- **Problem**: 1-step Temporal Difference ($\text{TD}(0)$) propagates credit back 1 step per training episode, requiring thousands of failed attempts to learn the docking maneuver.
- **Architectural Solution**: The low-level RL action option uses **$n$-step returns** ($n=8$) or **$\text{TD}(\lambda)$ eligibility traces** to propagate docking reward immediately back to early alignment adjustments.

### Scenario B: Temporary Sensor Blackout in Aisle 2
*Challenge*: Passing through a dusty corridor blinds the optical depth camera for 3 seconds ($t=100$ to $t=150$).
- **Problem**: Raw observation $o_t$ becomes zero/corrupted. An unlayered feedforward network would output random erratic actions.
- **Architectural Solution**:
  1. Layer 1's recurrent belief state $b_t = \text{RNN}(b_{t-1}, [o_t, a_{t-1}])$ uses internal dead-reckoning odometry to maintain an estimated belief position during the blackout.
  2. Layer 5's Behavior Tree detects low confidence in perception and triggers a fallback `SlowSpeedScan` option until camera streams recover.

### Scenario C: Out-of-Distribution Motor Failure
*Challenge*: Deep RL action network outputs a maximum torque command towards a wall due to an adversarial sensor glare.
- **Problem**: Black-box neural policy failure.
- **Architectural Solution**: Layer 5's Behavior Tree evaluates the deterministic safety precondition `IsObstacleDistance < 0.5m` **after** the RL action is computed but **before** commands reach hardware motors. The BT revokes the policy action and forces `EmergencyBrake`, proving that safety does not rely on neural network reliability.

---

## Part 3: Design Evaluation Questions

Answer the following synthesis questions to verify complete transfer of concepts:

1. **Why is Double DQN unsuitable for Layer 6's continuous steering control?**
   - *Answer*: Double DQN requires evaluating $\arg\max_a Q(s', a; \theta)$ over action space $\mathcal{A}$. For continuous wheel velocity control $(\mathbb{R}^2)$, finding the maximum over infinite continuous actions at 50 Hz is computationally impossible. Continuous Actor-Critic methods (PPO/SAC) must be used instead.

2. **How does the Options framework prevent the Symbolic Planner (Layer 4) from becoming overwhelmed?**
   - *Answer*: Without options, Layer 4 would have to plan 10,000 primitive motor torque steps individually. By abstracting 1,000 motor steps into a single macro-option (`Navigate(Aisle1)`), Layer 4 plans across a Semi-MDP of 5 macro-steps, reducing search space complexity exponentially.

3. **In what layer should battery management logic reside, and why?**
   - *Answer*: Battery telemetry is monitored in Layer 2 (Needs), which signals Layer 3 (Goal) to re-prioritize objectives. It should **not** be baked into Layer 6's RL reward function alone, because reward-shaping for battery survival can be bypassed by function approximation errors, leading to total power loss.
