"""Session and execution state management for Lab Runtime."""
import uuid
import time
from typing import Dict, Optional, Any, List
from portal.lab_rl.env import GridWorldEnv, StepRecord
from portal.lab_rl.agent import QLearningAgent, QUpdateDiagnostic


class RuntimeSession:
    """An isolated execution session in the Lab Runtime."""

    def __init__(self, session_id: str, capability: str = "rl_simulation", alpha: float = 0.1, gamma: float = 0.9):
        self.session_id = session_id
        self.capability = capability
        self.created_at = time.time()
        self.last_accessed = time.time()
        self.env = GridWorldEnv()
        self.agent = QLearningAgent(alpha=alpha, gamma=gamma)

    def touch(self):
        self.last_accessed = time.time()

    def reset(self, seed: Optional[int] = 42) -> Dict[str, Any]:
        self.touch()
        start_state = self.env.reset(seed=seed)
        self.agent.reset_q_table()
        return {
            "session_id": self.session_id,
            "state": list(start_state),
            "grid_size": self.env.grid_size,
            "goal_state": list(self.env.goal_state),
            "pit_state": list(self.env.pit_state),
            "q_table": self.agent.get_serialized_q_table(),
            "step_count": self.env.step_count,
            "done": self.env.done,
        }

    def step(self, action: int) -> Dict[str, Any]:
        self.touch()
        if self.env.done:
            raise ValueError("Environment is done. Call reset before stepping.")

        step_record: StepRecord = self.env.step(action)
        diagnostic: QUpdateDiagnostic = self.agent.update(step_record.transition)

        return {
            "session_id": self.session_id,
            "step_record": {
                "step_number": step_record.step_number,
                "transition": {
                    "state": list(step_record.transition.state),
                    "action": step_record.transition.action,
                    "reward": step_record.transition.reward,
                    "next_state": list(step_record.transition.next_state),
                    "done": step_record.transition.done,
                },
                "info": step_record.info,
            },
            "diagnostic": {
                "state": list(diagnostic.state),
                "action": diagnostic.action,
                "reward": diagnostic.reward,
                "next_state": list(diagnostic.next_state),
                "done": diagnostic.done,
                "old_q": diagnostic.old_q,
                "max_next_q": diagnostic.max_next_q,
                "target": diagnostic.target,
                "td_error": diagnostic.td_error,
                "new_q": diagnostic.new_q,
                "alpha": diagnostic.alpha,
                "gamma": diagnostic.gamma,
            },
            "q_table": self.agent.get_serialized_q_table(),
            "done": self.env.done,
        }


class SessionManager:
    """Manages active runtime sessions."""

    def __init__(self):
        self._sessions: Dict[str, RuntimeSession] = {}
        self.default_session_id = "default-rl-session"

    def create_session(
        self,
        capability: str = "rl_simulation",
        session_id: Optional[str] = None,
        alpha: float = 0.1,
        gamma: float = 0.9,
    ) -> RuntimeSession:
        if not session_id:
            session_id = f"sess_{uuid.uuid4().hex[:12]}"
        session = RuntimeSession(
            session_id=session_id,
            capability=capability,
            alpha=alpha,
            gamma=gamma,
        )
        self._sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[RuntimeSession]:
        return self._sessions.get(session_id)

    def cancel_session(self, session_id: str) -> bool:
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False

    def get_or_create_default(self) -> RuntimeSession:
        if self.default_session_id not in self._sessions:
            self.create_session(
                capability="rl_simulation",
                session_id=self.default_session_id,
            )
        return self._sessions[self.default_session_id]


session_manager = SessionManager()
