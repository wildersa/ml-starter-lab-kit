# Project Status

_Last updated: 2026-09-24_

## Current focus

The active delivery is the **Learning Portal MVP** for `ml-starter-lab-kit`, with Reinforcement Learning as the first proving path for the autonomous-agent learning program.

The project is no longer in design-only mode. A working vertical slice is already on `main`.

## Current implementation state

### Delivered on `main`

- React + TypeScript learner Portal.
- FastAPI application API.
- SQLite learner-state persistence.
- prerequisite-aware Skill Graph;
- Skill Workspace with theory, worked examples and evaluated activities;
- deterministic evaluator with numeric tolerance, exact-choice/text checks, feedback and misconception tags;
- Evidence -> Mastery -> Unlock progression;
- seven integrated RL foundation skills:
  - RL vocabulary;
  - Reward vs Return;
  - Discounting;
  - MDP;
  - V and Q;
  - Bellman backup;
  - TD / Q-Learning;
- first LabRL practical activity with GridWorld and visible Q-Learning diagnostics;
- foundational and advanced RL content packs with source/license tracking.

## Base-platform work still active

### 1. Separate Lab Runtime — ACTIVE

Issue: #212  
PR: #219

Goal: move execution-sensitive Lab work out of the Portal/control-plane process and expose it through an explicit Runtime boundary.

This is the current structural priority.

### 2. Declarative Skill/Course engine — QUEUED NEXT

Issue: #220

Goal: remove normal curriculum authoring from hardcoded `portal/api/graph.py` definitions and load versioned declarative course/skill content through a validated engine.

A normal new lesson should not require changing core Portal application code.

### 3. Learner identity/profile boundary — QUEUED NEXT

Issue: #221

Goal: replace implicit single-global-learner state with an explicit local learner identity so progress, evidence and mastery are learner-owned and isolated.

No production authentication is required for this stage.

## Content work

Content authoring is intentionally **parallel and order-independent** when it writes to isolated content paths.

Already present:

- RL foundations;
- DQN foundations;
- policy gradients / actor-critic;
- POMDP and delayed credit;
- model-based/planning concepts;
- hierarchical RL / Options / SMDP;
- Behavior Trees and layered-agent architecture;
- misconceptions, experiments and transfer exercises.

Content creation does not need to wait for Runtime or Portal-base work. Integration into interactive Portal surfaces may wait for the relevant platform capability.

## Next implementation priority

```text
#219 Separate Lab Runtime
        ↓
#220 Declarative Skill/Course engine
#221 Learner identity/profile
        ↓
#214 DQN interactive/execution slice
        ↓
additional advanced interactive learning surfaces
```

#220 and #221 may run in parallel only when file ownership is sufficiently separated to avoid predictable merge conflicts.

## Operational authority

For current delivery decisions, use:

1. `docs/learning-portal/MVP_DELIVERY_PLAN.md`
2. `docs/learning-portal/MVP_GAPS.md`
3. `docs/learning-portal/12-portal-work-tracker.md`

The earlier blueprint/research documents under `docs/learning-portal/` remain architectural and pedagogical references, but they are not a reason to revert the project to a design-only workflow.

## MVP policy

Prefer a working vertical slice over perfect polish.

- **BLOCKING NOW** — breaks current use, next-stage delivery, learner-state integrity, or a hard Portal/Runtime boundary.
- **FIX SOON** — material near-term risk that does not invalidate the current core.
- **DEFER** — polish or future capability; record and keep delivery moving.

Sensible overdelivery is kept when it remains coherent with the product direction.
