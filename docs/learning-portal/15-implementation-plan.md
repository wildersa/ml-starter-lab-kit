# Learning Portal implementation plan — autonomous-agent RL vertical slice

**Status:** implementation planning; does not override the active Portal design-stage gates  
**Primary proving track:** [14-autonomous-agent-rl-track.md](14-autonomous-agent-rl-track.md)  
**Architectural constraints:** [10-platform-architecture.md](10-platform-architecture.md) and [13-access-and-runtime-boundaries.md](13-access-and-runtime-boundaries.md)

## Purpose

Turn the Learning Portal design into an implementation sequence that can prove the product with one coherent specialization: Reinforcement Learning for autonomous-agent reasoning.

The goal is not to build the entire curriculum first. The goal is to establish the smallest reusable platform slice that demonstrates:

~~~text
Skill Graph
→ Skill Workspace
→ guided/manual activity
→ optional code execution
→ evaluation
→ evidence
→ mastery
→ unlock
→ review
~~~

while preserving the hard boundary:

~~~text
Portal / control plane
!=
Lab Runtime / execution plane
~~~

The RL content is a proving workload. The platform pieces must remain reusable for supervised, unsupervised, deep-learning and MLOps tracks.

## Implementation principles

1. **Implement vertical capability, not document structure.** Do not create one package or API per documentation chapter.
2. **Keep the first slice local-first but topology-neutral.** Portal and Runtime may run on one machine, but they remain separate processes and contracts.
3. **No arbitrary learner code in the Portal process.** Python execution belongs to the Lab Runtime.
4. **Evidence is the bridge.** Runtime results do not directly mutate mastery. The Portal evaluates/accepts evidence and applies progression rules.
5. **Content is declarative where practical.** A skill/activity definition should not require a React code change for ordinary authored content.
6. **Do not freeze a universal schema too early.** Start with the minimum shapes required by the vertical slice, with explicit versioning.
7. **Build one evolving environment family.** Avoid unrelated RL demos that duplicate infrastructure.
8. **Headless first.** State diagrams, tables, timelines and plots are enough; no game-engine or rich rendering dependency is required.

## First-release proof

The first complete product proof should cover this path:

~~~text
RL vocabulary
→ reward vs return
→ discounting
→ MDP
→ V and Q
→ one Bellman backup
→ TD target / TD error
→ one Q-Learning update
→ tabular Q-Learning experiment
→ function approximation
→ minimal neural Q approximator
→ DQN mechanisms
~~~

It is acceptable for later autonomous-agent topics — POMDP, delayed credit, planning, options and Behavior Trees — to enter after this first proof if the platform is already reusable.

The first proof must still be designed so those topics do not require an architectural rewrite.

# 1. Target architecture

## Portal / control plane

Suggested logical ownership:

~~~text
Web Portal
  ↓
Learning API
  ├─ Content / Skill Graph
  ├─ Learner State
  ├─ Activity Orchestration
  ├─ Evaluation policy
  ├─ Evidence
  ├─ Mastery / Unlock
  ├─ Review
  └─ Runtime session client
~~~

The Portal owns content navigation, skill prerequisites, learner attempts, submitted non-code answers, evidence acceptance, mastery calculation, unlock state, review state, notes, runtime capability requests and presentation of runtime results.

## Lab Runtime / execution plane

~~~text
Runtime service
  ├─ session/capability validation
  ├─ Python Runner
  ├─ activity workspace
  ├─ allowed dependencies
  ├─ execution limits
  ├─ structured outputs
  ├─ artifacts
  └─ cancellation/cleanup
~~~

The Runtime owns executing learner Python, running deterministic RL simulations, producing structured traces, generating allowed charts/artifacts, enforcing timeout/resource policy, accessing a connected project only through explicit capability and cleaning up execution state.

The Runtime does not own curriculum, mastery, unlock logic, learner navigation or pedagogical review scheduling.

## Evaluator split

Evaluation has two responsibilities:

~~~text
Portal-side pedagogical evaluator
- knows what competence is being assessed
- decides which evidence counts
- produces misconception/mastery signals

Runtime-side execution helpers
- inspect values, shapes, traces, invariants
- return structured facts about execution
~~~

Example:

~~~text
learner code
  ↓
Runtime executes
  ↓
structured facts: q_before, q_after, td_target, trace
  ↓
Portal evaluator checks activity criteria
  ↓
Evidence
  ↓
Mastery / feedback
~~~

# 2. Proposed repository ownership

This is a planning target, not a frozen package contract.

A clean implementation should converge toward logical areas equivalent to:

