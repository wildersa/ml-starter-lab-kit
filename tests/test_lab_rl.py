"""Unit tests for LabRL environment and Q-Learning agent."""
import pytest
from portal.lab_rl.env import GridWorldEnv, AgentTransition
from portal.lab_rl.agent import QLearningAgent


def test_gridworld_env_step_and_reset():
    env = GridWorldEnv()
    start_state = env.reset(seed=42)
    assert start_state == (0, 0)

    # Step RIGHT (action 1)
    record = env.step(1)
    assert record.step_number == 1
    assert record.transition.state == (0, 0)
    assert record.transition.action == 1
    assert record.transition.reward == -0.1
    assert record.transition.next_state == (0, 1)
    assert not record.transition.done


def test_qlearning_agent_update_diagnostic():
    agent = QLearningAgent(alpha=0.5, gamma=0.9)
    transition = AgentTransition(
        state=(0, 0),
        action=1,
        reward=10.0,
        next_state=(0, 1),
        done=False,
    )

    diag = agent.update(transition)
    assert diag.old_q == 0.0
    assert diag.reward == 10.0
    assert diag.max_next_q == 0.0
    assert diag.target == 10.0
    assert diag.td_error == 10.0
    assert diag.new_q == 5.0  # 0 + 0.5 * (10 - 0) = 5.0
    assert agent.get_q_value((0, 0), 1) == 5.0
