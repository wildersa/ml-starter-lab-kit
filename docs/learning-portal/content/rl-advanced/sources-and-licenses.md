# Sources and Licensing Matrix

This document tracks all theoretical references, academic papers, books, and open educational materials used as foundations for the **Deep RL to Autonomous Agent** learning pack.

In accordance with the repository's content licensing policy (`docs/learning-portal/05-content-sources-and-licensing.md`):
1. All prose, explanations, diagrams, mathematical expositions, pseudocode, and exercises are **100% original creations** written specifically for this project.
2. Proprietary or copyrighted texts, figures, and code samples are **never copied or reproduced**.
3. Theoretical frameworks, landmark algorithms, and formal definitions are formally cited to credit original authors and publishers.

---

## Content Provenance & Licensing Matrix

| Topic / Concept | Source Title & Authors | Publisher / Venue (Year) | License / Access Terms | Adaptation Policy & Usage |
| :--- | :--- | :--- | :--- | :--- |
| **RL Foundations & Value Functions** | *Reinforcement Learning: An Introduction*<br>Richard S. Sutton, Andrew G. Barto | MIT Press (2018, 2nd Ed.) | Freely accessible online for personal study; Copyright MIT Press. | **Reference Only**. Cited for mathematical notation ($\gamma$, $G_t$, Bellman updates) and conceptual sequencing. All prose, diagrams, and code are original. |
| **Deep Q-Networks (DQN)** | *Human-level control through deep reinforcement learning*<br>Volodymyr Mnih et al. | *Nature* 518, 529–533 (2015) | Peer-reviewed journal article (Copyright Nature Publishing Group). | **Reference Only**. Cited for algorithm design (Replay Buffer, Target Network, Q-loss). Original mathematical formulation and step-by-step exposition. |
| **Double DQN** | *Deep Reinforcement Learning with Double Q-learning*<br>Hado van Hasselt, Arthur Guez, David Silver | AAAI Conference on Artificial Intelligence (2016) | Open access paper (arXiv:1509.06461). | **Reference Only**. Cited for overestimation bias analysis and decoupled action-selection/evaluation target equation. |
| **Policy Gradients & REINFORCE** | *Policy Gradient Methods for Reinforcement Learning with Function Approximation*<br>R. S. Sutton et al. | NeurIPS (1999) | Open access conference paper. | **Reference Only**. Cited for the Policy Gradient Theorem and score function ($\nabla_\theta \log \pi_\theta(a\vert s)$) derivation. |
| **Actor-Critic & Advantage** | *Asynchronous Methods for Deep Reinforcement Learning*<br>Volodymyr Mnih et al. | ICML (2016) | Open access paper (arXiv:1602.01783). | **Reference Only**. Cited for Advantage estimation $A(s,a) = Q(s,a) - V(s)$ and shared network architecture. |
| **Proximal Policy Optimization (PPO)** | *Proximal Policy Optimization Algorithms*<br>John Schulman et al. | OpenAI Technical Report (2017) | Open access paper (arXiv:1707.06347). | **Reference Only**. Cited for Clipped Surrogate Objective formulation and trust-region intuition. |
| **POMDPs & Belief States** | *Planning and acting in partially observable stochastic domains*<br>Leslie P. Kaelbling, Michael L. Littman, Anthony R. Cassandra | *Artificial Intelligence* 101(1-2) (1998) | Peer-reviewed journal article. | **Reference Only**. Cited for 7-tuple POMDP definition $(S, A, T, R, \Omega, O, \gamma)$ and Bayesian belief updates. |
| **Options & Hierarchical RL** | *Between MDPs and semi-MDPs: A framework for temporal abstraction in reinforcement learning*<br>R. S. Sutton, D. Precup, S. Singh | *Artificial Intelligence* 112(1-2) (1999) | Peer-reviewed journal article. | **Reference Only**. Cited for Options tuple $o = (\mathcal{I}, \pi, \beta)$ and Semi-MDP formulation. |
| **Monte Carlo Tree Search (MCTS)** | *A Survey of Monte Carlo Tree Search Methods*<br>Cameron Browne et al. | *IEEE Transactions on Computational Intelligence and AI in Games* (2012) | Peer-reviewed journal article. | **Reference Only**. Cited for the 4 MCTS phases (Selection, Expansion, Simulation, Backpropagation) and UCT rule. |
| **Behavior Trees in Robotics** | *Behavior Trees in Robotics and AI: An Introduction*<br>Michele Colledanchise, Petter Ögren | CRC Press / Taylor & Francis (2018) | Open access draft / Published book. | **Reference Only**. Cited for node types (Sequence, Selector, Action, Condition) and execution semantics. |
| **Deep Learning Foundations** | *Dive into Deep Learning (D2L)*<br>Aston Zhang, Zack C. Lipton, Mu Li, Alexander J. Smola | Cambridge University Press / d2l.ai | `CC BY-SA 4.0` (Text/Content), MIT (Code) | **Open Material Reference**. Content structure and neural network intuition cross-referenced with `CC BY-SA 4.0` compatibility. |

---

## Verification & Compliance Checklist

- [x] No proprietary prose, code, or figures copied verbatim from external sources.
- [x] Academic credits explicitly cited for foundational formulas and algorithmic components.
- [x] Educational materials derived independently using original code, ASCII architecture diagrams, and custom worked examples.
- [x] Materials are fully portable and ready for integration into the Learning Portal platform.
