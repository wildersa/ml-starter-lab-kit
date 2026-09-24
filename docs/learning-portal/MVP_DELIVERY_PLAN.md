# Learning Portal MVP Delivery Plan

_Last updated: 2026-09-24_

## Delivery target

Ship and stabilize a usable Learning Portal MVP by 2026-09-25, optimized for beginning the autonomous-agent RL learning path immediately.

The MVP is a vertical product slice plus the minimum reusable platform base needed to keep adding courses without repeatedly rewriting the Portal core.

## Core product flow

```text
Skill Graph
  -> Skill Workspace
  -> theory / worked example
  -> evaluated activity
  -> Evidence
  -> Mastery
  -> Unlock
  -> practical Lab/Runtime activity when required
```

## Architectural invariant

```text
Portal / control plane != Lab Runtime / execution plane
```

Arbitrary learner code or execution-sensitive lab logic must not become a permanent responsibility of the Portal process.

## Current state

Already delivered on `main`:

- working React learner Portal;
- FastAPI API;
- SQLite persistence;
- prerequisite-aware Skill Graph;
- Skill Workspace;
- deterministic response evaluator;
- evidence/mastery/unlock flow;
- seven real RL foundational skills;
- first LabRL GridWorld/Q-Learning activity;
- foundational and advanced RL content packs.

## Structural priority

### 1. Finish separate Lab Runtime

Issue #212 / PR #219.

This is the current shared-infrastructure priority.

### 2. Build declarative Skill/Course engine

Issue #220.

Goal: normal content/skill additions should be declarative and versioned, not hardcoded in core Portal Python.

### 3. Add learner identity/profile boundary

Issue #221.

Goal: progress, evidence and mastery must belong to an explicit learner. Local-first identity is sufficient; production authentication is not required.

#220 and #221 may run in parallel if file ownership is safely separated. Otherwise #220 goes first.

### 4. Continue execution-capable learning slices

Issue #214 DQN becomes the next interactive/execution priority after the reusable base is safely underway.

## Content parallelism

Content authoring is not serialized by the structural sequence above.

RL foundations, DQN, POMDP, planning/model-based material, hierarchical RL/Options, Behavior Trees, review material and other didactic content may be authored in parallel when they use isolated content paths.

Integration into Portal interaction/runtime surfaces may wait for the relevant engine capability.

## Delivery behavior

- Prefer completion over perfect polish.
- Keep coherent overdelivery.
- If the core is delivered with gaps, accept the core and log non-blocking gaps in `MVP_GAPS.md`.
- Fix immediately only gaps that block current use, the next slice, learner-state correctness, or a hard architectural invariant.
- Work that can safely proceed in parallel should be dispatched in parallel.
- The `jules` label is the dispatch mechanism for Jules.
