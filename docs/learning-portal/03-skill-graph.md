# Skill graph

## Why a graph instead of a linear course

Machine Learning knowledge is not a single sequence. Multiple prerequisite chains converge into later skills.

Examples:

- DQN depends on both value-based RL and neural networks.
- XGBoost depends on supervised learning fundamentals and tree-based models.
- model monitoring depends on metrics, data quality, experimentation, and deployment concepts.

Therefore the progression model should be a **directed acyclic graph (DAG)** of competencies rather than a single curriculum list or strict tree.

## Skill node

Each node represents a demonstrable competency, not merely a chapter.

A skill should define at least:

- id;
- title;
- short purpose;
- prerequisites;
- concepts covered;
- learning activities;
- checkpoint criteria;
- mastery threshold;
- unlocks;
- references;
- common misconceptions;
- optional transfer exercise.

## Dependency behavior

A skill becomes available when its required prerequisite conditions are met.

Dependencies may support different rules:

- all prerequisites required;
- one of a set of prerequisites required;
- recommended but non-blocking prerequisite;
- mastery threshold greater than simple completion.

The initial implementation should prefer simple explicit dependencies before adding complex rule expressions.

## Example convergence

```text
Probability basics ───────────────┐
                                 ├─> RL foundations
Sequential decision concepts ────┘

RL foundations
  -> Return and discounting
  -> Markov property
  -> MDP
  -> Value functions
  -> Bellman equations
  -> Dynamic Programming
  -> Monte Carlo
  -> Temporal Difference
  -> SARSA / Q-Learning

Neural Networks ──────────────────┐
                                 ├─> DQN
Q-Learning ───────────────────────┘
```

## Progress vs mastery vs gamification

These must remain separate.

### Progress

How much of the learning activity has been completed.

### Mastery

How strongly the learner has demonstrated the competency.

### XP

A motivational score. XP must never be the authority for prerequisite unlocking when mastery is required.

Example:

```text
Q-Learning
Progress: 100%
Mastery: 78%
XP: 480
Status: acquired
```

## Skill acquisition

A learner should receive a visible skill when reaching the defined checkpoint threshold.

Examples:

- Dataset Explorer
- Confusion Matrix
- Classification Metrics
- K-Means Foundations
- Bellman Solver
- Q-Learning Foundations
- Experiment Tracking

Names should describe actual competence rather than arbitrary levels.

## Branch achievements

Completing a meaningful subgraph may award a larger achievement or specialization.

Examples:

- Data Foundations
- Classical ML Foundations
- Supervised Learning Practitioner
- Unsupervised Learning Foundations
- Value-Based RL Foundations
- Deep Learning Foundations
- MLOps Foundations

## Visual graph behavior

The portal should eventually show:

- acquired nodes;
- available nodes;
- locked nodes;
- prerequisite edges;
- recommended next nodes;
- weak nodes needing review;
- current learning path;
- alternative branches.

The graph should explain why a node is locked instead of merely disabling it.

Example:

> DQN is locked because `Q-Learning` and `Neural Networks` are not both acquired.

## Review can affect mastery

Mastery should not necessarily be permanent after one successful attempt.

A learner may retain the skill badge while the node moves to `needs review` if later retrieval checks reveal weakness.

This allows the portal to distinguish:

- exposure;
- successful completion;
- retained understanding.

## Graph authoring rule

Do not create a graph edge only because two topics are adjacent in a textbook. Add a prerequisite when the later skill actually depends on the earlier competency.