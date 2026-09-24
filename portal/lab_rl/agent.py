"""Tabular Q-Learning agent with explicit update diagnostics."""
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any
from portal.lab_rl.env import AgentTransition


@dataclass
class QUpdateDiagnostic:
    """Traceable diagnostic data for a single Q-value update."""
    state: Tuple[int, int]
    action: int
    reward: float
    next_state: Tuple[int, int]
    done: bool
    old_q: float
    max_next_q: float
    target: float
    td_error: float
    new_q: float
    alpha: float
    gamma: float


class QLearningAgent:
    """
    Tabular Q-Learning Agent with explicit diagnostics.
    Updates Q(s, a) = Q(s, a) + alpha * [r + gamma * max_a' Q(s', a') - Q(s, a)]
    """

    def __init__(self, alpha: float = 0.1, gamma: float = 0.9, num_actions: int = 4, grid_size: int = 3):
        self.alpha = alpha
        self.gamma = gamma
        self.num_actions = num_actions
        self.grid_size = grid_size
        self.q_table: Dict[Tuple[int, int], List[float]] = {}
        self.reset_q_table()

    def reset_q_table(self):
        self.q_table = {
            (r, c): [0.0] * self.num_actions
            for r in range(self.grid_size)
            for c in range(self.grid_size)
        }

    def get_q_value(self, state: Tuple[int, int], action: int) -> float:
        return self.q_table.get(state, [0.0] * self.num_actions)[action]

    def update(self, transition: AgentTransition) -> QUpdateDiagnostic:
        s = transition.state
        a = transition.action
        r = transition.reward
        s_next = transition.next_state
        done = transition.done

        old_q = self.get_q_value(s, a)

        if done:
            max_next_q = 0.0
            target = r
        else:
            max_next_q = max(self.q_table.get(s_next, [0.0] * self.num_actions))
            target = r + self.gamma * max_next_q

        td_error = target - old_q
        new_q = old_q + self.alpha * td_error

        # Update table
        self.q_table[s][a] = round(new_q, 4)

        return QUpdateDiagnostic(
            state=s,
            action=a,
            reward=r,
            next_state=s_next,
            done=done,
            old_q=round(old_q, 4),
            max_next_q=round(max_next_q, 4),
            target=round(target, 4),
            td_error=round(td_error, 4),
            new_q=round(new_q, 4),
            alpha=self.alpha,
            gamma=self.gamma,
        )

    def get_serialized_q_table(self) -> Dict[str, List[float]]:
        return {f"{r},{c}": [round(v, 4) for v in values] for (r, c), values in self.q_table.items()}
