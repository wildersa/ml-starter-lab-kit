# Learning Portal work tracker

_Last updated: 2026-09-24_

## Purpose

This is the current operational tracker for Learning Portal delivery.

The earlier stage-by-stage design workflow that previously lived in this file is preserved in Git history. The project has moved beyond design-only execution into implementation and MVP hardening.

Current operational authority:

1. this tracker;
2. `MVP_DELIVERY_PLAN.md`;
3. `MVP_GAPS.md`;
4. architectural constraints in `13-access-and-runtime-boundaries.md`.

## Delivery state

| Work item | State | Notes |
| --- | --- | --- |
| Initial Portal vertical slice | DONE | React + FastAPI + SQLite + Skill Graph + Workspace + evaluator + Evidence/Mastery/Unlock + LabRL |
| RL foundational content | DONE | Authored, licensed/source-tracked and integrated |
| Advanced RL/autonomous-agent content | DONE AS CONTENT | DQN, policy methods, POMDP, planning, HRL, BT and transfer material authored |
| #219 / #212 Separate Lab Runtime | IN_PROGRESS | Current structural priority |
| #220 Declarative Skill/Course engine | QUEUED_NEXT | Dispatch after #219 merge |
| #221 Learner identity/profile boundary | QUEUED_NEXT | Dispatch after #219 merge; parallel with #220 only if conflict-safe |
| #214 DQN interactive/execution slice | WAITING_BASE | Prioritize after #220/#221 are safely underway or landed |

## What is already a working base

The current `main` supports:

```text
Skill Graph
  -> Skill Workspace
  -> learning content
  -> evaluated activity
  -> Evidence
  -> Mastery
  -> Unlock
  -> LabRL
```

This is a functional vertical slice, but it is not yet the final reusable platform base.

## Base-platform completion criteria

The structural base is considered ready for broad course growth when all of the following are true:

- Portal/control-plane and Lab Runtime/execution-plane are separated;
- ordinary skills/courses are declarative and versioned rather than hardcoded into core application code;
- learner identity explicitly owns progress/evidence/mastery;
- the current evaluator and progression flow remain compatible;
- current RL course continues to run through the same engine.

## Parallelization rule

Content authoring may proceed in parallel and in any pedagogically coherent order when it remains isolated from shared Portal/runtime code.

Serialize only work that predictably collides in shared infrastructure such as:

- Portal application core;
- persistence/mastery contracts;
- learner identity;
- shared course/skill loader;
- Runtime service boundary.

## Active dispatch policy

The `jules` label dispatches work to Jules.

Current structural sequence:

```text
finish #219
   ↓
dispatch #220
dispatch #221 when conflict-safe
   ↓
stabilize reusable base
   ↓
dispatch #214 DQN execution
```

Content-only work may be dispatched independently of this sequence.

## Review policy

For each delivery:

- merge/accept when core acceptance criteria are met and there is no blocking defect;
- keep coherent overdelivery;
- record non-blocking gaps in `MVP_GAPS.md`;
- fix immediately only defects that block current use, the next slice, learner-state correctness, or a hard architecture boundary;
- do not force rework for polish.

## Historical design documents

The following remain useful as design references:

- `01-product-vision.md`
- `02-learning-model.md`
- `03-skill-graph.md`
- `04-curriculum.md`
- `05-content-sources-and-licensing.md`
- `06-activities-and-assessment.md`
- `07-portal-experience.md`
- `08-content-and-runtime-boundaries.md`
- `09-learning-science-foundations.md`
- `10-platform-architecture.md`
- `11-portal-blueprint.md`
- `13-access-and-runtime-boundaries.md`

They are references, not an instruction to return to the previous design-only stage gates.
