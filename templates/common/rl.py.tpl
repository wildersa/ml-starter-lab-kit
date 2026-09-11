"""
Reinforcement Learning (RL) Foundation Module.

Provides explicit, lightweight contracts and dataclasses for:
- Environment (state vs. observation split, stepping, rendering)
- AgentTransition (agent-visible transition data, preventing state leakage in POMDPs)
- StepRecord (richer debug/history record for UI teaching and analysis)
- Agent (action selection, learning update, policy/Q-value inspection)
- RLRunner (coordinating step/reset execution, transition recording, return tracking)
- Toy Gridworld environment and Tabular Q-agent for demonstrations.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Protocol, Union
import random


@dataclass
class AgentTransition:
    """Agent-visible transition data (contains only observable feedback, preventing state leakage)."""
    observation_before: Any
    action: Any
    reward: float
    observation_after: Any
    terminated: bool
    truncated: bool
    info: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StepRecord:
    """Richer debug and history record containing both full internal environment state and agent transition."""
    episode: int
    step: int
    state_before: Any
    state_after: Any
    transition: AgentTransition
    update_info: Dict[str, Any] = field(default_factory=dict)

    # Helper properties for backwards compatibility and UI convenience
    @property
    def observation_before(self) -> Any:
        return self.transition.observation_before

    @property
    def action(self) -> Any:
        return self.transition.action

    @property
    def reward(self) -> float:
        return self.transition.reward

    @property
    def observation_after(self) -> Any:
        return self.transition.observation_after

    @property
    def terminated(self) -> bool:
        return self.transition.terminated

    @property
    def truncated(self) -> bool:
        return self.transition.truncated

    @property
    def info(self) -> Dict[str, Any]:
        return self.transition.info


class BaseEnvironment:
    """Protocol / Interface for RL Environments in this Lab."""

    def reset(self, seed: Optional[int] = None) -> Tuple[Any, Dict[str, Any]]:
        """Resets the environment to an initial state."""
        raise NotImplementedError

    def step(self, action: Any) -> Tuple[Any, float, bool, bool, Dict[str, Any]]:
        """
        Executes one environment step.
        Returns: (observation, reward, terminated, truncated, info)
        """
        raise NotImplementedError

    def available_actions(self, observation: Optional[Any] = None) -> List[Any]:
        """Returns the list of valid actions for the current or given observation."""
        raise NotImplementedError

    def get_state(self) -> Any:
        """Returns the true underlying state (for teaching/debug/MDP analysis)."""
        raise NotImplementedError

    def render_ascii(self) -> str:
        """Returns an ASCII text representation of the environment."""
        return ""


class BaseAgent:
    """Protocol / Interface for RL Agents in this Lab."""

    def select_action(self, observation: Any, available_actions: List[Any]) -> Any:
        """Selects an action given the current observation and available actions."""
        raise NotImplementedError

    def update(self, transition: AgentTransition, available_next_actions: Optional[List[Any]] = None) -> Dict[str, Any]:
        """
        Updates agent parameters given an agent-visible transition.
        `transition` contains ONLY observation_before, action, reward, observation_after, terminated, truncated, info.
        Returns a dict of diagnostics (e.g. td_error, q_old, q_new) for UI inspection.
        """
        return {}

    def reset_episode(self) -> None:
        """Optional callback called at the start of a new episode."""
        pass

    def get_policy(self, observation: Any, available_actions: Optional[List[Any]] = None) -> Dict[Any, float]:
        """Returns action probabilities P(a|s) for the given observation."""
        return {}

    def get_values(self) -> Dict[Any, float]:
        """Returns V(s) state-value estimates if available."""
        return {}

    def get_q_values(self, observation: Any) -> Dict[Any, float]:
        """Returns Q(s, a) action-value estimates for the given observation."""
        return {}

    def set_q_value(self, observation: Any, action: Any, value: float) -> None:
        """Allows manual editing/overriding of Q(s, a) for teaching experiments."""
        pass


class RLRunner:
    """
    Coordinates the interaction loop between Environment and Agent.
    Maintains history, cumulative return (undiscounted total episode reward), episode counters, and manual/auto stepping.
    """

    def __init__(self, env: BaseEnvironment, agent: BaseAgent):
        self.env = env
        self.agent = agent
        self.episode_count: int = 0
        self.step_count: int = 0
        self.history: List[StepRecord] = []
        self.current_obs: Any = None
        self.current_info: Dict[str, Any] = {}
        self.is_terminated: bool = False
        self.is_truncated: bool = False
        self.cumulative_return: float = 0.0  # Undiscounted total episode reward (\sum r_t)

        self.reset_episode()

    def reset_episode(self, seed: Optional[int] = None) -> Tuple[Any, Dict[str, Any]]:
        """Resets environment and agent for a new episode."""
        if self.step_count > 0 or self.episode_count == 0:
            self.episode_count += 1
        self.step_count = 0
        self.cumulative_return = 0.0
        self.is_terminated = False
        self.is_truncated = False
        self.agent.reset_episode()

        self.current_obs, self.current_info = self.env.reset(seed=seed)
        return self.current_obs, self.current_info

    def step(self, action: Optional[Any] = None) -> StepRecord:
        """
        Executes a single step in the environment.
        If action is None, asks agent to select an action automatically.
        """
        if self.is_terminated or self.is_truncated:
            self.reset_episode()

        available = self.env.available_actions(self.current_obs)
        if action is None:
            action = self.agent.select_action(self.current_obs, available)

        state_before = self.env.get_state()
        obs_before = self.current_obs

        obs_after, reward, terminated, truncated, info = self.env.step(action)
        state_after = self.env.get_state()

        self.step_count += 1
        self.cumulative_return += reward
        self.is_terminated = terminated
        self.is_truncated = truncated
        self.current_obs = obs_after
        self.current_info = info

        # Agent-visible transition (strictly NO state_before or state_after)
        agent_transition = AgentTransition(
            observation_before=obs_before,
            action=action,
            reward=reward,
            observation_after=obs_after,
            terminated=terminated,
            truncated=truncated,
            info=info
        )

        available_next = self.env.available_actions(obs_after) if not (terminated or truncated) else []
        update_info = self.agent.update(agent_transition, available_next_actions=available_next)

        record = StepRecord(
            episode=self.episode_count,
            step=self.step_count,
            state_before=state_before,
            state_after=state_after,
            transition=agent_transition,
            update_info=update_info
        )

        self.history.append(record)
        return record


class GridworldToyEnv(BaseEnvironment):
    """
    A 3x3 Gridworld environment for RL visual scaffolding demonstrations.
    Grid Layout:
      (0,0) [Start]  (0,1) [Empty]  (0,2) [Empty]
      (1,0) [Empty]  (1,1) [Pit -1] (1,2) [Empty]
      (2,0) [Empty]  (2,1) [Empty]  (2,2) [Goal +1]

    Actions: 'UP', 'RIGHT', 'DOWN', 'LEFT'
    """

    ACTIONS = ["UP", "RIGHT", "DOWN", "LEFT"]
    ACTION_OFFSETS = {
        "UP": (-1, 0),
        "RIGHT": (0, 1),
        "DOWN": (1, 0),
        "LEFT": (0, -1),
    }

    def __init__(self, grid_size: int = 3, goal: Tuple[int, int] = (2, 2), pit: Tuple[int, int] = (1, 1)):
        self.grid_size = grid_size
        self.start_pos = (0, 0)
        self.goal_pos = goal
        self.pit_pos = pit
        self.agent_pos = self.start_pos

    def reset(self, seed: Optional[int] = None) -> Tuple[Tuple[int, int], Dict[str, Any]]:
        if seed is not None:
            random.seed(seed)
        self.agent_pos = self.start_pos
        return self.get_observation(), {"grid_size": self.grid_size}

    def get_state(self) -> Tuple[int, int]:
        """Full internal environment state."""
        return self.agent_pos

    def get_observation(self) -> Tuple[int, int]:
        """In this fully observable Gridworld, observation equals state."""
        return self.agent_pos

    def available_actions(self, observation: Optional[Any] = None) -> List[str]:
        return list(self.ACTIONS)

    def step(self, action: str) -> Tuple[Tuple[int, int], float, bool, bool, Dict[str, Any]]:
        if action not in self.ACTIONS:
            raise ValueError(f"Invalid action: {action}. Must be one of {self.ACTIONS}")

        dr, dc = self.ACTION_OFFSETS[action]
        r, c = self.agent_pos
        new_r = max(0, min(self.grid_size - 1, r + dr))
        new_c = max(0, min(self.grid_size - 1, c + dc))

        self.agent_pos = (new_r, new_c)

        if self.agent_pos == self.goal_pos:
            reward = 1.0
            terminated = True
        elif self.agent_pos == self.pit_pos:
            reward = -1.0
            terminated = True
        else:
            reward = -0.01  # Small step penalty
            terminated = False

        truncated = False
        info = {"pos": self.agent_pos}
        return self.get_observation(), reward, terminated, truncated, info

    def render_ascii(self) -> str:
        grid = []
        for r in range(self.grid_size):
            row_str = []
            for c in range(self.grid_size):
                pos = (r, c)
                if pos == self.agent_pos:
                    row_str.append("[A]")
                elif pos == self.goal_pos:
                    row_str.append(" G ")
                elif pos == self.pit_pos:
                    row_str.append(" X ")
                else:
                    row_str.append(" . ")
            grid.append("".join(row_str))
        return "\n".join(grid)


class ToyRLAgent(BaseAgent):
    """
    Simple Tabular Q-Learning Agent for demonstration and teaching.
    Allows inspecting and overriding Q-values and action probabilities.
    """

    def __init__(self, alpha: float = 0.1, gamma: float = 0.9, epsilon: float = 0.2, default_actions: Optional[List[Any]] = None):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.default_actions = default_actions or ["UP", "RIGHT", "DOWN", "LEFT"]
        # Q-table mapping obs -> dict[action, float]
        self.q_table: Dict[Any, Dict[Any, float]] = {}

    def _ensure_obs(self, obs: Any, available_actions: Optional[List[Any]] = None) -> Dict[Any, float]:
        obs_key = str(obs)
        actions = available_actions or self.default_actions
        if obs_key not in self.q_table:
            self.q_table[obs_key] = {a: 0.0 for a in actions}
        else:
            # Ensure all available actions exist in the Q-row so max Q(s', a) uses the full action set
            for a in actions:
                if a not in self.q_table[obs_key]:
                    self.q_table[obs_key][a] = 0.0
        return self.q_table[obs_key]

    def select_action(self, observation: Any, available_actions: List[Any]) -> Any:
        q_vals = self._ensure_obs(observation, available_actions)
        if random.random() < self.epsilon:
            return random.choice(available_actions)

        # Greedy choice with tie breaking
        max_v = max(q_vals[a] for a in available_actions)
        best_actions = [a for a in available_actions if q_vals[a] == max_v]
        return random.choice(best_actions)

    def get_policy(self, observation: Any, available_actions: Optional[List[Any]] = None) -> Dict[Any, float]:
        if available_actions is None:
            available_actions = self.default_actions
        q_vals = self._ensure_obs(observation, available_actions)

        n_actions = len(available_actions)
        if n_actions == 0:
            return {}

        max_v = max(q_vals[a] for a in available_actions)
        best_actions = [a for a in available_actions if q_vals[a] == max_v]

        prob = {}
        base_prob = self.epsilon / n_actions
        for a in available_actions:
            prob[a] = base_prob
            if a in best_actions:
                prob[a] += (1.0 - self.epsilon) / len(best_actions)

        return prob

    def get_q_values(self, observation: Any) -> Dict[Any, float]:
        obs_key = str(observation)
        return dict(self.q_table.get(obs_key, {}))

    def set_q_value(self, observation: Any, action: Any, value: float) -> None:
        obs_key = str(observation)
        if obs_key not in self.q_table:
            self.q_table[obs_key] = {a: 0.0 for a in self.default_actions}
        self.q_table[obs_key][action] = value

    def update(self, transition: AgentTransition, available_next_actions: Optional[List[Any]] = None) -> Dict[str, Any]:
        """
        Q-learning update using strictly agent-visible AgentTransition data.
        Bootstraps max Q(s', a') across the full next action set.
        """
        obs_s = str(transition.observation_before)
        obs_next = str(transition.observation_after)
        action = transition.action
        reward = transition.reward

        # Ensure current observation row exists
        self._ensure_obs(transition.observation_before, [action])
        q_old = self.q_table[obs_s].get(action, 0.0)

        if transition.terminated:
            target = reward
        else:
            # Full next action set bootstrap
            next_actions = available_next_actions if available_next_actions is not None else self.default_actions
            next_q_dict = self._ensure_obs(transition.observation_after, next_actions)
            max_next_q = max(next_q_dict[a] for a in next_actions) if next_actions else 0.0
            target = reward + self.gamma * max_next_q

        td_error = target - q_old
        q_new = q_old + self.alpha * td_error
        self.q_table[obs_s][action] = q_new

        return {
            "obs_before": obs_s,
            "action": action,
            "q_old": round(q_old, 4),
            "reward": round(reward, 4),
            "target": round(target, 4),
            "td_error": round(td_error, 4),
            "q_new": round(q_new, 4),
            "alpha": self.alpha,
            "gamma": self.gamma,
        }
