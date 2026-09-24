"""LabRL execution environment and contracts."""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Union
import random


@dataclass
class AgentTransition:
    """Agent-observable state transition without hidden POMDP variables."""
    state: Tuple[int, int]
    action: int
    reward: float
    next_state: Tuple[int, int]
    done: bool


@dataclass
class StepRecord:
    """Full environment debug record for traceability."""
    step_number: int
    transition: AgentTransition
    info: Dict[str, Any] = field(default_factory=dict)


class BaseEnvironment:
    """Abstract Base Class for LabRL environments."""
    def reset(self, seed: Optional[int] = None) -> Tuple[int, int]:
        raise NotImplementedError

    def step(self, action: int) -> StepRecord:
        raise NotImplementedError


class GridWorldEnv(BaseEnvironment):
    """
    Deterministic 3x3 GridWorld MDP.
    Grid coordinates: (row, col) from (0,0) top-left to (2,2) bottom-right.
    Start state: (0, 0)
    Goal state: (2, 2), reward +10.0, terminal.
    Pit state: (1, 1), reward -5.0, non-terminal or terminal (here non-terminal with penalty).
    Actions: 0: UP, 1: RIGHT, 2: DOWN, 3: LEFT
    Step cost: -0.1
    """

    ACTION_NAMES = {0: "UP", 1: "RIGHT", 2: "DOWN", 3: "LEFT"}
    ACTION_VECTORS = {
        0: (-1, 0),  # UP
        1: (0, 1),   # RIGHT
        2: (1, 0),   # DOWN
        3: (0, -1),  # LEFT
    }

    def __init__(self, grid_size: int = 3, goal_state: Tuple[int, int] = (2, 2), pit_state: Tuple[int, int] = (1, 1)):
        self.grid_size = grid_size
        self.goal_state = goal_state
        self.pit_state = pit_state
        self.start_state = (0, 0)
        self.current_state = self.start_state
        self.step_count = 0
        self.done = False

    def reset(self, seed: Optional[int] = None) -> Tuple[int, int]:
        if seed is not None:
            random.seed(seed)
        self.current_state = self.start_state
        self.step_count = 0
        self.done = False
        return self.current_state

    def step(self, action: int) -> StepRecord:
        if self.done:
            raise RuntimeError("Environment is done. Call reset() before stepping.")

        if action not in self.ACTION_VECTORS:
            raise ValueError(f"Invalid action {action}. Valid actions are 0, 1, 2, 3.")

        self.step_count += 1
        dr, dc = self.ACTION_VECTORS[action]
        r, c = self.current_state
        nr = max(0, min(self.grid_size - 1, r + dr))
        nc = max(0, min(self.grid_size - 1, c + dc))
        next_state = (nr, nc)

        # Calculate reward and termination
        if next_state == self.goal_state:
            reward = 10.0
            self.done = True
        elif next_state == self.pit_state:
            reward = -5.0
            self.done = False
        else:
            reward = -0.1
            self.done = False

        transition = AgentTransition(
            state=self.current_state,
            action=action,
            reward=reward,
            next_state=next_state,
            done=self.done,
        )

        record = StepRecord(
            step_number=self.step_count,
            transition=transition,
            info={"action_name": self.ACTION_NAMES[action], "pit_hit": (next_state == self.pit_state)},
        )

        self.current_state = next_state
        return record