~~~text
apps/
  learning_portal/
    web/               # React + TypeScript learner UI
    api/               # FastAPI composition/application boundary

packages/
  learning/
    content/           # skill/activity loading and validation
    graph/             # prerequisites/unlocks
    learner_state/     # attempts, notes, evidence, mastery, review
    evaluation/        # deterministic/rubric evaluation contracts

services/
  lab_runtime/
    api/               # runtime/session endpoint
    runner/            # isolated execution
    environments/      # reusable teaching environments
    outputs/           # structured results/artifacts

content/
  skills/
    rl/
    deep_learning/
~~~

The exact paths may change after the active design stages. The important ownership rule is that Portal application code and execution-sensitive Runtime code remain independently testable and deployable.

Existing starter-generator templates and current Streamlit workspace should remain untouched unless a concrete integration need appears.

# 3. Minimal domain contracts to prove

Do not start by modeling every future Portal concept. The first implementation needs only enough explicit contracts to support the vertical slice.

## Skill

Minimum conceptual fields:

- stable id;
- version;
- title;
- purpose;
- prerequisites;
- activities;
- checkpoint;
- unlock targets/tags.

## Activity

Minimum conceptual fields:

- stable id;
- skill id;
- activity type;
- prompt/content reference;
- required runtime capability, if any;
- evaluator reference;
- allowed hints;
- evidence types produced.

Initial activity families:

- reading/theory;
- manual numeric answer;
- prediction;
- parameterized simulation;
- Python code execution;
- checkpoint.

## Attempt

- learner;
- skill/activity;
- started/submitted/completed timestamps;
- submitted answer or execution request reference;
- hints used;
- result state.

## Evidence

- learner;
- source activity/attempt;
- evidence type;
- normalized result;
- evaluator version;
- provenance;
- timestamp.

## Mastery state

- learner;
- skill;
- acquired/not acquired;
- current mastery indicator;
- needs-review flag;
- evidence references.

The first version does not need probabilistic knowledge tracing.

## Runtime session/capability

Minimum semantics:

- owner;
- activity;
- granted capabilities;
- expiration;
- runtime identity;
- cancellation/revocation;
- structured result reference.

The protocol shape belongs to the later runtime-contract stage; these semantics must be preserved now.

# 4. Progressive implementation slices

## Slice 0 — documentation and authority cleanup

**Goal:** make the project navigable before implementation begins.

Deliver:

- canonical documentation index;
- active vs supporting vs historical document classification;
- explicit implementation plan;
- explicit autonomous-agent RL specialization;
- root documentation link to the Learning Portal;
- current status pointing to one implementation path.

Exit criterion:

> A new contributor can identify the product authority, platform authority, active work tracker, focused content track and implementation plan without reading every numbered document.

## Slice 1 — content loader + read-only Skill Graph

**Portal only; no Runtime required.**

Deliver:

- versioned skill definitions for the first RL nodes;
- prerequisite edges;
- read-only graph endpoint;
- graph UI showing locked/available states for a local learner;
- lock reason;
- one recommended next skill.

Seed skills:

~~~text
rl.agent-environment
rl.reward-return
rl.discounting
rl.markov
rl.mdp
rl.value-functions
rl.bellman-backup
~~~

Do not implement mastery sophistication yet. A local development learner may use explicit seeded state.

Exit criterion:

> The learner can open the Portal, inspect the graph, select an available RL skill and understand why later nodes are locked.

## Slice 2 — Skill Workspace with Portal-only activities

**No arbitrary code execution yet.**

Deliver:

- skill page;
- theory blocks;
- worked example;
- numeric/manual answer;
- prediction prompt;
- deterministic evaluator for numeric/formula-derived answers;
- attempt/evidence persistence;
- basic acquisition rule;
- graph unlock after valid evidence.

First complete learning path:

~~~text
reward vs return
→ discounting
→ one Bellman backup
~~~

Example Bellman activity:

- small state;
- known rewards/transitions;
- learner enters target/update;
- evaluator checks result with tolerance;
- feedback identifies reward/discount/max-next-Q mistakes when distinguishable.

Exit criterion:

> The learner can acquire a skill from evidence and see a dependent node unlock without any Runtime service.

This slice proves that not every learning interaction requires execution.

## Slice 3 — deterministic simulation capability

Introduce the Lab Runtime as a separate service.

Runtime capability: **rl.simulate**.

Deliver:

- Runtime process separate from Portal;
- short-lived local session;
- deterministic tiny-survival environment;
- seed/config input;
- structured transition trace output;
- Portal visualizer for state/action/reward transitions;
- timeout/cancellation basics;
- runtime unavailable state.

