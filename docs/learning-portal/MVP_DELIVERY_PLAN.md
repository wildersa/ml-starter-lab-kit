# Learning Portal MVP Delivery Plan

_Last updated: 2026-09-24_

## Delivery target

Ship a usable Learning Portal MVP by 2026-09-25, optimized for beginning the autonomous-agent RL learning path immediately.

The MVP is a vertical product slice, not a complete LMS or complete RL curriculum.

## Core product flow

```text
Skill Graph
  -> Skill Workspace
  -> theory / worked example
  -> evaluated activity
  -> Evidence
  -> Mastery
  -> Unlock
  -> first LabRL practical activity
```

## Architectural invariant

```text
Portal / control plane != Lab Runtime / execution plane
```

For the MVP, reuse existing repository capabilities pragmatically. Arbitrary learner Python must not be introduced into the Portal process.

## Delivery order

1. Portal MVP + first LabRL activity.
2. RL foundational content pack in parallel.
3. Portal hardening/gaps only where they block delivery or create immediate risk.
4. Separated execution runtime after the initial MVP path is usable.
5. DQN learning slice.
6. Advanced autonomous-agent content: POMDP, delayed credit, planning, hierarchy, Behavior Trees.

## Delivery behavior

- Prefer completion over perfect architectural polish.
- Keep coherent overdelivery.
- If the core is delivered with gaps, accept the core and log gaps in `MVP_GAPS.md`.
- Fix immediately only gaps that block current use, the next slice, or a hard architectural invariant.
- Work that can safely proceed in parallel should be dispatched in parallel.
- The `jules` label is the dispatch mechanism for Jules.
