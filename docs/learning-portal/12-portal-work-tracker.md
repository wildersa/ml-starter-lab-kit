# Learning Portal work tracker

## Purpose

This document is the operational companion to [`11-portal-blueprint.md`](11-portal-blueprint.md).

The blueprint explains **what the Portal must eventually define**. This tracker explains **what an agent may work on in the current round, how it should choose that work, what it must update, and where it must stop**.

This is intentionally a design/documentation workflow before implementation.

Use these status values:

- `LOCKED` — do not work on this yet;
- `ELIGIBLE` — may be selected in the current stage;
- `IN_PROGRESS` — current round owns this item;
- `DONE` — item has met its item-level completion criteria;
- `BLOCKED` — requires a decision or dependency outside this item;
- `READY_FOR_REVIEW` — every stage exit criterion appears satisfied; human review is required before moving to the next stage.

---

# 1. Canonical documents

Before every round, read at least:

1. [`11-portal-blueprint.md`](11-portal-blueprint.md) — canonical Portal design blueprint;
2. this tracker — canonical operational state for Portal design work;
3. [`02-learning-model.md`](02-learning-model.md) — learning behavior that the Portal must support;
4. [`03-skill-graph.md`](03-skill-graph.md) — progression and prerequisite model;
5. [`10-platform-architecture.md`](10-platform-architecture.md) — already adopted technical direction;
6. [`13-access-and-runtime-boundaries.md`](13-access-and-runtime-boundaries.md) — adopted access-role and Portal/Lab Runtime separation constraints;
7. [`../../STATUS.md`](../../STATUS.md) — project-level current status and cross-front dependencies.

When the selected package needs a concrete learning workload, use:

- [`14-autonomous-agent-rl-track.md`](14-autonomous-agent-rl-track.md) — preferred focused content scenario;
- [`15-implementation-plan.md`](15-implementation-plan.md) — implementation target and vertical-slice gates.

These two documents are **reference constraints, not permission to skip the active Portal stage**. They should make abstract surface decisions concrete without freezing later API/runtime details early.

When a round touches project transfer or generated-project behavior, also read:

- [`08-content-and-runtime-boundaries.md`](08-content-and-runtime-boundaries.md).

Do not override an `ADOPTED` decision from the blueprint or `13-access-and-runtime-boundaries.md` unless the issue explicitly asks to reconsider it.

---

# 2. Round protocol

Every Jules/agent round must follow this sequence.

## Step 1 — Identify the active stage

Read `CURRENT_STAGE` below.

Do not work on later stages.

## Step 2 — Select exactly one eligible work package

Choose one item marked `ELIGIBLE` in the active stage.

Selection priority:

1. prefer an item with no unresolved dependency on Front 1, Front 3, or Front 4;
2. prefer an item that clarifies boundaries needed by multiple later items;
3. prefer an item that reduces the largest current ambiguity in the Portal experience;
4. if still equivalent, choose the lowest item ID.

Do not select an item marked `BLOCKED`, `LOCKED`, or `DONE`.

## Step 3 — Claim the item

Change only the selected item from `ELIGIBLE` to `IN_PROGRESS` while working.

Do not claim multiple work packages in one round.

## Step 4 — Refine the blueprint

Update the relevant section(s) of `11-portal-blueprint.md` with concrete design detail.

A useful refinement should distinguish:

- adopted constraints;
- recommended behavior;
- alternatives considered;
- unresolved trade-offs;
- dependencies on another front;
- major states and transitions when relevant.

Prefer learner-visible behavior and information architecture over implementation detail.

All refinements must preserve the adopted separation between Portal/control-plane responsibilities and Lab Runtime/execution-plane responsibilities. Current Portal IA should be interpreted as the **Learner-facing view** unless a task explicitly expands the role scope.

## Step 5 — Update this tracker

At the end of the round:

- mark the selected item `DONE` if its item-level completion criteria are met;
- otherwise mark it `BLOCKED` and record the exact blocker;
- add a concise entry under `Round log` describing what changed;
- recalculate which remaining items are now `ELIGIBLE`;
- do not silently advance to another stage.