No free-form Python is required yet.

Exit criterion:

> The Portal can request a simulation capability, receive a structured trace and render it, while remaining functional when the Runtime is offline.

## Slice 4 — Q-Learning experiment

Deliver:

- Q-table representation;
- epsilon-greedy visual explanation;
- step-through TD/Q update;
- parameter controls for alpha, gamma and epsilon;
- multi-seed run;
- learning-curve output;
- deterministic/invariant evaluator;
- compare-runs view.

The learner should first perform one Q update manually, then run the algorithm.

Evidence may include correct update, correct interpretation of policy/Q table, successful experiment configuration and explanation/prediction activity.

Exit criterion:

> The learner can move from a manual Q update to an empirical Q-Learning run and explain the relationship between the two.

## Slice 5 — controlled Python execution

Add capability: **python.execute.learning**.

Deliver:

- editable Python cell only inside allowed activities;
- isolated execution workspace;
- package allowlist/policy;
- stdout/stderr;
- scalar/list/array/table outputs;
- execution timeout;
- cancellation;
- structured error reporting;
- activity-scoped files only.

The first coding tasks should fill small missing pieces, not paste complete agents.

Examples:

- implement discounted return;
- implement one Q update;
- implement epsilon-greedy selection.

Exit criterion:

> Learner code executes outside the Portal process and returns structured evidence that can be evaluated reproducibly.

## Slice 6 — neural Q approximation and DQN

Dependencies:

~~~text
Q-Learning mastery
+
neural-network prerequisite nodes
~~~

Deliver a staged DQN workspace:

1. Q-table vs network(state)[action];
2. forward pass and selected action value;
3. Bellman target;
4. loss;
5. optimizer step;
6. epsilon-greedy;
7. replay buffer;
8. minibatch;
9. target network;
10. conceptual Double DQN comparison.

Use a small numeric survival environment. GPU must not be required.

Exit criterion:

> The learner can explain which part of tabular Q-Learning remains conceptually unchanged and which DQN mechanisms exist for scale/stability.

## Slice 7 — review and retained mastery

Deliver:

- review queue;
- changed numerical examples;
- retrieval prompts;
- misconception-targeted review;
- acquired vs needs-review distinction;
- history/evidence view.

Initial review targets:

- reward vs return;
- gamma;
- Bellman target;
- TD error;
- Q-Learning update;
- target network purpose.

Exit criterion:

> A previously acquired skill can require review without losing its acquisition badge, and new evidence can clear the review need.

## Slice 8 — autonomous-agent advanced branch

After the core platform proves reusable, extend the same environment family:

- POMDP / observation vs hidden state;
- memory/belief;
- n-step / TD(lambda);
- delayed reward;
- model-based planning;
- rollout/search;
- options/SMDP;
- hierarchical policies;
- Behavior Tree execution;
- hybrid architecture exercise.

This slice should reuse the same activity, Runtime, evidence and mastery infrastructure. New platform primitives require explicit justification.

# 5. First vertical-slice Skill Graph

A practical first graph:

~~~text
rl.agent-environment
        ↓
rl.reward-vs-return
        ↓
rl.discounting
        ↓
rl.markov-property
        ↓
rl.mdp
        ↓
rl.value-functions
        ↓
rl.bellman-backup
        ↓
rl.td-foundations
        ↓
rl.exploration
        ↓
rl.q-learning
        ├───────────────┐
        ↓               │
rl.q-learning-lab       │
                        │
nn.forward-pass ────────┤
nn.loss-gradient ───────┤
                        ↓
                 rl.function-approximation
                        ↓
                      rl.dqn
~~~

This is intentionally small. Policy gradients/PPO, POMDP, planning and hierarchy belong to later branches, not the first implementation gate.

# 6. Content design for each implemented skill

Each first-release RL skill should declare:

- **Learning objective:** one demonstrable statement.
- **Required prior competence:** graph prerequisites, not chapter adjacency.
- **Worked example:** small enough to trace completely.
- **Guided activity:** partial scaffolding.
- **Prediction:** ask what should change before showing the execution.
- **Experiment:** parameter or state change with observable consequence.
- **Independent checkpoint:** changed example without the worked solution visible.
- **Misconceptions:** machine-usable tags where possible.
- **Review variants:** at least one changed problem for later retrieval.

Example misconception tags:

- reward_equals_return;
- gamma_applied_to_immediate_reward;
- q_uses_current_state_max;
- sarsa_qlearning_policy_confusion;
- target_network_is_second_policy.

# 7. Testing strategy

