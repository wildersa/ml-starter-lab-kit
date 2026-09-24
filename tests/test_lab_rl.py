"""Unit tests for LabRL environment and Q-Learning agent."""
import unittest
from portal.lab_rl.env import GridWorldEnv, AgentTransition
from portal.lab_rl.agent import QLearningAgent


class TestLabRL(unittest.TestCase):
    def test_gridworld_env_step_and_reset(self):
        env = GridWorldEnv()
        start_state = env.reset(seed=42)
        self.assertEqual(start_state, (0, 0))

        # Step RIGHT (action 1)
        record = env.step(1)
        self.assertEqual(record.step_number, 1)
        self.assertEqual(record.transition.state, (0, 0))
        self.assertEqual(record.transition.action, 1)
        self.assertEqual(record.transition.reward, -0.1)
        self.assertEqual(record.transition.next_state, (0, 1))
        self.assertFalse(record.transition.done)

    def test_qlearning_agent_update_diagnostic(self):
        agent = QLearningAgent(alpha=0.5, gamma=0.9)
        transition = AgentTransition(
            state=(0, 0),
            action=1,
            reward=10.0,
            next_state=(0, 1),
            done=False,
        )

        diag = agent.update(transition)
        self.assertEqual(diag.old_q, 0.0)
        self.assertEqual(diag.reward, 10.0)
        self.assertEqual(diag.max_next_q, 0.0)
        self.assertEqual(diag.target, 10.0)
        self.assertEqual(diag.td_error, 10.0)
        self.assertEqual(diag.new_q, 5.0)  # 0 + 0.5 * (10 - 0) = 5.0
        self.assertEqual(agent.get_q_value((0, 0), 1), 5.0)


if __name__ == "__main__":
    unittest.main()