## Step 6 — Stop at the checkpoint

One round ends after one work package.

Do not continue into the next eligible package in the same round.

If every work package in the current stage is `DONE` and all stage exit criteria are satisfied, set the stage status to `READY_FOR_REVIEW` and stop.

A human review must move `CURRENT_STAGE` forward.

---

# 3. Global stop rules

Stop instead of broadening scope when:

- the selected work package requires a product decision owned by Front 3;
- it requires a curriculum/mastery decision not yet available from Front 1;
- it requires a project-integration decision owned by Front 4;
- resolving it would require freezing API, database, evaluator, runner, authorization, or schema contracts before Stage 5;
- the task would require implementation code rather than Portal design documentation;
- two current documents conflict on an `ADOPTED` decision and the conflict cannot be reconciled from existing project context;
- the proposed design collapses the Portal and Lab Runtime into one process, filesystem, deployment, or trust boundary;
- the proposed design requires direct Portal access to arbitrary learner project files or arbitrary learner Python execution;
- the proposed design assumes that content-authoring or platform-administration roles automatically inherit learner project/runtime access.

When blocked, record the dependency explicitly and stop.

---

# 4. Current stage

```text
CURRENT_STAGE: P2-S1
STAGE_STATUS: ACTIVE
```

Portal Front (`P2`) stages:

```text
P2-S1  Information architecture and surface responsibilities   <- CURRENT
P2-S2  Skill Workspace and interaction model
P2-S3  Learner flows and state UX
P2-S4  Progress, mastery, review, and gamification presentation
P2-S5  Runtime and authorization interaction boundary
P2-S6  First-release Portal specification
```

---

# 5. P2-S1 — Information architecture and surface responsibilities

## Goal

Turn the current Portal surface list into a coherent information architecture where each surface has a clear learner purpose, boundaries, entry/exit paths, and relationship to the shared application shell.

This stage does **not** design React components or runtime/auth contracts.

`P2-S1-A` through `P2-S1-C` were completed before the access/runtime boundary was made explicit. They remain valid as learner-facing IA. The final `P2-S1-J` cross-surface review must verify that no completed surface implicitly depends on Portal/Runtime co-location or broad global access.

## Work packages

### P2-S1-A — Shared shell and top-level navigation

**Status:** `DONE`

Define:

- primary navigation model;
- stable shell regions;
- what context persists while the learner moves between surfaces;
- when a full-width/distraction-free workspace is needed;
- where global review/progress/project indicators belong;
- desktop-first information architecture, while noting responsive constraints.

**Done when:** the blueprint contains one recommended shell/navigation model, alternatives/trade-offs, and explicit boundaries for what is global vs surface-local.

### P2-S1-B — Home

**Status:** `DONE`

Define:

- Home's single primary learner goal;
- first-visit state;
- returning-learner state;
- review-needed state;
- project-connected vs project-independent state;
- what actions belong here vs elsewhere;
- whether Home presents one recommended action or several choices.

**Done when:** Home can be described without overlapping materially with Progress, Review Center, or Skill Graph.

### P2-S1-C — Skill Graph

**Status:** `DONE`

Define:

- graph's primary role;
- what node/edge information is visible;
- locked/available/started/acquired/mastered/review states;
- node-detail interaction;
- recommended-path vs free-exploration behavior;
- strategies for a graph that grows large;
- what does not belong in the graph.

**Done when:** the blueprint explains how the learner uses the graph to decide what to learn next without turning it into a linear course list.

### P2-S1-D — Skill Workspace

**Status:** `ELIGIBLE`

Define at IA level only:

- Workspace's primary role;
- relationship between content, practice, checkpoint, notes, hints, and references;
- what belongs inside the Workspace vs Practice Lab;
- entry/continue/resume behavior;
- skill-level navigation boundaries;
- which learner actions conceptually depend on a Lab Runtime capability vs remain Portal-only;
- learner-visible behavior when a required Runtime is unavailable/denied/disconnected, without defining the protocol.

