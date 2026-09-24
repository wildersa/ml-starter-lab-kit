# Learning Portal

This folder contains the product, pedagogy, platform boundaries, active design work, and implementation planning for the Learning Portal inside the ml-starter-lab-kit ecosystem.

The current starter generator, generated project structure, labs, and existing Streamlit workspace remain separate. The Portal may reuse capabilities and data, but it is not a refactor of the current workspace.

## Start here

For current work, read these documents first:

1. [../../STATUS.md](../../STATUS.md) — project-level status and active fronts.
2. [11-portal-blueprint.md](11-portal-blueprint.md) — canonical working blueprint for the learner-facing Portal.
3. [12-portal-work-tracker.md](12-portal-work-tracker.md) — current Portal design stage and bounded work packages.
4. [10-platform-architecture.md](10-platform-architecture.md) — platform ownership and technical direction.
5. [13-access-and-runtime-boundaries.md](13-access-and-runtime-boundaries.md) — hard Portal/Lab Runtime and access constraints.
6. [15-implementation-plan.md](15-implementation-plan.md) — implementation sequence once the design gates permit implementation.

For the current focused proving content:

- [14-autonomous-agent-rl-track.md](14-autonomous-agent-rl-track.md) — RL specialization aimed at autonomous-agent reasoning, from Bellman/Q-Learning through DQN, POMDP, planning and hierarchy.

## Authority map

The numbered files are not intended to be read as one long linear specification. Use them by concern.

### Product and pedagogy

- [01-product-vision.md](01-product-vision.md) — product purpose, boundaries and long-term learner experience.
- [02-learning-model.md](02-learning-model.md) — standard learning loop, mastery, retrieval and transfer.
- [09-learning-science-foundations.md](09-learning-science-foundations.md) — adopted learning-science foundation and methodology rules.

When these overlap, 09 defines the adopted methodology, 02 applies it operationally, and 01 remains the product-level framing.

### Content and progression

- [03-skill-graph.md](03-skill-graph.md) — graph progression, prerequisites, unlocks and mastery states.
- [04-curriculum.md](04-curriculum.md) — broad curriculum map and candidate teaching order.
- [05-content-sources-and-licensing.md](05-content-sources-and-licensing.md) — source, citation and licensing rules.
- [06-activities-and-assessment.md](06-activities-and-assessment.md) — activity/evaluation patterns.
- [14-autonomous-agent-rl-track.md](14-autonomous-agent-rl-track.md) — detailed focused specialization used as the preferred proving track.

The broad curriculum remains authoritative for the global ML graph. The RL track refines one region and must not turn RL into the root of the whole product.

### Platform and runtime

- [10-platform-architecture.md](10-platform-architecture.md) — Portal/control-plane and Lab Runtime/execution-plane architecture.
- [13-access-and-runtime-boundaries.md](13-access-and-runtime-boundaries.md) — adopted hard constraints for execution, project access, roles and topology.
- [08-content-and-runtime-boundaries.md](08-content-and-runtime-boundaries.md) — supporting separation of content, learning engine, evaluator and existing project capabilities.

For new technical decisions, prefer 10 and 13 as the active authorities. Keep 08 as supporting background unless it is explicitly promoted.

### Learner experience and active design

- [07-portal-experience.md](07-portal-experience.md) — earlier learner-surface framing and supporting product context.
- [11-portal-blueprint.md](11-portal-blueprint.md) — canonical active design blueprint.
- [12-portal-work-tracker.md](12-portal-work-tracker.md) — canonical operational tracker for Portal design rounds.

When 07 and 11 overlap, 11 is the active design authority.

### Implementation planning

- [15-implementation-plan.md](15-implementation-plan.md) — first implementation path, vertical slices, gates, test strategy and ownership targets.

This plan does not bypass the staged design process in 12. It gives the team a concrete implementation target so current design decisions can be tested against a real workload.

## Product model

The project supports two complementary experiences:

1. **Starter / experiment mode** — generate a clean ML project and work normally.
2. **Learning mode** — learn concepts through an interactive Portal with theory, worked examples, guided/manual practice, experiments, library use, review and mastery tracking.

The Portal is a dedicated web application, not Jupyter or Streamlit as the product shell.

## Adopted learning model

The foundation is:

- Mastery Learning;
- Cognitive Load management + Worked Examples + Scaffolding;
- Retrieval Practice;
- Experiential Learning;
- Competency / Skill Graph progression.

Gamification may sit on top of the model, but XP never substitutes for evidence of competence.

The default learning progression is:

~~~text
intuition
→ theory
→ visualization
→ worked example
→ guided/manual execution
→ prediction
→ experiment
→ reduced scaffolding
→ library abstraction
→ realistic application
→ mastery checkpoint
→ later retrieval
→ transfer
~~~

## Platform invariant

The central ownership split is:

~~~text
PORTAL / CONTROL PLANE
- content
- Skill Graph
- learner state
- attempts
- evidence
- mastery
- review
- notes
- runtime/session requests
- result presentation

          │ scoped capability/session
          ▼

LAB RUNTIME / EXECUTION PLANE
- Python execution
- simulations
- ML/data dependencies
- project/dataset access when authorized
- structured execution outputs
- artifacts
- timeout/cancellation
- isolation/cleanup
~~~

This split applies even when both run on the same local machine.

Arbitrary learner code never executes inside the Portal/API process. Runtime results are evidence inputs; the Runtime does not own progression or mastery.

## Focused proving track

The first detailed specialization is Reinforcement Learning for autonomous agents.

It is useful because one coherent track can exercise:

- manual numeric activities;
- Skill Graph prerequisites;
- deterministic checking;
- simulations;
- multi-seed experiments;
- Python execution;
- PyTorch;
- evidence/mastery/unlocks;
- review;
- later partial observability, planning and hierarchy.

The first implementation proof is intentionally smaller than the full specialization:

~~~text
reward / return
→ discounting
→ MDP
→ V / Q
→ Bellman
→ TD
→ Q-Learning
→ function approximation
→ DQN
~~~

Later branches extend the same platform to POMDP, delayed credit, model-based planning, options/SMDP and Behavior Trees.

## Documentation maintenance rules

To keep this folder from becoming another specification dump:

1. Add a decision to its owning authority instead of copying it into several files.
2. Use this README as the navigation and authority map.
3. Do not rename/move numbered documents merely for aesthetics; avoid link churn unless ownership really changes.
4. Mark older framing documents as supporting when a newer authority supersedes them.
5. Keep current operational state in STATUS/work trackers, not in every design document.
6. Keep focused specialization detail out of the global curriculum except for links and cross-track prerequisites.
7. Do not turn every document section into an implementation issue.

## Current status

The Learning Portal itself is not implemented yet.

Existing starter/lab capabilities remain operational, while the Portal is still in staged product/platform design. The focused RL track and implementation plan now provide a concrete target for those design stages without changing the requirement that Portal and Lab Runtime remain separate.