## Content tests

Validate:

- unique ids;
- valid prerequisite references;
- DAG/no unintended cycles;
- evaluator references exist;
- runtime capabilities are declared explicitly;
- version fields present.

## Learning-core tests

Validate:

- locked/available transitions;
- acquisition rule;
- evidence provenance;
- review-state transitions;
- no XP-only unlock.

## Portal API tests

Validate:

- learner ownership;
- graph projection;
- attempt lifecycle;
- evaluation result handling;
- runtime unavailable behavior.

## Runtime tests

Validate:

- session scope;
- timeout;
- cancellation;
- deterministic seeds;
- structured output contracts;
- environment reset isolation;
- no Portal-state mutation.

## End-to-end proof

At minimum:

~~~text
fresh learner
→ opens graph
→ completes discounting
→ dependent Bellman skill unlocks
→ completes manual Bellman activity
→ runs tiny RL simulation
→ evidence persisted
→ Q-Learning node becomes available
~~~

A later E2E adds Python execution.

# 8. What to reuse from the existing repository

Reuse capabilities before UI.

Good reuse candidates:

- generator/project metadata contracts;
- synthetic data patterns where useful;
- experiment configuration ideas;
- existing Multi-Armed Bandit educational material;
- existing tests/utilities that are generic;
- current docs on metrics and experimentation.

Do not make the new Portal depend on:

- current Streamlit workspace layout;
- Streamlit session state;
- generated-project UI internals;
- direct imports from learner projects;
- a particular local filesystem topology.

# 9. Documentation reorganization rule

Do not physically rename every existing numbered Portal document merely for aesthetics. That would create link churn without adding product value.

Instead, documentation should be organized by **authority and concern** in the Portal README:

- Start here / current state;
- Product and pedagogy;
- Content and Skill Graph;
- Platform and runtime;
- Active planning;
- Focused specialization.

Documents that overlap should either clearly defer to one canonical authority or be marked as background/supporting material.

New decisions should be added to the correct authority rather than duplicated across multiple docs.

# 10. Implementation gates

## Gate A — design readiness

Before production implementation:

- current IA stage reviewed;
- Skill Workspace responsibility clear;
- Practice Lab responsibility clear;
- first learner flow agreed;
- first local deployment mode agreed;
- focused RL skill list accepted.

## Gate B — Portal-only vertical proof

Required:

- content loading;
- graph;
- workspace;
- deterministic manual evaluation;
- evidence;
- mastery/unlock.

No Runtime dependency.

## Gate C — Runtime boundary proof

Required:

- separate Runtime process;
- capability/session semantics;
- deterministic simulation;
- unavailable/error/cancel behavior.

## Gate D — learner-code proof

Required:

- controlled Python execution;
- structured outputs;
- isolation policy;
- evaluator integration;
- reproducibility.

## Gate E — DQN proof

Required:

- neural prerequisite skills;
- PyTorch CPU environment;
- replay/target-network activities;
- multi-seed evaluation;
- no hidden dependency on game UI.

## Gate F — autonomous-agent specialization proof

Required:

- partial observability;
- long-horizon credit;
- planning/model use;
- hierarchical skills/options;
- behavior-execution comparison;
- transfer exercise to a layered agent architecture.

# 11. Explicit first-release non-goals

Do not block implementation on:

- full global ML curriculum completion;
- SaaS multi-tenancy;
- all future roles;
- LLM tutoring;
- arbitrary package installation;
- arbitrary filesystem access;
- GPU orchestration;
- Jupyter compatibility;
- every RL algorithm;
- real Project Zomboid integration;
- rich 2D/3D game rendering;
- probabilistic knowledge tracing.

The first release should be locally useful, pedagogically sound and architecturally compatible with later hosted/hybrid modes.

# 12. Immediate work order

The current design process should not be skipped. The practical next order is:

~~~text
1. Finish Portal IA:
   Skill Workspace
   Practice Lab
   Review
   Notes
   Progress
   Project Context
   cross-surface review

2. Use the RL track as the concrete scenario while refining:
   interaction primitives
   learner flows
   mastery/review presentation

3. Freeze the first implementation boundary:
   local Portal
   local separate Runtime
   first skill definitions
   first evidence model

4. Implement Portal-only Bellman vertical slice.

5. Add deterministic Runtime simulation.

6. Add controlled Python execution.

7. Extend to Q-Learning and DQN.

8. Extend to POMDP/planning/hierarchy.
~~~

This sequence keeps the architecture disciplined while turning the autonomous-agent learning goal into a concrete implementation driver rather than an abstract future example.
