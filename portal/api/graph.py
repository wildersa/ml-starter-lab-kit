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
    misconceptions: Optional[List[Dict[str, Any]]] = None


@dataclass
class SkillNode:
    id: str
    title: str
    prerequisites: List[str]
    theory: str
    worked_example: str
    activities: List[Dict[str, Any]]
    lab_rl_enabled: bool = False
    review_variant: Optional[Dict[str, str]] = None


# Canonical RL Curriculum Graph populated from authored content packs
SKILL_GRAPH_NODES: Dict[str, SkillNode] = {
    "rl-vocab": SkillNode(
        id="rl-vocab",
        title="RL Vocabulary & Agent-Environment Loop",
        prerequisites=[],
        theory=(
            "In supervised learning, a fixed model receives an input $x$ and predicts a label $y$ with immediate feedback.\n"
            "In contrast, an autonomous RL agent operates in a **loop of interaction** with an uncertain environment.\n\n"
            "**Core Vocabulary**:\n"
            "- **Agent**: The autonomous decision-maker (e.g., foraging survival agent, robot, game character).\n"
            "- **Environment**: Everything outside the agent with which it interacts.\n"
            "- **Action ($A_t \\in \\mathcal{A}$)**: A decision chosen by the agent at step $t$.\n"
            "- **Reward ($R_{t+1} \\in \\mathbb{R}$)**: A scalar feedback signal returned by the environment measuring immediate success or penalty.\n"
            "- **Episode**: A complete interaction sequence from start state to terminal state.\n"
            "- **Trajectory ($\\tau$)**: The full sequence over an episode: $\\tau = (S_0, A_0, R_1, S_1, A_1, R_2, \\dots, S_T)$.\n\n"
            "**State vs. Observation**:\n"
            "- **State ($S_t \\in \\mathcal{S}$)**: Complete physical condition of the world.\n"
            "- **Observation ($O_t \\in \\Omega$)**: Partial sensor data accessible to the agent.\n"
            "  - **Fully Observable (MDP)**: $O_t = S_t$. The agent perceives all relevant world state.\n"
            "  - **Partially Observable (POMDP)**: $O_t \\neq S_t$. The agent sees only local sensor data while hidden variables exist."
        ),
        worked_example=(
            "**Example: GridWorld Navigation & Survival Loop**:\n"
            "In a GridWorld navigation task:\n"
            "- State: Agent grid position $(r, c)$\n"
            "- Action: Directions (UP, RIGHT, DOWN, LEFT)\n"
            "- Reward: $+10$ upon reaching goal, $-0.1$ per step cost, $-5.0$ into pit.\n\n"
            "In a survival environment, taking action FORAGE yields immediate reward $R_1 = +2$ and transitions from state Hungry to state Eating."
        ),
        activities=[
            {
                "id": "act_vocab_1",
                "prompt": "Which component in RL provides numerical feedback evaluating the immediate quality of an action?",
                "type": "choice",
                "options": ["State", "Environment", "Reward", "Policy"],
                "expected_answer": "Reward",
                "explanation": "The Reward signal serves as scalar feedback indicating immediate success or penalty.",
                "misconceptions": [
                    {
                        "expected_value": "Policy",
                        "tag": "MISC_REWARD_VS_RETURN",
                        "message": "Policy defines the agent's behavior strategy, not scalar performance feedback.",
                    },
                    {
                        "expected_value": "State",
                        "tag": "MISC_OBS_VS_STATE",
                        "message": "State describes the world condition, not scalar performance feedback.",
                    },
                ],
            },
            {
                "id": "act_vocab_2",
                "prompt": "In a partially observable environment (POMDP), does observation O_t always equal true state S_t?",
                "type": "choice",
                "options": ["Yes", "No"],
                "expected_answer": "No",
                "explanation": "In a POMDP, O_t is a noisy or partial sensor reading, whereas true state S_t includes hidden world variables.",
                "misconceptions": [
                    {
                        "expected_value": "Yes",
                        "tag": "MISC_OBS_VS_STATE",
                        "message": "In a POMDP, observation O_t != S_t because hidden environment variables exist outside agent vision.",
                    }
                ],
            },
        ],
        review_variant={
            "prompt": "Retrieval Challenge: Why does an autonomous survival agent in a partially observable environment (POMDP) fail if treated as a pure Markov state? How can an agent construct a valid Markov state from observations O_0, O_1, ..., O_t?",
            "key_answer": "If key world variables (e.g., predator location) are unobserved in O_t, transition dynamics P(O_{t+1} | O_t) are non-Markovian. To restore the Markov property, the agent must build a state representation S_t using frame stacking, recurrent memory (RNN/LSTM), or a belief distribution over hidden variables.",
        },
    ),
    "reward-return": SkillNode(
        id="reward-return",
        title="Reward vs Return",
        prerequisites=["rl-vocab"],
        theory=(
            "A fundamental distinction in Reinforcement Learning is between immediate feedback and cumulative long-term consequences.\n\n"
            "- **Immediate Reward ($R_{t+1}$)**: The short-term scalar feedback received right after step $t$.\n"
            "- **Cumulative Return ($G_t$)**: The total sum of rewards received from step $t$ onwards over a trajectory:\n"
            "  $$G_t = R_{t+1} + R_{t+2} + R_{t+3} + \\dots + R_T = \\sum_{k=0}^{T-t-1} R_{t+k+1}$$\n\n"
            "Evaluating behavior purely based on immediate reward leads to greedy, short-sighted decisions (e.g., eating poisonous berries yields momentary relief $+2$ but causes fatal illness $-100$ later). Return $G_t$ evaluates true long-term cumulative success."
        ),
        worked_example=(
            "**Example**: Consider a 3-step survival trajectory with immediate rewards: $R_1 = -1.0$ (energy spent moving), $R_2 = -1.0$ (energy searching), $R_3 = +20.0$ (food cache reached).\n"
            "The total undiscounted return from start is $G_0 = -1.0 + (-1.0) + 20.0 = 18.0$."
        ),
        activities=[
            {
                "id": "act_return_1",
                "prompt": "An agent receives immediate rewards r_1 = -0.5, r_2 = -0.5, r_3 = 5.0. What is the total undiscounted return G_0?",
                "type": "numeric",
                "expected_answer": 4.0,
                "tolerance": 0.01,
                "explanation": "G_0 = -0.5 + (-0.5) + 5.0 = 4.0.",
                "misconceptions": [
                    {
                        "expected_value": -0.5,
                        "tag": "MISC_REWARD_VS_RETURN",
                        "message": "You provided immediate reward r_1 (-0.5) instead of total return G_0! Total return G_0 is the sum of all future rewards: -0.5 + (-0.5) + 5.0 = 4.0.",
                    }
                ],
            },
            {
                "id": "act_return_2",
                "prompt": "A survival agent completes a 5-step episode with rewards: R1 = -2.0, R2 = -1.0, R3 = +10.0, R4 = +5.0, R5 = +20.0. Calculate undiscounted return G_0.",
                "type": "numeric",
                "expected_answer": 32.0,
                "tolerance": 0.01,
                "explanation": "G_0 = -2.0 + (-1.0) + 10.0 + 5.0 + 20.0 = 32.0.",
                "misconceptions": [
                    {
                        "expected_value": -2.0,
                        "tag": "MISC_REWARD_VS_RETURN",
                        "message": "You provided immediate reward R1 (-2.0) instead of total cumulative return G_0!",
                    }
                ],
            },
        ],
        review_variant={
            "prompt": "Retrieval Challenge: Why is immediate scalar reward R_{t+1} insufficient for long-term survival planning, and how does cumulative return G_t solve this?",
            "key_answer": "Immediate reward R_{t+1} reflects only single-step outcomes. Cumulative return G_t sums all future rewards over the trajectory so the agent evaluates true long-term survival consequences.",
        },
    ),
    "discounting": SkillNode(
        id="discounting",
        title="Discounting & Infinite Horizons",
        prerequisites=["reward-return"],
        theory=(
            "In infinite-horizon or risky environments, future rewards are discounted by factor $\\gamma \\in [0, 1)$:\n"
            "$$G_t = \\sum_{k=0}^{\\infty} \\gamma^k R_{t+k+1} = R_{t+1} + \\gamma R_{t+2} + \\gamma^2 R_{t+3} + \\dots$$\n\n"
            "Recursive relationship for Return: $G_t = R_{t+1} + \\gamma G_{t+1}$\n\n"
            "**Why discount future rewards?**\n"
            "1. **Mathematical Convergence**: Ensures $G_t$ remains finite in infinite non-terminating episodes ($\\sum_{k=0}^\\infty \\gamma^k = \\frac{1}{1-\\gamma}$).\n"
            "2. **Uncertainty & Survival**: Models effective survival probability per step. An agent's **effective planning horizon** is $H \\approx \\frac{1}{1-\\gamma}$ steps (e.g. $\\gamma=0.5 \\implies H \\approx 2$, $\\gamma=0.9 \\implies H \\approx 10$, $\\gamma=0.99 \\implies H \\approx 100$)."
        ),
        worked_example=(
            "**Example**: Given rewards $R_1 = -1.0, R_2 = -1.0, R_3 = +20.0$ and $\\gamma = 0.9$:\n"
            "Working backwards:\n"
            "- $G_2 = R_3 = 20.0$\n"
            "- $G_1 = R_2 + \\gamma G_2 = -1.0 + 0.9 \\times 20.0 = 17.0$\n"
            "- $G_0 = R_1 + \\gamma G_1 = -1.0 + 0.9 \\times 17.0 = 14.3$\n\n"
            "Direct formula: $G_0 = -1.0 + (0.9 \\times -1.0) + (0.81 \\times 20.0) = -1.0 - 0.9 + 16.2 = 14.3$."
        ),
        activities=[
            {
                "id": "act_discount_1",
                "prompt": "Calculate discounted return G_0 for rewards R1 = -1.0, R2 = -1.0, R3 = +20.0 with discount factor gamma = 0.9.",
                "type": "numeric",
                "expected_answer": 14.3,
                "tolerance": 0.1,
                "explanation": "G_0 = -1.0 + 0.9(-1.0) + (0.9)^2(20.0) = 14.3.",
                "misconceptions": [
                    {
                        "expected_value": 18.0,
                        "tag": "MISC_BELLMAN_DISCOUNT_OMISSION",
                        "message": "You calculated the undiscounted sum (-1 + -1 + 20 = 18)! Remember to multiply future rewards by gamma at each step.",
                    },
                    {
                        "expected_value": -1.0,
                        "tag": "MISC_REWARD_VS_RETURN",
                        "message": "G_0 is total discounted return over all steps, not just immediate reward R1 (-1.0).",
                    },
                ],
            },
            {
                "id": "act_discount_2",
                "prompt": "If gamma is changed from 0.9 to 0.0 (myopic agent) for reward sequence (-1, -1, +20), what will G_0 become?",
                "type": "choice",
                "options": ["14.3", "-1.0", "0.0", "20.0"],
                "expected_answer": "-1.0",
                "explanation": "When gamma = 0, G_0 = R1 = -1.0. A myopic agent ignores future food and considers only immediate movement cost.",
                "misconceptions": [
                    {
                        "expected_value": "14.3",
                        "tag": "MISC_DISCOUNT_RANGE",
                        "message": "14.3 was computed with gamma = 0.9. With gamma = 0, all future rewards are zeroed out.",
                    }
                ],
            },
            {
                "id": "act_discount_3",
                "prompt": "A survival agent receives rewards R1 = -5, R2 = 0, R3 = +15, R4 = +50 with discount factor gamma = 0.5. Compute G_0.",
                "type": "numeric",
                "expected_answer": 5.0,
                "tolerance": 0.01,
                "explanation": "G3 = 50, G2 = 15 + 0.5(50) = 40, G1 = 0 + 0.5(40) = 20, G0 = -5 + 0.5(20) = 5.0.",
                "misconceptions": [
                    {
                        "expected_value": 60.0,
                        "tag": "MISC_BELLMAN_DISCOUNT_OMISSION",
                        "message": "You omitted discount factor gamma = 0.5!",
                    }
                ],
            },
        ],
        review_variant={
            "prompt": "Retrieval Challenge: How does the choice of discount factor gamma affect the agent's effective planning horizon H?",
            "key_answer": "The effective planning horizon is H ≈ 1 / (1 - gamma). For gamma = 0.5, H ≈ 2 steps. For gamma = 0.9, H ≈ 10 steps. For gamma = 0.99, H ≈ 100 steps.",
        },
    ),
    "mdp": SkillNode(
        id="mdp",
        title="Markov Decision Process (MDP)",
        prerequisites=["discounting"],
        theory=(
            "A formal Markov Decision Process is defined by a 5-tuple $(\\mathcal{S}, \\mathcal{A}, \\mathcal{P}, \\mathcal{R}, \\gamma)$:\n"
            "- $\\mathcal{S}$: Set of all valid states.\n"
            "- $\\mathcal{A}$: Set of all valid actions.\n"
            "- $\\mathcal{P}(s' \\mid s, a) = \\mathbb{P}(S_{t+1} = s' \\mid S_t = s, A_t = a)$: Transition probability matrix.\n"
            "- $\\mathcal{R}(s, a, s') = \\mathbb{E}[R_{t+1} \\mid S_t = s, A_t = a, S_{t+1} = s']$: Reward function.\n"
            "- $\\gamma \\in [0, 1)$: Discount factor.\n\n"
            "**The Markov Property**:\n"
            "A state $S_t$ satisfies the Markov property if transition dynamics depend *strictly* on current state $S_t$ and action $A_t$, independent of historical trajectory $(S_0, A_0, \\dots, S_{t-1})$.\n"
            "*'The present state contains all necessary information to predict the future.'*"
        ),
        worked_example=(
            "**Example**: In GridWorld, taking action RIGHT from state $(0,0)$ transitions to state $(0,1)$ with probability $\\mathcal{P}((0,1) \\mid (0,0), \\text{RIGHT}) = 1.0$, regardless of how state $(0,0)$ was originally reached."
        ),
        activities=[
            {
                "id": "act_mdp_1",
                "prompt": "Does the Markov property dictate that future transition dynamics depend on the entire history of past states?",
                "type": "choice",
                "options": ["Yes", "No"],
                "expected_answer": "No",
                "explanation": "The Markov property dictates that future states depend ONLY on current state S_t and action A_t.",
                "misconceptions": [
                    {
                        "expected_value": "Yes",
                        "tag": "MISC_MARKOV_MEMORY",
                        "message": "The Markov property states that S_t contains all sufficient information to predict S_{t+1}, making past historical trajectories redundant.",
                    }
                ],
            },
            {
                "id": "act_mdp_2",
                "prompt": "Which 5-tuple formally defines a Markov Decision Process?",
                "type": "choice",
                "options": ["(S, A, P, R, gamma)", "(S, A, V, Q, pi)", "(State, Action, Loss, Weights, Optimizer)", "(Episode, Step, Reward, Policy, Error)"],
                "expected_answer": "(S, A, P, R, gamma)",
                "explanation": "MDP is defined by States S, Actions A, Transition probabilities P, Rewards R, and Discount factor gamma.",
                "misconceptions": [],
            },
        ],
        review_variant={
            "prompt": "Retrieval Challenge: State the formal definition of a Markov Decision Process (MDP) and explain what the Markov Property guarantees.",
            "key_answer": "An MDP is a 5-tuple (S, A, P, R, gamma). The Markov Property guarantees that P(S_{t+1}=s' | S_t=s, A_t=a) depends solely on present state s and action a, independent of historical trajectories.",
        },
    ),
    "v-and-q": SkillNode(
        id="v-and-q",
        title="Policies & Value Functions (V and Q)",
        prerequisites=["mdp"],
        theory=(
            "To make decision-making choices without calculating multi-step trajectories from scratch every time, an agent computes **Value Functions** under a behavior strategy called a **Policy** ($\\pi$).\n\n"
            "- **Policy ($\\pi$)**: Strategy mapping states to action probabilities $\\pi(a \\mid s) = \\mathbb{P}(A_t = a \\mid S_t = s)$.\n"
            "- **State-Value Function ($V^\\pi(s)$)**: Expected return starting from state $s$ following policy $\\pi$:\n"
            "  $$V^\\pi(s) = \\mathbb{E}_\\pi \\left[ G_t \\mid S_t = s \\right]$$\n"
            "- **Action-Value Function ($Q^\\pi(s,a)$)**: Expected return starting from state $s$, taking action $a$, then following policy $\\pi$:\n"
            "  $$Q^\\pi(s,a) = \\mathbb{E}_\\pi \\left[ G_t \\mid S_t = s, A_t = a \\right]$$\n\n"
            "**Relationship**:\n"
            "$$V^\\pi(s) = \\sum_{a \\in \\mathcal{A}} \\pi(a \\mid s) Q^\\pi(s,a)$$"
        ),
        worked_example=(
            "**Example**: Given state $S_0$ with Q-values $Q(S_0, a_1) = 10.0$, $Q(S_0, a_2) = 25.0$, $Q(S_0, a_3) = 18.0$:\n"
            "1. Under uniform random policy $\\pi(a_i \\mid S_0) = \\frac{1}{3}$:\n"
            "   $$V^\\pi(S_0) = \\frac{1}{3}(10.0) + \\frac{1}{3}(25.0) + \\frac{1}{3}(18.0) = \\frac{53}{3} \\approx 17.67$$\n"
            "2. Under optimal greedy policy $\\pi^*$:\n"
            "   $$V^*(S_0) = \\max_a Q^*(S_0, a) = 25.0$$"
        ),
        activities=[
            {
                "id": "act_vq_1",
                "prompt": "If an agent in state s has Q-values Q(s, UP) = 1.5, Q(s, RIGHT) = 4.0, Q(s, DOWN) = -2.0, what is max action-value max_a Q(s, a)?",
                "type": "numeric",
                "expected_answer": 4.0,
                "tolerance": 0.01,
                "explanation": "max_a Q(s,a) = max(1.5, 4.0, -2.0) = 4.0.",
                "misconceptions": [
                    {
                        "expected_value": 3.5,
                        "tag": "MISC_V_VS_Q",
                        "message": "You took an average or sum instead of max_a Q(s,a)!",
                    }
                ],
            },
            {
                "id": "act_vq_2",
                "prompt": "Given Q(S0, a1) = 10, Q(S0, a2) = 25, Q(S0, a3) = 18 and a uniform policy pi(a_i|S0) = 1/3, calculate V^pi(S0).",
                "type": "numeric",
                "expected_answer": 17.67,
                "tolerance": 0.05,
                "explanation": "V^pi(S0) = (10 + 25 + 18) / 3 = 17.67.",
                "misconceptions": [
                    {
                        "expected_value": 25.0,
                        "tag": "MISC_BELLMAN_MAX_VS_AVG",
                        "message": "You used max_a Q(s,a) for a uniform policy! max_a is used only for optimal policy V*(s). For policy V^pi, take weighted expectation 17.67.",
                    }
                ],
            },
            {
                "id": "act_vq_3",
                "prompt": "Action A1 yields immediate R = +100 leading to death state V(S_dead) = 0. Action A2 yields immediate R = 0 leading to safe colony V(S_safe) = 200. With gamma = 0.9, which action will optimal policy choose?",
                "type": "choice",
                "options": [
                    "A1 because immediate reward is higher",
                    "A2 because Q*(S, A2) = 180 > Q*(S, A1) = 100",
                    "Both actions are equally valued",
                ],
                "expected_answer": "A2 because Q*(S, A2) = 180 > Q*(S, A1) = 100",
                "explanation": "Q*(S, A1) = 100 + 0.9(0) = 100. Q*(S, A2) = 0 + 0.9(200) = 180. Optimal policy selects A2 for higher total return.",
                "misconceptions": [
                    {
                        "expected_value": "A1 because immediate reward is higher",
                        "tag": "MISC_REWARD_VS_RETURN",
                        "message": "Greedy immediate selection ignores fatal future state V(S_dead)=0!",
                    }
                ],
            },
        ],
        review_variant={
            "prompt": "Retrieval Challenge: Explain the fundamental difference between State-Value V^pi(s) and Action-Value Q^pi(s,a).",
            "key_answer": "V^pi(s) is the expected return starting from state s and following policy pi. Q^pi(s,a) is the expected return starting from state s, taking action a specifically, and thereafter following policy pi. V^pi(s) = sum_a pi(a|s) Q^pi(s,a).",
        },
    ),
    "bellman-backup": SkillNode(
        id="bellman-backup",
        title="Bellman Equations & Value Backups",
        prerequisites=["v-and-q"],
        theory=(
            "The **Bellman Equation** decomposes value into immediate reward plus discounted expected future value.\n\n"
            "- **Bellman Expectation Equation for $V^\\pi(s)$**:\n"
            "  $$V^\\pi(s) = \\sum_{a \\in \\mathcal{A}} \\pi(a \\mid s) \\sum_{s' \\in \\mathcal{S}} \\mathcal{P}(s' \\mid s, a) \\left[ \\mathcal{R}(s,a,s') + \\gamma V^\\pi(s') \\right]$$\n\n"
            "- **Bellman Optimality Equation for $Q^*(s,a)$**:\n"
            "  $$Q^*(s,a) = \\sum_{s' \\in \\mathcal{S}} \\mathcal{P}(s' \\mid s, a) \\left[ \\mathcal{R}(s,a,s') + \\gamma \\max_{a' \\in \\mathcal{A}} Q^*(s', a') \\right]$$\n\n"
            "Notice: Bellman Expectation averages over policy actions ($\\sum_a \\pi(a|s)$), while Bellman Optimality takes maximum over actions ($\\max_a$)."
        ),
        worked_example=(
            "**Example**: State $S_0 = \\text{Cave Entrance}$, $\\gamma = 0.9$.\n"
            "Actions: $a_1 = \\text{REST}$ ($100\\%$ stay in $S_0, R = +1.0, V(S_0) = 10.0$), $a_2 = \\text{VENTURE}$ ($70\\%$ reach $S_1, R = +15.0, V(S_1) = 30.0$; $30\\%$ reach $S_2, R = -10.0, V(S_2) = 2.0$).\n\n"
            "1. $Q(S_0, a_1) = 1.0 + 0.9(10.0) = 10.0$\n"
            "2. $Q(S_0, a_2) = 0.7[15 + 0.9(30)] + 0.3[-10 + 0.9(2)] = 0.7(42) + 0.3(-8.2) = 29.4 - 2.46 = 26.94$\n"
            "3. Bellman Expectation for $\\pi(a_1)=0.4, \\pi(a_2)=0.6$: $V^\\pi(S_0) = 0.4(10.0) + 0.6(26.94) = 20.164$\n"
            "4. Bellman Optimality $V^*(S_0) = \\max(10.0, 26.94) = 26.94$"
        ),
        activities=[
            {
                "id": "act_bellman_1",
                "prompt": "Calculate the Bellman target value for immediate reward r = -0.1, discount gamma = 0.9, and next state max Q-value max_a' Q(s', a') = 10.0.",
                "type": "numeric",
                "expected_answer": 8.9,
                "tolerance": 0.01,
                "explanation": "Target = -0.1 + 0.9 * 10.0 = 8.9.",
                "misconceptions": [
                    {
                        "expected_value": 9.9,
                        "tag": "MISC_BELLMAN_DISCOUNT_OMISSION",
                        "message": "You omitted discount gamma = 0.9! Target is -0.1 + 0.9*(10) = 8.9.",
                    }
                ],
            },
            {
                "id": "act_bellman_2",
                "prompt": "State S = Bush, gamma = 0.5. Action a2 transitions 50% to S' (R = 4, V(S') = 20) and 50% to S'' (R = -2, V(S'') = 0). Calculate Q(S, a2).",
                "type": "numeric",
                "expected_answer": 6.0,
                "tolerance": 0.01,
                "explanation": "Q(S, a2) = 0.5[4 + 0.5(20)] + 0.5[-2 + 0.5(0)] = 0.5[14] + 0.5[-2] = 7.0 - 1.0 = 6.0.",
                "misconceptions": [
                    {
                        "expected_value": 12.0,
                        "tag": "MISC_TRANSITION_PROB_SUM",
                        "message": "You calculated only one branch transition instead of summing weighted expectations over all transition outcomes.",
                    }
                ],
            },
        ],
        review_variant={
            "prompt": "Retrieval Challenge: How does the Bellman Optimality Equation for Q*(s,a) lay the exact foundation for the tabular Q-Learning algorithm?",
            "key_answer": "The Bellman Optimality equation Q*(s,a) = E[R + gamma * max_{a'} Q*(s', a')] defines the exact target value. Q-Learning uses sample transitions (s, a, r, s') to incrementally update Q(s,a) toward this target without requiring a known environment transition model P(s'|s,a).",
        },
    ),
    "td-q-learning": SkillNode(
        id="td-q-learning",
        title="Temporal Difference & Q-Learning",
        prerequisites=["bellman-backup"],
        theory=(
            "Temporal Difference (TD) learning allows an agent to learn directly from online sample experience $(S_t, A_t, R_{t+1}, S_{t+1})$ without waiting for episode termination or knowing transition dynamics $\\mathcal{P}(s'|s,a)$.\n\n"
            "**1-Step TD Error ($\\delta_t$)**:\n"
            "$$\\delta_t = \\underbrace{R_{t+1} + \\gamma \\max_{a'} Q(S_{t+1}, a')}_{\\text{Q-Learning Target}} - Q(S_t, A_t)$$\n\n"
            "**Q-Learning Update Rule (Off-Policy)**:\n"
            "$$Q(S_t, A_t) \\leftarrow Q(S_t, A_t) + \\alpha \\delta_t$$\n\n"
            "**SARSA Update Rule (On-Policy)**:\n"
            "$$Q(S_t, A_t) \\leftarrow Q(S_t, A_t) + \\alpha \\left[ R_{t+1} + \\gamma Q(S_{t+1}, A_{t+1}) - Q(S_t, A_t) \\right]$$\n\n"
            "Key Difference: Q-Learning evaluates optimal potential ($\\max_{a'} Q$) off-policy, whereas SARSA evaluates active exploratory actions ($A_{t+1}$) on-policy."
        ),
        worked_example=(
            "**Example 1: TD Value Update**:\n"
            "$V(S_{\\text{hill}}) = 12.0, V(S_{\\text{river}}) = 25.0, \\alpha = 0.1, \\gamma = 0.9, R = +3.0$\n"
            "$\\text{Target} = 3.0 + 0.9(25.0) = 25.5$\n"
            "$\\delta_t = 25.5 - 12.0 = +13.5$\n"
            "$V(S_{\\text{hill}}) \\leftarrow 12.0 + 0.1(13.5) = 13.35$\n\n"
            "**Example 2: Q-Learning Update**:\n"
            "$Q_{old}(S_1, \\text{DIG}) = 4.0, \\max_{a'} Q(S_2, a') = 15.0, R = +6.0, \\alpha = 0.25, \\gamma = 0.8$\n"
            "$\\text{Target} = 6.0 + 0.8(15.0) = 18.0$\n"
            "$\\delta_t = 18.0 - 4.0 = 14.0$\n"
            "$Q_{new}(S_1, \\text{DIG}) = 4.0 + 0.25(14.0) = 7.5$"
        ),
        activities=[
            {
                "id": "act_td_1",
                "prompt": "Given Q_old(s,a) = 2.0, learning rate alpha = 0.2, and Target = 7.0, calculate Q_new(s,a).",
                "type": "numeric",
                "expected_answer": 3.0,
                "tolerance": 0.01,
                "explanation": "TD Error = 7.0 - 2.0 = 5.0. Q_new = 2.0 + 0.2 * 5.0 = 3.0.",
                "misconceptions": [
                    {
                        "expected_value": 7.0,
                        "tag": "MISC_ALPHA_OVERFLOW",
                        "message": "You set Q_new equal to Target directly! When alpha < 1.0, Q_new blends Old Q and Target.",
                    }
                ],
            },
            {
                "id": "act_td_2",
                "prompt": "Given V(S1) = 50.0, V(S2) = 20.0, learning rate alpha = 0.2, discount factor gamma = 0.8. Transition S1 -> R = -5.0 -> S2. Compute new V(S1).",
                "type": "numeric",
                "expected_answer": 42.2,
                "tolerance": 0.01,
                "explanation": "Target = -5.0 + 0.8(20) = 11.0. TD Error = 11.0 - 50.0 = -39.0. V_new = 50.0 + 0.2(-39.0) = 42.2.",
                "misconceptions": [
                    {
                        "expected_value": 11.0,
                        "tag": "MISC_ALPHA_OVERFLOW",
                        "message": "11.0 is the TD Target, not the updated value V_new! Apply alpha * TD Error to V_old.",
                    }
                ],
            },
            {
                "id": "act_td_3",
                "prompt": "Q(SA, a1) = 10.0, Q(SB, b1) = 5.0, Q(SB, b2) = 30.0. Parameters alpha = 0.5, gamma = 0.9. Transition (SA, a1) -> R = +2.0 -> SB. Compute new Q(SA, a1).",
                "type": "numeric",
                "expected_answer": 19.5,
                "tolerance": 0.01,
                "explanation": "max_a' Q(SB, a') = 30.0. Target = 2.0 + 0.9(30.0) = 29.0. TD Error = 29.0 - 10.0 = 19.0. Q_new = 10.0 + 0.5(19.0) = 19.5.",
                "misconceptions": [
                    {
                        "expected_value": 29.0,
                        "tag": "MISC_ALPHA_OVERFLOW",
                        "message": "29.0 is the Q-Learning Target! New Q value is 10.0 + 0.5(29.0 - 10.0) = 19.5.",
                    }
                ],
            },
            {
                "id": "act_td_4",
                "prompt": "If learning rate alpha = 1.0 and gamma = 0.0, what does the Q-Learning update rule reduce to?",
                "type": "choice",
                "options": [
                    "Q(S_t, A_t) <- R_{t+1}",
                    "Q(S_t, A_t) <- Q(S_t, A_t)",
                    "Q(S_t, A_t) <- max_a' Q(S_{t+1}, a')",
                ],
                "expected_answer": "Q(S_t, A_t) <- R_{t+1}",
                "explanation": "With alpha = 1 and gamma = 0, Q(S_t, A_t) <- Q + 1.0 * [R_{t+1} + 0 - Q] = R_{t+1}.",
                "misconceptions": [],
            },
        ],
        review_variant={
            "prompt": "Retrieval Challenge: Explain why Q-Learning can re-use old historical transitions logged in an experience replay buffer, whereas standard SARSA cannot.",
            "key_answer": "Q-Learning is off-policy: its target r + gamma * max_{a'} Q(s', a') depends only on state transitions and rewards, not on which policy generated the historical action a'. SARSA's target requires Q(s', A_{t+1}), where A_{t+1} was chosen by the specific policy active at that past step, making uncorrected historical buffer replay invalid.",
        },
        lab_rl_enabled=True,
    ),
}