Do not yet design the detailed block/interaction system; that belongs to P2-S2.

**Done when:** the surface boundary is clear enough that P2-S2 can design its internal interaction model without reopening the question of what the Workspace is for or assuming Portal/Runtime co-location.

### P2-S1-E — Practice Lab

**Status:** `ELIGIBLE`

Define:

- why Practice Lab exists separately from Skill Workspace;
- expected level of scaffolding;
- whether activities are skill-bound, branch-bound, challenge-based, project-based, or mixed;
- entry/exit paths;
- relationship to mastery evidence at a conceptual level;
- which experiences require Lab Runtime capability and how runtime-unavailable state is represented at IA level.

**Done when:** the blueprint can distinguish a Skill Workspace activity from a Practice Lab activity using learner intent and scaffolding, not just UI appearance, without assuming execution occurs inside the Portal.

### P2-S1-F — Review Center

**Status:** `ELIGIBLE`

Define:

- Review Center's primary job;
- how review work reaches the learner;
- relationship to Home recommendations;
- skill-specific vs mixed review sessions;
- what belongs here vs Progress/Profile;
- conceptual queue types without freezing the scheduling algorithm.

**Done when:** Review Center has a clear purpose independent of Home and Progress and can support retrieval practice rather than rereading.

### P2-S1-G — Notes

**Status:** `ELIGIBLE`

Define:

- whether Notes is a first-class surface, contextual tool, or both;
- note attachment model at a UX level;
- search/revisit behavior;
- relationship to Skill Workspace and Review;
- boundaries for future AI assistance;
- learner ownership/privacy assumptions at a conceptual level.

**Done when:** the information architecture makes clear where notes are created, where they are revisited, and why a separate Notes surface is or is not necessary.

### P2-S1-H — Progress / Profile

**Status:** `ELIGIBLE`

Define:

- primary learner questions answered by this surface;
- separation of progress, mastery, acquired skills, review state, and XP/achievements;
- history/evidence visibility at a conceptual level;
- what should not become a gamified score optimization surface;
- that learner-owned evidence/progress visibility does not imply cross-user/admin access.

**Done when:** Progress/Profile no longer overlaps ambiguously with Home, Skill Graph, or Review Center and remains conceptually ownership-aware.

### P2-S1-I — Project Context / transfer surface

**Status:** `ELIGIBLE`

Define at Portal IA level:

- whether Project Context is a dedicated surface, contextual mode/panel, or hybrid;
- learner-visible distinction between teaching data and project data;
- where transfer opportunities appear;
- read-only/safe-learning assumptions that must be handed to Front 4;
- learner-visible project permission/access states;
- the requirement that direct filesystem/environment access occurs behind the Lab Runtime/runtime-local Project Adapter boundary rather than inside the Portal process.

Do not decide detailed project adapter/runtime behavior here.

**Done when:** Front 4 receives a clear learner-facing integration requirement rather than an implementation guess, and the IA does not assume Portal-direct project filesystem access.

### P2-S1-J — Cross-surface boundary review

**Status:** `LOCKED`

Unlock only when `P2-S1-A` through `P2-S1-I` are `DONE` or explicitly `BLOCKED` with accepted external dependencies.

Review the complete IA for:

- duplicate responsibilities;
- dead-end navigation;
- unclear entry/exit paths;
- surfaces that should merge;
- missing surface-level responsibilities;
- inconsistent terminology;
- unresolved dependencies on Front 1/3/4;
- implicit assumptions that Portal and Lab Runtime share process, filesystem, deployment, or trust boundary;
- runtime-required actions that have no unavailable/denied state;
- accidental mixing of Learner IA with Content Author/Admin responsibilities.

**Done when:** a learner's primary Portal destinations have distinct jobs, the top-level navigation can be explained coherently end-to-end, and the full IA respects `13-access-and-runtime-boundaries.md`.

---

## P2-S1 stage exit criteria

Set `P2-S1` to `READY_FOR_REVIEW` only when all are true:

