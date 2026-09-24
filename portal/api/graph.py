"""Prerequisite-aware RL Skill Graph and Evaluation Engine."""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
import math

from portal.api import database


@dataclass
class Activity:
    id: str
    prompt: str
    type: str  # "numeric" or "choice"
    options: Optional[List[str]] = None
    expected_answer: Optional[Union[float, str]] = None
    tolerance: float = 0.01
    explanation: str = ""


@dataclass
class SkillNode:
    id: str
    title: str
    prerequisites: List[str]
    theory: str
    worked_example: str
    activities: List[Dict[str, Any]]
    lab_rl_enabled: bool = False


# Canonical RL Curriculum Graph
SKILL_GRAPH_NODES: Dict[str, SkillNode] = {
    "rl-vocab": SkillNode(
        id="rl-vocab",
        title="RL Vocabulary",
        prerequisites=[],
        theory=(
            "Reinforcement Learning (RL) models sequential decision-making where an **Agent** interacts with an **Environment**.\n"
            "At each discrete time step $t$, the agent receives a state $s_t \\in S$, selects an action $a_t \\in A$, receives a numerical reward $r_{t+1} \\in \\mathbb{R}$, "
            "and transitions to next state $s_{t+1}$."
        ),
        worked_example=(
            "**Example**: In a GridWorld navigation task:\n"
            "- State: Agent grid position $(r, c)$\n"
            "- Action: Navigation direction (UP, RIGHT, DOWN, LEFT)\n"
            "- Reward: $+10$ upon reaching goal state, $-0.1$ per step cost."
        ),
        activities=[
            {
                "id": "act_vocab_1",
                "prompt": "Which component in RL provides numerical feedback evaluating the quality of an action?",
                "type": "choice",
                "options": ["State", "Environment", "Reward", "Policy"],
                "expected_answer": "Reward",
                "explanation": "The Reward signal serves as scalar feedback indicating immediate success or penalty.",
            }
        ],
    ),
    "reward-return": SkillNode(
        id="reward-return",
        title="Reward vs Return",
        prerequisites=["rl-vocab"],
        theory=(
            "A **Reward** $r_t$ is the immediate scalar feedback received at step $t$.\n"
            "The **Return** $G_t$ is the total accumulated reward from step $t$ onwards over a trajectory: $G_t = r_{t+1} + r_{t+2} + r_{t+3} + \\dots + r_T$."
        ),
        worked_example=(
            "**Example**: Consider a 3-step episode with immediate rewards: $r_1 = -1.0$, $r_2 = -1.0$, $r_3 = +10.0$.\n"
            "The total undiscounted return $G_0 = -1.0 + (-1.0) + 10.0 = 8.0$."
        ),
        activities=[
            {
                "id": "act_return_1",
                "prompt": "An agent receives immediate rewards $r_1 = -0.5$, $r_2 = -0.5$, $r_3 = 5.0$. What is the total undiscounted return $G_0$?",
                "type": "numeric",
                "expected_answer": 4.0,
                "tolerance": 0.01,
                "explanation": "G_0 = -0.5 + (-0.5) + 5.0 = 4.0",
            }
        ],
    ),
    "discounting": SkillNode(
        id="discounting",
        title="Discounting",
        prerequisites=["reward-return"],
        theory=(
            "In infinite-horizon or risky environments, future rewards are discounted by factor $\\gamma \\in [0, 1)$:\n"
            "$G_t = \\sum_{k=0}^{\\infty} \\gamma^k r_{t+k+1} = r_{t+1} + \\gamma r_{t+2} + \\gamma^2 r_{t+3} + \\dots$\n"
            "Discounting bounds total return mathematically and models preference for immediate over delayed rewards."
        ),
        worked_example=(
            "**Example**: Given rewards $r_1 = 1.0$, $r_2 = 2.0$, $r_3 = 10.0$ and $\\gamma = 0.9$:\n"
            "$G_0 = 1.0 + 0.9 \\times 2.0 + (0.9)^2 \\times 10.0 = 1.0 + 1.8 + 8.1 = 10.9$."
        ),
        activities=[
            {
                "id": "act_discount_1",
                "prompt": "Calculate discounted return $G_0$ for rewards $r_1 = 2.0$, $r_2 = 4.0$ with discount factor $\\gamma = 0.5$.",
                "type": "numeric",
                "expected_answer": 4.0,
                "tolerance": 0.01,
                "explanation": "G_0 = 2.0 + 0.5 * 4.0 = 2.0 + 2.0 = 4.0",
            }
        ],
    ),
    "mdp": SkillNode(
        id="mdp",
        title="MDP",
        prerequisites=["discounting"],
        theory=(
            "A Markov Decision Process (MDP) satisfies the **Markov Property**: the transition probability $P(s' | s, a)$ "
            "depends strictly on the current state $s$ and action $a$, independently of historical trajectory."
        ),
        worked_example=(
            "**Example**: In GridWorld, moving RIGHT from state $(0,0)$ transitions to state $(0,1)$ with probability $1.0$, regardless of how $(0,0)$ was reached."
        ),
        activities=[
            {
                "id": "act_mdp_1",
                "prompt": "Does the Markov property state that future transition dynamics depend on the entire history of past states?",
                "type": "choice",
                "options": ["Yes", "No"],
                "expected_answer": "No",
                "explanation": "No, the Markov property dictates that future states depend ONLY on the present state and action.",
            }
        ],
    ),
    "v-and-q": SkillNode(
        id="v-and-q",
        title="V and Q Functions",
        prerequisites=["mdp"],
        theory=(
            "- **State-Value Function** $V^{\\pi}(s)$: Expected return starting from state $s$ following policy $\\pi$.\n"
            "- **Action-Value Function** $Q^{\\pi}(s, a)$: Expected return starting from state $s$, taking action $a$, then following policy $\\pi$."
        ),
        worked_example=(
            "**Example**: If $Q(s, \\text{RIGHT}) = 8.5$ and $Q(s, \\text{UP}) = 2.1$, taking action RIGHT yields higher expected cumulative return."
        ),
        activities=[
            {
                "id": "act_vq_1",
                "prompt": "If an agent in state $s$ has Q-values $Q(s,\\text{UP})=1.5$, $Q(s,\\text{RIGHT})=4.0$, $Q(s,\\text{DOWN})=-2.0$, what is the max action-value $\\max_a Q(s,a)$?",
                "type": "numeric",
                "expected_answer": 4.0,
                "tolerance": 0.01,
                "explanation": "max_a Q(s, a) = max(1.5, 4.0, -2.0) = 4.0",
            }
        ],
    ),
    "bellman-backup": SkillNode(
        id="bellman-backup",
        title="Bellman Backup",
        prerequisites=["v-and-q"],
        theory=(
            "The Bellman Optimality Equation decomposes value into immediate reward plus discounted optimal future value:\n"
            "$Q^*(s, a) = r + \\gamma \\max_{a'} Q^*(s', a')$"
        ),
        worked_example=(
            "**Example**: Given reward $r = 1.0$, discount $\\gamma = 0.9$, and next-state action values $[2.0, 5.0, 1.0]$:\n"
            "$\\max_{a'} Q(s', a') = 5.0$\n"
            "Target $= 1.0 + 0.9 \\times 5.0 = 5.5$."
        ),
        activities=[
            {
                "id": "act_bellman_1",
                "prompt": "Calculate the Bellman target value for immediate reward $r = -0.1$, discount $\\gamma = 0.9$, and next state max Q-value $\\max_{a'} Q(s', a') = 10.0$.",
                "type": "numeric",
                "expected_answer": 8.9,
                "tolerance": 0.01,
                "explanation": "Target = -0.1 + 0.9 * 10.0 = -0.1 + 9.0 = 8.9",
            }
        ],
    ),
    "td-q-learning": SkillNode(
        id="td-q-learning",
        title="TD / Q-Learning",
        prerequisites=["bellman-backup"],
        theory=(
            "Temporal-Difference (TD) Q-Learning updates action values iteratively using sample transitions $(s, a, r, s')$:\n"
            "$\\text{Target} = r + \\gamma \\max_{a'} Q(s', a')$\n"
            "$\\text{TD Error} = \\text{Target} - Q(s, a)$\n"
            "$Q_{new}(s, a) = Q_{old}(s, a) + \\alpha \\times \\text{TD Error}$"
        ),
        worked_example=(
            "**Example**: $Q_{old}(s, a) = 0.0$, $\\alpha = 0.1$, $\\text{Target} = 10.0$.\n"
            "$\\text{TD Error} = 10.0 - 0.0 = 10.0$.\n"
            "$Q_{new}(s, a) = 0.0 + 0.1 \\times 10.0 = 1.0$."
        ),
        activities=[
            {
                "id": "act_td_1",
                "prompt": "Given $Q_{old}(s,a) = 2.0$, learning rate $\\alpha = 0.2$, and Target $= 7.0$, calculate $Q_{new}(s,a)$.",
                "type": "numeric",
                "expected_answer": 3.0,
                "tolerance": 0.01,
                "explanation": "TD Error = 7.0 - 2.0 = 5.0. Q_new = 2.0 + 0.2 * 5.0 = 3.0.",
            }
        ],
        lab_rl_enabled=True,
    ),
}


