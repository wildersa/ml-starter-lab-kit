# Learning Portal MVP Gaps

_Last updated: 2026-09-24_

## Purpose

Operational gap log for the Learning Portal MVP delivery.

The goal is to ship a usable MVP quickly. A delivered core should not be rejected because of non-blocking polish gaps.

## Review rule

For every Jules delivery, classify findings as:

- **BLOCKING NOW** — breaks the current MVP core, violates the Portal/Lab Runtime boundary, prevents the next work item, corrupts learner state/evidence, or makes the product unusable. Fix immediately, preferably in parallel.
- **FIX SOON** — important but does not block the current vertical slice. Open/activate a repair issue only when it will materially reduce risk in the next few hours.
- **DEFER** — polish, optional hardening, or future-scope work. Record it here and keep delivery moving.

Useful extra work from Jules should be kept when coherent with the new plan. Do not request rework merely because the implementation exceeded the narrow wording of an issue.

## MVP acceptance target

The MVP is usable when a learner can:

1. open the Learning Portal;
2. see a small prerequisite-aware Skill Graph;
3. open an RL skill;
4. consume real learning content;
5. complete at least one evaluated activity;
6. persist evidence/mastery;
7. see a dependent skill unlock;
8. run the first LabRL-backed practical activity;
9. resume without losing core learning state.

## Active gaps

### DEFER
- **DQN / Deep RL algorithms**: Currently limited to tabular Q-Learning on 3x3 GridWorld.
- **Advanced Graph Visualizations**: Currently renders hierarchical list-based DAG nodes rather than force-directed interactive graphs.
- **Multi-user authentication / RBAC**: SQLite store is local-first single-learner without user logins.
- **Full Course Authoring System**: Curriculum is defined in code (`portal/api/graph.py`).

## Resolved gaps

- **[2026-09-24] Initial Vertical Slice Delivered**: Learner Portal MVP with FastAPI backend, SQLite persistence, React frontend, 7-node RL Skill Graph, evaluated math activities, and first LabRL 3x3 GridWorld Q-Learning activity.
