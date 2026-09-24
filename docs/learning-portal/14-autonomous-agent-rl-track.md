# Autonomous-agent Reinforcement Learning track

**Status:** focused content plan / reference vertical slice  
**Audience:** learner who wants RL competence for designing autonomous agents  
**Product role:** specialization inside the Learning Portal Skill Graph, not a separate course engine  
**Implementation role:** preferred proving track for the first end-to-end Portal + Lab Runtime slice once platform stages permit implementation

## Why this track exists

The general Machine Learning curriculum must remain broader than Reinforcement Learning. However, RL is a particularly useful proving ground for the Learning Portal because it exercises almost every adopted learning capability:

- prerequisite-aware skill progression;
- manual calculations before library abstraction;
- state/action/reward visualizations;
- prediction before execution;
- code execution;
- deterministic and invariant-based evaluation;
- repeated experiments with changed parameters;
- mastery evidence and unlocks;
- delayed review;
- transfer from toy environments to a real agent architecture.

The motivating transfer context is an autonomous survival-game agent with a cognitive pipeline like:

```text
PERCEPTION
  ↓
SURVIVAL / NEEDS
  ↓
GOAL SELECTION
  ↓
DECISION / PLANNING
  ↓
BEHAVIOR
  ↓
ACTION / EXECUTION
```

The Portal must teach the algorithms without pretending that one RL method is the architecture of the whole agent. RL, planning, POMDP formulations, Behavior Trees, options/skills and other mechanisms may fill different responsibilities.

## Core pedagogical rule

The learner should encounter a technique because the previous environment exposes a limitation that the next technique addresses.

The preferred progression is therefore not:

```text
algorithm 1
algorithm 2
algorithm 3
...
```

It is:

```text
small decision problem
  ↓ limitation appears
new concept explains the limitation
  ↓
manual mechanism
  ↓
guided experiment
  ↓
implementation
  ↓
larger decision problem
```

A single evolving family of small survival environments should be reused across the track so that the learner sees why complexity is being added.

## Skill Graph

### A. Sequential-decision foundations

```text
Probability intuition
      +
Functions / basic algebra intuition
      ↓
Sequential decision vocabulary
      ↓
Reward vs return
      ↓
Discounting
      ↓
Markov property
      ↓
MDP
      ↓
Policy
      ↓
V(s) and Q(s,a)
```

Demonstrable competencies include:

- identify agent, environment, state/observation, action, reward and episode in a scenario;
- distinguish immediate reward from return;
- compute a short discounted return by hand;
- explain what the Markov assumption means operationally;
- distinguish a policy from a value function;
- read and interpret a small (V) or (Q) representation.

### B. Bellman and dynamic programming

```text
V / Q
  ↓
Bellman expectation
  ↓
one Bellman backup
  ↓
Bellman optimality
  ↓
policy evaluation
  ↓
policy improvement
  ↓
value iteration / policy iteration
```

Key activities:

- calculate one backup manually;
- predict how changing `gamma` changes distant-reward importance;
- visualize repeated backups over a tiny state graph;
- compare a policy before and after improvement.

Checkpoint should require interpreting the update, not merely reproducing a formula.

### C. Learning from experience

```text
Bellman
  ↓
Monte Carlo intuition
  ↓
Temporal Difference
  ↓
TD target / TD error
  ↓
exploration vs exploitation
  ↓
epsilon-greedy
  ↓
SARSA
  ↓
Q-Learning
```

The learner should be able to:

- perform one TD update manually;
- explain bootstrap vs full-return learning;
- distinguish on-policy SARSA from off-policy Q-Learning;
- inspect a Q-table and explain why an action is selected;
- run the same environment with different `alpha`, `gamma` and `epsilon`;
- compare multiple seeds instead of trusting one run.

### D. Function approximation and DQN

Dependency:

```text
Q-Learning + Neural-network foundations
              ↓
      function approximation
              ↓
             DQN
```

The teaching sequence should deliberately begin with the minimal conceptual replacement:

```text
Q-table lookup
Q[state, action]

becomes

network(state)[action]
≈ Q(s,a; θ)
```

Then add DQN mechanisms one at a time:

```text
neural Q approximator
  ↓
epsilon-greedy action selection
  ↓
replay buffer
  ↓
minibatch training
  ↓
target network
  ↓
Double DQN concept
```

The first neural example should remain intentionally small enough that the learner can trace:

```text
state
→ Q-values
→ chosen action
→ reward / next state
→ Bellman target
→ loss
→ gradient update
```

Do not introduce a large framework before this flow is understood.

### E. Policy methods

```text
policy as direct object
  ↓
policy gradient intuition
  ↓
REINFORCE
  ↓
baseline / advantage
  ↓
actor-critic
  ↓
PPO
```

Target competence is conceptual and practical enough to compare value-based and policy-based approaches. The track does not require exhaustive coverage of every modern policy-gradient variant.

### F. Partial observability

This branch is important for autonomous agents because:

```text
WorldTruth != Observation != Belief
```

Progression:

```text
fully observed MDP
  ↓
hidden state introduced
  ↓
observation
  ↓
history / memory
  ↓
belief-state intuition
  ↓
POMDP formulation
  ↓
recurrent-policy concept
```

The environment should be modified so that two different hidden states can produce the same immediate observation. The learner must observe why a policy using only the current observation can fail.

### G. Long-horizon credit assignment

Use a delayed-outcome environment inspired by survival planning:

```text
plant
→ wait
→ maintain
→ harvest
→ consume
```

Concepts:

- delayed and sparse reward;
- n-step return;
- TD(λ) and eligibility-trace intuition;
- temporal credit assignment;
- reward shaping risks.