- every proposed top-level surface has a single primary learner purpose;
- overlaps between Home, Skill Graph, Skill Workspace, Practice, Review, Notes, Progress, and Project Context are explicitly resolved;
- shared shell/global context responsibilities are defined;
- major entry and exit paths are defined;
- first-visit and returning-user implications are identified where relevant;
- dependencies on Front 1, Front 3, and Front 4 are recorded rather than guessed;
- current IA is explicitly the Learner-facing experience rather than a universal all-role interface;
- runtime-dependent actions can be identified without assuming runtime co-location or permanent availability;
- project access is compatible with a runtime-local/scoped adapter boundary;
- no React component tree, API route, DB schema, evaluator schema, auth model, or runner protocol has been frozen;
- `P2-S1-J` cross-surface review is complete.

**Stage endpoint:** `READY_FOR_REVIEW` — stop and wait for human approval before P2-S2.

---

# 6. P2-S2 — Skill Workspace and interaction model

**Stage status:** `LOCKED`

## Entry condition

Human approval of P2-S1.

## Stage scope

Define:

- Workspace composition model;
- theory/practice continuity;
- reusable interaction primitive vocabulary;
- manual calculation UX;
- prediction-before-run UX;
- Python/code/data execution UX;
- DataFrame/chart/model outputs;
- visualization/simulation embedding;
- hint and feedback affordances;
- interruption/resume behavior;
- distinction between Portal-only interactions and Runtime-required interactions;
- visible unavailable/denied/disconnected runtime states.

## Stage exit criteria

- the Portal can represent the adopted learning sequence without one rigid lesson template;
- each interaction family has a learner action, visible states, and feedback expectations;
- theory, manual work, experiment, code, and interpretation can coexist coherently;
- the boundary between Skill Workspace and Practice Lab remains intact;
- Runtime-required interactions do not assume execution in the Portal process;
- no detailed backend/runner/auth protocol is frozen yet.

**Stage endpoint:** `READY_FOR_REVIEW`.

---

# 7. P2-S3 — Learner flows and state UX

**Stage status:** `LOCKED`

## Entry condition

Human approval of P2-S2.

## Stage scope

Specify end-to-end flows for:

- onboarding/first entry;
- start and continue;
- skill acquisition/unlock;
- failed understanding/remediation;
- review;
- branch/path choice;
- project transfer;
- interruption/resume;
- runtime connection/availability transitions for execution-dependent activities;
- denied/expired project or runtime capability;
- execution cancellation;
- authentication/session recovery where supported by the product mode;
- empty/loading/error/recovery states.

## Stage exit criteria

- every critical journey has a happy path and failure/recovery path;
- no surface becomes a navigation dead end;
- learner error and platform/runtime failure are clearly separated;
- runtime loss/denial can recover without corrupting Portal learning state;
- resume/recovery expectations are explicit;
- unresolved content/product dependencies are recorded.

**Stage endpoint:** `READY_FOR_REVIEW`.

---

# 8. P2-S4 — Progress, mastery, review, and gamification presentation

**Stage status:** `LOCKED`

## Entry condition

Human approval of P2-S3 plus sufficient Front 1/Front 3 decisions.

## Stage scope

Define how the Portal presents:

- progress;
- acquired skills;
- mastery;
- evidence;
- weak/review state;
- misconceptions;
- graph unlocks;
- achievements/XP;
- review recommendations;
- learner ownership/access boundaries for progress/evidence at product-UX level.

## Stage exit criteria

- progress and mastery are not collapsed into one score;
- XP/gamification cannot substitute for competence;
- review does not appear as punishment/loss of achievement;
- the learner can understand why a skill is available, locked, mastered, or due for review;
- visibility of evidence is defined at the product-UX level;
- nothing in the learner UX requires broad cross-user or administrative access.

**Stage endpoint:** `READY_FOR_REVIEW`.

---

# 9. P2-S5 — Runtime and authorization interaction boundary

**Stage status:** `LOCKED`

## Entry condition

Human approval of P2-S4 and sufficient Front 1/4 decisions.

## Stage scope