def get_curriculum_state(db_path: Optional[str] = None) -> List[Dict[str, Any]]:
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
    db_path: Optional[str] = None,
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
    misconception_tag = None
    diagnostic_message = None

    if act_type == "numeric":
        try:
            val = float(given_answer)
            tol = activity_dict.get("tolerance", 0.01)
            is_correct = abs(val - float(expected)) <= tol
        except (ValueError, TypeError):
            is_correct = False
    else:  # choice / text
        is_correct = str(given_answer).strip().lower() == str(expected).strip().lower()

    if not is_correct:
        for rule in activity_dict.get("misconceptions", []):
            rule_exp = rule.get("expected_value")
            if act_type == "numeric":
                try:
                    given_val = float(given_answer)
                    if abs(given_val - float(rule_exp)) <= activity_dict.get("tolerance", 0.05):
                        misconception_tag = rule.get("tag")
                        diagnostic_message = rule.get("message")
                        break
                except (ValueError, TypeError):
                    pass
            else:
                if str(given_answer).strip().lower() == str(rule_exp).strip().lower():
                    misconception_tag = rule.get("tag")
                    diagnostic_message = rule.get("message")
                    break

    if is_correct:
        feedback = "Correct! " + explanation
    else:
        if misconception_tag and diagnostic_message:
            feedback = f"Incorrect. ⚠️ Misconception Detected [{misconception_tag}]: {diagnostic_message} {explanation}"
        else:
            feedback = "Incorrect. " + explanation

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
        "misconception_tag": misconception_tag,
        "unlocked_next": get_curriculum_state(db_path),
    }