The learner should experiment with horizons rather than only read about them.

### H. Planning and model-based decision making

Progression:

```text
model-free learner
  ↓
known transition model
  ↓
rollout
  ↓
planning with a model
  ↓
search / MCTS intuition
  ↓
MPC intuition
  ↓
model-based RL concept
```

This branch should explicitly compare:

- learning a value/policy from experience;
- using an available causal model to reason about future transitions.

The track must not imply that model-free RL is automatically preferable when a trustworthy model exists.

### I. Hierarchical decision making

Progression:

```text
primitive action
  ↓
multi-step skill
  ↓
temporal abstraction
  ↓
Option
  ↓
SMDP intuition
  ↓
hierarchical policy / skill selection
```

Example distinction:

```text
high level: obtain food

skill / option:
search_room_for_food

primitive actions:
move
open
inspect
take
```

This branch is the main bridge from RL algorithms to a layered autonomous-agent architecture.

### J. Behavior execution and hybrid architecture

This is not an RL-only branch.

The learner should understand the separation:

```text
goal selection
      ↓
decision / planning
      ↓
behavior
      ↓
skill / local policy
      ↓
action
```

Topics:

- Behavior Tree sequence / selector / condition / action;
- reactive execution;
- interruption and fallback;
- preconditions and effects;
- where a learned policy can live inside a larger behavior;
- why a planner, BT and RL policy are not competing abstractions at the same layer.

The intended transfer result is the ability to reason about which mechanism belongs where, not to declare one universal winner.

## Progressive environment family

The first implementation should use a compact environment family instead of unrelated demos.

### Environment 0 — one-step choice

State:
- hunger level.

Actions:
- eat;
- wait.

Purpose:
- reward;
- return;
- policy vocabulary.

### Environment 1 — tiny survival MDP

State:
- hunger;
- food availability;
- threat.

Actions:
- eat;
- search;
- hide;
- wait.

Purpose:
- MDP;
- V/Q;
- Bellman;
- dynamic programming.

### Environment 2 — experiential learner

Same conceptual world, stochastic transitions.

Purpose:
- Monte Carlo;
- TD;
- SARSA;
- Q-Learning;
- exploration.

### Environment 3 — continuous/large observation

Replace a few discrete state IDs with numeric features.

Purpose:
- function approximation;
- DQN.

### Environment 4 — hidden information

Add hidden threat/resource conditions and partial observations.

Purpose:
- observation vs state;
- memory;
- belief;
- POMDP.

### Environment 5 — delayed survival process

Add delayed resource production and longer horizons.

Purpose:
- n-step;
- delayed credit;
- planning.

### Environment 6 — hierarchical tasks

Expose reusable skills/options over primitive actions.

Purpose:
- SMDP/options;
- planning;
- Behavior execution;
- hybrid agent design.

The family does not need graphical rendering. A simple state inspector, transition diagram, timeline and plots are sufficient.

## Activity types needed from the Portal

This track exercises a useful minimum set of Portal interaction primitives:

- short theory block;
- formula renderer;
- numeric/manual answer;
- state-transition table;
- prediction-before-run prompt;
- parameter control;
- step-through simulation;
- chart;
- editable Python cell;
- structured runtime output;
- compare-runs view;
- misconception feedback;
- mastery checkpoint;
- delayed retrieval prompt;
- transfer/reflection activity.

These primitives should be reusable by non-RL tracks.

## Evaluation and mastery evidence

Examples of deterministic evidence:

- correct discounted return;
- correct Bellman backup;
- correct TD target;
- correct Q update;
- valid action selection under epsilon-greedy conditions;
- implementation satisfies shape and update invariants;
- trained policy crosses a predefined evaluation threshold across declared seeds.

Examples of semantic/rubric evidence:

- explains why target networks improve DQN stability;
- distinguishes state from observation in a partially observable scenario;
- identifies when planning can exploit a known model;
- places RL, planning, BT and options at defensible architectural responsibilities.

One successful training run must never be sufficient evidence by itself.

## Scientific habits taught by the track

The Portal should make these habits visible early:

- multiple seeds;
- baselines;
- train/evaluation separation;
- holdout scenarios when appropriate;
- learning curves;
- variance;
- reward leakage awareness;
- hidden-state leakage awareness;
- ablations;
- reproducible configuration.

This aligns the learning experience with how agent experiments should later be evaluated.

## Transfer to an autonomous-agent project

The specialization should end with an architectural transfer exercise, not direct coupling to a particular repository.

The learner receives a layered agent model:

```text
Perception
→ Needs
→ Goal
→ Decision / Planning
→ Behavior
→ Action
```

and must identify candidate mechanisms for each responsibility while preserving:

- partial observability;
- memory/belief boundaries;
- different temporal horizons;
- reactive execution;
- reusable skills;
- explicit evaluation.

A later project adapter may allow using artifacts or scenarios from a real autonomous-agent project, but that is not required for the first release.

## Explicit non-goals for the first specialization release

Do not block the first useful track on:

- Atari;
- Unity;
- robotics motor control;
- continuous-control algorithms such as SAC/TD3;
- multi-agent RL;
- RLHF;
- transformer-based RL;
- distributed large-scale training;
- GPU requirement;
- visually rich game rendering.

They may become later branches if a real learning need appears.

## Relationship to the general curriculum

This document refines the RL/autonomous-agent region only.

It must not:

- make RL the root of the global ML graph;
- replace the general curriculum;
- force non-RL tracks to use RL-specific interaction patterns;
- turn the autonomous-agent motivating context into a runtime dependency.

The general Skill Graph remains authoritative for cross-track prerequisites. This track contributes detailed candidate nodes and a coherent traversal for one specialization.
