# Reinforcement Learning Foundations: Autonomous-Agent Pack

## Overview

Welcome to the **Foundational Autonomous-Agent RL Content Pack**! This learning pack provides a rigorous, pedagogical, and practical introduction to Reinforcement Learning (RL) designed specifically for autonomous agents operating in dynamic, uncertain environments.

This content pack is completely isolated from portal application code and runtime logic, making it portable for ingestion into the Learning Portal database, LMS platforms, or standalone study.

---

## Pedagogical Design

In accordance with the **Learning Portal Methodology** ([`docs/learning-portal/02-learning-model.md`](../../02-learning-model.md)), every skill module follows a standardized 9-step experiential progression:

1. **Intuition** — Real-world survival motivation (e.g., managing hunger, avoiding threats, searching for food).
2. **Theory** — Formal mathematical definitions, variables, and structural equations.
3. **Worked Example** — Step-by-step arithmetic walk-through on small discrete states.
4. **Manual / Guided Exercise** — Fill-in-the-blank step calculations for the learner.
5. **Prediction** — Active hypothesis testing before running numerical updates.
6. **Guided Experiment** — Parameter tweaking ($\gamma, \alpha, \epsilon$) and behavioral observation.
7. **Independent Checkpoint** — Unassisted problem solving with deterministic evaluation specs.
8. **Misconceptions** — Common learning traps tagged with machine-readable codes (`MISC_*`).
9. **Review Variant** — Retrieval practice tasks for retention and transfer.

---

## Learning Path & Skill Graph Mapping

This pack fulfills the **Value-Based RL Foundations** node in the Skill Graph ([`docs/learning-portal/03-skill-graph.md`](../../03-skill-graph.md)) and serves as the direct prerequisite for Deep Q-Networks (DQN) and Autonomous Decision Systems.

```text
Sequential Decision Concepts ──┐
                               ├──> RL Foundations ──> Value-Based Control ──> Deep Q-Networks (DQN)
Probability & Expected Value ──┘
```

---

## Content Index

| Module File | Core Topics Covered | Key Survival Agent Scenarios |
| :--- | :--- | :--- |
| **[`sources-and-licenses.md`](sources-and-licenses.md)** | Source matrix, license verification, copyright compliance rules | N/A |
| **[`01-agent-environment-and-mdp.md`](01-agent-environment-and-mdp.md)** | RL Vocabulary, Reward vs Return, Discount Factor ($\gamma$), Markov Property, MDP (5-tuple), State vs Observation | Hunger vs Food Foraging, Threat Evasion, Partial Visibility |
| **[`02-policies-and-value-functions.md`](02-policies-and-value-functions.md)** | Policy ($\pi$), State-Value $V(s)$, Action-Value $Q(s,a)$, Bellman Expectation & Optimality Equations, One Bellman Backup | Shelter Navigation, High-Risk vs Safe Resource Paths |
| **[`03-temporal-difference-and-control.md`](03-temporal-difference-and-control.md)** | Model-Free TD, TD Target & Error ($\delta_t$), Exploration vs Exploitation, $\epsilon$-Greedy Policy, Q-Learning, SARSA vs Q-Learning, DQN Bridge | Dangerous Shortcut Evasion, Safe vs Optimal Survival Policies |
| **[`04-worked-examples-and-checkpoints.md`](04-worked-examples-and-checkpoints.md)** | Comprehensive numerical calculations & independent checkpoints for Return, Bellman Backup, TD Update, Q-Update | Multi-step Trajectories, 2-State Survival MDPs |
| **[`05-misconceptions-and-evaluator-spec.md`](05-misconceptions-and-evaluator-spec.md)** | Machine-readable misconception taxonomy (`MISC_*`), diagnostic feedback rules, portal evaluator specs | Automated grading specs for all exercises |

---

## Core Hands-On Mastery Criteria

To achieve mastery of this content pack, the learner must be able to perform:

1. **Discounted Return Calculation**: Compute $G_0 = \sum_{t=0}^T \gamma^t R_{t+1}$ given a sequence of rewards.
2. **One Bellman Backup**: Calculate $V(s)$ or $Q(s,a)$ from transition probabilities and successor state values.
3. **One TD Update**: Update state value $V(s) \leftarrow V(s) + \alpha [R + \gamma V(s') - V(s)]$.
4. **One Q-Learning Update**: Update action value $Q(s,a) \leftarrow Q(s,a) + \alpha [R + \gamma \max_{a'} Q(s',a') - Q(s,a)]$.

---

## Quality & Licensing Guarantee

- **100% Original Explanations**: All prose, worked calculations, and survival examples are original works.
- **Source Verification**: All theoretical references are explicitly recorded in [`sources-and-licenses.md`](sources-and-licenses.md).
- **DQN Readiness**: Math notation and state/action value representations directly map to PyTorch neural network function approximation in subsequent modules.
