# Sources and Licenses Matrix — RL Foundations Content Pack

## Overview

This content pack provides original, learner-facing educational materials for reinforcement learning (RL) tailored to autonomous agents. In accordance with the project's content policy defined in [`docs/learning-portal/05-content-sources-and-licensing.md`](../../05-content-sources-and-licensing.md), all explanations, math derivations, worked examples, interactive predictions, exercises, and misconception tags in this pack are original works.

External textbooks, courses, and scientific papers were consulted as authoritative theoretical references. No prose, diagrams, proprietary exercises, or copyrighted code from restricted sources were copied or directly reproduced.

---

## Source and License Matrix

| Source Name | Author / Publisher | Official URL | License / Terms | Permitted Reuse | How Applied in Content Pack |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Reinforcement Learning: An Introduction (2nd Ed., 2018)** | Richard S. Sutton & Andrew G. Barto / MIT Press | [IncompleteIdeas Site](http://incompleteideas.net/book/the-book-2nd.html) | Copyrighted (MIT Press). PDF freely viewable for personal use. | Theoretical reference only. No adaptation of text or figures. | Primary source for canonical RL notation ($s, a, r, s', \gamma, \alpha, \epsilon$), MDP formalization, Bellman expectation/optimality equations, TD error definition, and SARSA vs. Q-Learning theoretical distinctions. |
| **OpenAI Spinning Up in Deep RL** | Joshua Achiam / OpenAI | [Spinning Up Docs](https://spinningup.openai.com/) | MIT License | Full reuse, modification, and adaptation permitted with attribution. | Reference for clear intuitive definitions of trajectory, return, value functions, policy types, and transition into deep RL. |
| **Dive into Deep Learning (D2L.ai)** | Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola | [D2L Web](https://d2l.ai/) / [GitHub](https://github.com/d2l-ai/d2l-en) | Text: CC BY-SA 4.0; Code: Apache 2.0 | Text adaptation allowed with CC BY-SA 4.0 attribution; Code allowed under Apache 2.0. | Reference for pedagogical structuring of MDPs, discount factor intuition, and value function backup visualizations. |
| **Hugging Face Deep RL Course** | Thomas Simonini et al. / Hugging Face | [HF Learn](https://huggingface.co/learn/deep-rl-course) / [GitHub](https://github.com/huggingface/deep-rl-class) | Apache License 2.0 | Full reuse, modification, and adaptation permitted with attribution. | Reference for hands-on tabular Q-Learning workflow, exploration/exploitation decay curves, and student misconception taxonomy. |
| **UCL Course on RL (2015)** | David Silver / University College London | [UCL Course Site](https://www.davidsilver.uk/teaching/) | CC BY-NC 4.0 | Theoretical reference for educational non-commercial concepts. | Reference for the sequence of value prediction (Bellman expectation) to control (Bellman optimality) and model-free TD updates. |
| **Gymnasium (Farama Foundation)** | Farama Foundation | [Gymnasium Docs](https://gymnasium.farama.org/) | MIT License | Permissive open source. | Reference for standard environment step interface conventions `(observation, reward, terminated, truncated, info)`. |
| **Dynamic Programming (1957)** | Richard Bellman / Princeton University Press | Scientific Literature | Public domain mathematical equations. | Standard mathematical formulations. | Source of the Bellman Equation for Markov decision processes. |
| **Learning from Delayed Rewards (1989) / Q-Learning (1992)** | Christopher J. C. H. Watkins & Peter Dayan | Ph.D. Thesis / Machine Learning Journal | Scientific Literature | Standard mathematical formulations and algorithms. | Source of the Q-Learning algorithm and convergence properties. |

---

## Copyright Compliance and Originality Declaration

1. **No Reproduction of Protected Material**: Neither the textbook text of Sutton & Barto (2018) nor figures/diagrams from copyrighted publishers were copied.
2. **Original Survival-Agent Examples**: All worked examples (hunger/food foraging, threat evasion, stamina management, shelter discovery) were created independently for this pack.
3. **Consistent Mathematical Notation**: Notation follows standard academic conventions:
   - State space $S$, Action space $A$, Reward function $R(s,a,s')$, Transition dynamics $P(s' \mid s, a)$, Discount factor $\gamma \in [0, 1)$.
   - Return $G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}$.
   - State-value function $V^\pi(s)$ and Action-value function $Q^\pi(s,a)$.
   - Temporal Difference error $\delta_t = R_{t+1} + \gamma Q(S_{t+1}, A_{t+1}) - Q(S_t, A_t)$.
4. **Provenance Metadata**: Every skill document includes explicit source attribution metadata headers for ingestion into the Learning Portal database.
