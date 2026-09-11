# 🤖 Reinforcement Learning (RL) Foundation & Extension Guide

Welcome to the **Reinforcement Learning Lab Base**. This foundation provides an explicit, step-by-step interaction loop and visual workspace for RL concepts without hiding algorithm inner workings behind a black-box function call.

---

## 🎯 Architecture & Base Contracts

The RL foundation is built on explicit abstractions located in `src/{{PACKAGE_NAME}}/rl.py`:

### 1. `AgentTransition` vs. `StepRecord` Data Structures
To prevent hidden state leakage in partially observable environments (POMDPs), the interaction loop strictly separates agent-visible feedback from full environment debug data:

```python
@dataclass
class AgentTransition:
    """Agent-visible transition data (contains ONLY observable feedback)."""
    observation_before: Any    # Agent observation o
    action: Any                # Action a
    reward: float              # Reward r
    observation_after: Any     # Next observation o'
    terminated: bool           # Terminal status
    truncated: bool            # Truncated status
    info: dict                 # Diagnostic info

@dataclass
class StepRecord:
    """Richer UI debug & history record combining full world state and AgentTransition."""
    episode: int
    step: int
    state_before: Any          # True internal world state s
    state_after: Any           # Next true internal world state s'
    transition: AgentTransition
    update_info: dict          # Diagnostic data from agent update
```

### 2. `BaseEnvironment` Contract
Implement this interface for any new environment (MDP or POMDP):
```python
class BaseEnvironment:
    def reset(self, seed: Optional[int] = None) -> tuple[Any, dict]:
        """Resets the environment. Returns (observation, info)."""
        ...

    def step(self, action: Any) -> tuple[Any, float, bool, bool, dict]:
        """Executes action. Returns (observation, reward, terminated, truncated, info)."""
        ...

    def available_actions(self, observation: Optional[Any] = None) -> list[Any]:
        """Returns valid actions for current or given observation."""
        ...

    def get_state(self) -> Any:
        """Returns true internal state (for teaching, debugging, and POMDP analysis)."""
        ...

    def render_ascii(self) -> str:
        """Optional ASCII text representation."""
        ...
```

### 3. `BaseAgent` Contract
Implement this interface for any learning or planning algorithm:
```python
class BaseAgent:
    def select_action(self, observation: Any, available_actions: list[Any]) -> Any:
        """Selects an action given current observation."""
        ...

    def update(self, transition: AgentTransition, available_next_actions: Optional[list[Any]] = None) -> dict:
        """Updates agent parameters using agent-visible transition. Returns diagnostic dict."""
        ...

    def get_policy(self, observation: Any, available_actions: Optional[list[Any]] = None) -> dict[Any, float]:
        """Returns action probability distribution P(a|s)."""
        ...

    def get_q_values(self, observation: Any) -> dict[Any, float]:
        """Returns Q(s, a) values for observation."""
        ...

    def set_q_value(self, observation: Any, action: Any, value: float) -> None:
        """Allows manual Q-value overrides in assisted training mode."""
        ...
```

### 4. `RLRunner` Coordinator
Coordinates stepping, episode counters, cumulative return $G_t$ (undiscounted total episode reward $\sum r_t$), and transition history:
```python
runner = RLRunner(env, agent)
record = runner.step(action=chosen_action)  # Manual step
# or
record = runner.step()                      # Auto action from agent policy
```

---

## 🕹️ Assisted Training Mode

In the **Visual RL Workspace** (`python -m {{PACKAGE_NAME}}.lab rl-workspace`), you can run training in **Assisted Mode**:

1. **[ RESET EPISODE ]**: Re-initializes environment and agent episode state.
2. **[ STEP ]**: Executes exactly one transition step.
3. **[ AUTO ]**: Automatically steps at a configurable delay.
4. **[ PAUSE ]**: Pauses automatic stepping to allow close inspection.

### Key Assisted Mode Capabilities:
- **State vs. Observation Split**: Inspect true state $s$ alongside what the agent observed $o$.
- **Manual Action Selection**: Choose specific actions manually to test edge cases or agent counterfactuals.
- **Update Diagnostics**: View exact numeric calculations (TD error $\delta$, Bellman target $r + \gamma \max Q$, old Q vs new Q).
- **Interactive Q-Value Overriding**: Manually edit Q-values and watch the greedy policy and action selection update immediately.
- **Transition History Inspector**: Navigate back to any previous step in the episode to inspect its exact inputs and outputs.

---

## 🔌 How to Plug in Future MDP Exercises

To implement a custom **Fully Observable Markov Decision Process (MDP)** exercise (e.g. Gridworld, Inventory Management, Cliff Walking):

1. **Define Environment**:
   Subclass `BaseEnvironment`. In fully observable MDPs, `get_state()` and `get_observation()` return the same value.
   ```python
   class MyGridworldMDP(BaseEnvironment):
       def reset(self, seed=None):
           self.pos = (0, 0)
           return self.pos, {}

       def step(self, action):
           # update position
           ...
           return next_obs, reward, terminated, truncated, info

       def get_state(self):
           return self.pos
   ```

2. **Define Agent**:
   Implement a tabular algorithm (e.g., Q-Learning, SARSA, Monte Carlo) by subclassing `BaseAgent`.
   ```python
   class MyQLearningAgent(BaseAgent):
       def update(self, transition: AgentTransition, available_next_actions=None) -> dict:
           # compute TD error using AgentTransition and update Q(obs, action)
           ...
           return {"td_error": td_err, "q_new": new_val}
   ```

3. **Plug into Workspace**:
   Pass your instances into `RLRunner(env, agent)` in `src/{{PACKAGE_NAME}}/rl_workspace.py`.

---

## 🐯 How to Plug in Future POMDP Exercises

To implement a custom **Partially Observable Markov Decision Process (POMDP)** exercise (e.g., Tiger Problem, Maze with Partial Visibility):

1. **Define Environment with State/Observation Split**:
   - `get_state()` returns the true environment state $s$ (e.g., `tiger_location = "LEFT"`).
   - `get_observation()` returns noisy or partial observation $o$ (e.g., `growl = "LEFT"` with probability $0.85$).
   ```python
   class TigerPOMDPEnv(BaseEnvironment):
       def reset(self, seed=None):
           self.true_tiger_pos = random.choice(["LEFT", "RIGHT"])
           return "LISTEN_OBS_INITIAL", {"true_state": self.true_tiger_pos}

       def step(self, action):
           if action == "LISTEN":
               obs = self.true_tiger_pos if random.random() < 0.85 else ("RIGHT" if self.true_tiger_pos == "LEFT" else "LEFT")
               reward = -1.0
               terminated = False
           elif action == "OPEN_LEFT":
               reward = -100.0 if self.true_tiger_pos == "LEFT" else 10.0
               terminated = True
               obs = "TERMINAL"
           ...
           return obs, reward, terminated, False, {}

       def get_state(self):
           return {"tiger_position": self.true_tiger_pos}
   ```

2. **Define Belief Agent**:
   Implement an agent maintaining a belief state $b(s)$ updated via Bayes rule inside `update(transition: AgentTransition)`. Note that `AgentTransition` strictly isolates the agent from `self.true_tiger_pos`.

3. **Visualize in Workspace**:
   The transition panel will clearly highlight the distinction between `State Before` and `Observation Before`, allowing students to visually see partial observability in action.

---

## 📚 References & Recommended Reading
- Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press.
- Kaelbling, L. P., Littman, M. L., & Cassandra, A. R. (1998). Planning and acting in partially observable stochastic domains. *Artificial Intelligence*, 101(1-2), 99-134.
