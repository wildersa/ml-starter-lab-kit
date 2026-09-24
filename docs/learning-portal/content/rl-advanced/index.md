# Deep RL to Autonomous Agent Advanced Learning Pack

## Overview

Welcome to the **Deep RL to Autonomous Agent** learning pack. This curriculum transitions from tabular Reinforcement Learning (Q-learning) to neural function approximation, policy optimization, temporal abstraction, and layered autonomous agent architectures.

Rather than presenting Reinforcement Learning as a standalone black-box controller expected to handle everything from raw sensor readings to long-term task execution, this pack emphasizes **separation of responsibilities**. You will learn where learned policies excel, where symbolic planners and Behavior Trees are required, and how to combine them into robust, production-grade autonomous agent systems.

---

## Pedagogical Structure

The pack follows an explicit step-by-step progression:

1. **Tabular-to-Neural Bridge**: Demonstrating how discrete lookup tables $Q[s, a]$ transition into continuous parameterised function approximators $Q(s, a; \theta)$.
2. **Incremental Stability**: Adding Replay Buffers, Minibatches, Target Networks, and Double Q-learning one mechanism at a time to explain *why* each is necessary for convergence.
3. **Policy-First & Actor-Critic Foundations**: Moving beyond value estimation to direct policy search (REINFORCE), advantage estimation ($A(s,a) = Q(s,a) - V(s)$), and trust-region optimization (PPO).
4. **Partial Observability, Credit, & Planning**: Addressing real-world constraints such as unobservable state (POMDPs, belief states), delayed credit assignment ($n$-step returns, $\text{TD}(\lambda)$), and model-based rollouts (MCTS).
5. **Hierarchical RL & Agent Architecture**: Structuring decisions across temporal scales using Options/Semi-MDPs, Behavior Trees, and a 6-layer agent architecture (**Perception -> Needs -> Goal -> Decision/Planning -> Behavior -> Action**).
6. **Diagnostics & Hands-On Verification**: Clearing common misconceptions and guiding framework-free Python/NumPy implementations.
7. **End-to-End Transfer Exercise**: Applying the full 6-layer architecture to a concrete autonomous domain.

---

## Content Pack Navigation

| Module | Title | Primary Learning Objectives |
| :--- | :--- | :--- |
| **01** | [`01-dqn-foundations.md`](01-dqn-foundations.md) | Neural function approximation, Replay Buffer, Minibatches, Target Network, $\epsilon$-greedy, Double DQN intuition. |
| **02** | [`02-policy-gradients-and-actor-critic.md`](02-policy-gradients-and-actor-critic.md) | Policy gradient family, REINFORCE, Actor-Critic, Advantage function, PPO surrogate objective. |
| **03** | [`03-pomdp-credit-assignment-planning.md`](03-pomdp-credit-assignment-planning.md) | POMDPs (observation vs state vs belief), delayed rewards ($n$-step, $\text{TD}(\lambda)$), model-free vs model-based, rollouts & MCTS. |
| **04** | [`04-hierarchical-rl-and-agent-architectures.md`](04-hierarchical-rl-and-agent-architectures.md) | Options / SMDP framework, Behavior Trees vs Planners vs Learned Policies, Layered Agent Architecture. |
| **05** | [`05-misconceptions-and-experiments.md`](05-misconceptions-and-experiments.md) | Common deep RL failure modes, framework-free NumPy checkpoints, architectural diagnostic exercises. |
| **06** | [`06-transfer-exercise.md`](06-transfer-exercise.md) | Comprehensive transfer exercise mapping autonomous system mechanics to the 6-layer pipeline. |
| **Matrix** | [`sources-and-licenses.md`](sources-and-licenses.md) | Provenance, academic citations, licensing terms, and adaptation guidelines. |

---

## Prerequisites

Before starting this pack, learners should be comfortable with:
- Foundational RL concepts: MDPs, Bellman Expectation & Optimality equations, tabular Q-learning (`docs/learning-portal/04-curriculum.md`).
- Neural Network basics: Linear layers, activation functions, loss functions, backpropagation (`docs/learning-portal/04-curriculum.md`).
- Basic Python and NumPy vector operations.

---

## Sources & Licensing

All content in this pack is written originally for the Learning Portal, drawing theoretical grounding from foundational texts (Sutton & Barto 2018) and seminal research papers (Mnih et al. 2015, Schulman et al. 2017, Kaelbling et al. 1998, Sutton et al. 1999).

For full details on academic citations, original authorship, and licensing compliance, see [`sources-and-licenses.md`](sources-and-licenses.md).