Only here define detailed Portal-facing contracts for:

- Lab Runtime capability/session negotiation;
- Python execution;
- Evaluator interaction;
- structured execution outputs;
- persistence/state transitions;
- frontend/backend responsibility boundaries;
- sandbox/error presentation;
- project-context execution boundary;
- authorization propagation from Portal to Runtime;
- runtime/session identity and ownership;
- project/dataset capability scope;
- timeout, cancellation, retry, expiration, and revocation;
- local, hosted, and hybrid Runtime compatibility;
- audit/provenance expectations for execution requests/results;
- first-release role/permission enforcement boundary without conflating it with UI visibility.

## Stage exit criteria

- every interaction that requires execution has an explicit responsible subsystem;
- Portal/control-plane and Lab Runtime/execution-plane responsibilities are independently defined;
- structured output families are defined;
- learner error vs platform failure behavior is defined;
- persistence and retry expectations are explicit;
- runtime sessions/capabilities have ownership and scope semantics;
- direct learner project/filesystem access is not required by the Portal process;
- the contract can support local, hosted, and hybrid Runtime topologies without changing curriculum semantics;
- authorization is enforced across service boundaries rather than only through UI state;
- contracts are sufficient for implementation slicing without coupling content to runtime internals.

**Stage endpoint:** `READY_FOR_REVIEW`.

---

# 10. P2-S6 — First-release Portal specification

**Stage status:** `LOCKED`

## Entry condition

Human approval of P2-S5 and alignment with Fronts 1, 3, and 4.

## Stage scope

Consolidate the Portal design into the first implementation-ready release definition.

Define:

- included surfaces;
- included learner flows;
- supported interaction primitives;
- first vertical slice requirements;
- explicit deferred capabilities;
- responsive/accessibility expectations;
- technical ownership boundaries;
- supported first-release roles/access profile(s);
- supported first-release deployment/runtime topology while preserving the local/SaaS/hybrid boundary model;
- safe implementation slices/issues.

## Stage exit criteria

- MVP/first release is bounded;
- included and deferred capabilities are explicit;
- supported roles and access assumptions are explicit;
- Portal and Lab Runtime implementation ownership is separable;
- cross-front dependencies are resolved or deliberately deferred;
- implementation surfaces and ownership boundaries are clear enough to create Jules implementation issues without mechanical task splitting;
- no major Portal UX or trust-boundary decision is left to be invented during implementation.

**Stage endpoint:** `READY_FOR_IMPLEMENTATION_SLICING`.

---

# 11. Round log

Add newest entries first.

| Date | Round | Selected package | Result | Notes |
| --- | --- | --- | --- | --- |
| 2026-09-14 | architecture constraint | cross-cutting | ADOPTED | Added `13-access-and-runtime-boundaries.md`: Portal/control plane and Lab Runtime/execution plane are separate responsibilities in local, SaaS, and hybrid modes; introduced ownership-aware access roles and required later stages/IA review to preserve those boundaries. |
| 2026-09-14 | P2-S1-C | P2-S1-C | DONE | Defined Skill Graph IA (visual decision surface for ML knowledge structure and next-step decisions, default vs inspector visible details, visual/textual representation of 6 adopted states, node detail interactions & lock rationales, recommended path vs free DAG exploration, large-graph usability strategies, strict surface boundaries, entry/exit paths, and external dependencies) in Section 5 of the blueprint. |
| 2026-09-14 | P2-S1-B | P2-S1-B | DONE | Defined Home IA (orientation & momentum launchpad, bounded hybrid recommendation model, learner states, strict surface boundaries, summary-only limits, entry/exit paths, and external dependencies) in Section 4 of the blueprint. |
| 2026-09-14 | P2-S1-A | P2-S1-A | DONE | Refined shared shell and top-level navigation (regions, navigation rail, contextual panel, distraction-free mode, and global vs surface-local boundaries) in Section 2 and 3 of the blueprint. |
| 2026-09-14 | bootstrap | tracker creation | DONE | Created the incremental Portal work protocol and defined stage endpoints. |