def get_curriculum_state(db_path: str = database.DB_PATH) -> List[Dict[str, Any]]:
    progress = database.get_all_skill_progress(db_path)

    nodes_result = []
    for skill_id, node in SKILL_GRAPH_NODES.items():
        user_data = progress.get(skill_id, {"state": "locked", "mastery_score": 0.0, "completed_activities": []})
        current_state = user_data["state"]

        # Compute state based on prerequisites if currently locked
        prereqs_met = all(
            progress.get(p, {}).get("state") in ("acquired", "mastered")
            for p in node.prerequisites
        )

        if current_state == "locked" and prereqs_met:
            current_state = "available"

        nodes_result.append({
            "id": node.id,
            "title": node.title,
            "prerequisites": node.prerequisites,
            "state": current_state,
            "mastery_score": user_data["mastery_score"],
            "lab_rl_enabled": node.lab_rl_enabled,
        })

    return nodes_result


def evaluate_activity(
    skill_id: str,
    activity_id: str,
    given_answer: Any,
    db_path: str = database.DB_PATH,
) -> Dict[str, Any]:
    if skill_id not in SKILL_GRAPH_NODES:
        raise ValueError(f"Unknown skill_id: {skill_id}")

    node = SKILL_GRAPH_NODES[skill_id]
    activity_dict = next((a for a in node.activities if a["id"] == activity_id), None)
    if not activity_dict:
        raise ValueError(f"Unknown activity_id: {activity_id} for skill: {skill_id}")

    act_type = activity_dict["type"]
    expected = activity_dict["expected_answer"]
    explanation = activity_dict["explanation"]

    is_correct = False
    if act_type == "numeric":
        try:
            val = float(given_answer)
            tol = activity_dict.get("tolerance", 0.01)
            is_correct = abs(val - float(expected)) <= tol
        except (ValueError, TypeError):
            is_correct = False
    else:  # choice / text
        is_correct = str(given_answer).strip().lower() == str(expected).strip().lower()

    feedback = "Correct! " + explanation if is_correct else "Incorrect. " + explanation

    # Record evidence
    database.record_evidence(skill_id, activity_id, is_correct, str(given_answer), feedback, db_path)

    # Update progress if correct
    if is_correct:
        existing = database.get_all_skill_progress(db_path).get(skill_id, {
            "state": "available",
            "mastery_score": 0.0,
            "completed_activities": [],
        })
        completed = set(existing["completed_activities"])
        completed.add(activity_id)

        # Mark acquired/mastered if all activities complete
        total_acts = len(node.activities)
        mastery = len(completed) / float(total_acts)
        new_state = "acquired" if mastery >= 1.0 else "started"

        database.save_skill_progress(skill_id, new_state, mastery, list(completed), db_path)

    return {
        "is_correct": is_correct,
        "feedback": feedback,
        "explanation": explanation,
        "unlocked_next": get_curriculum_state(db_path),
    }
