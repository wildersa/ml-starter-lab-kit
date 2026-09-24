# Project Status

_Last updated: 2026-09-24_

## Current focus

The current design effort is the new **Learning Portal** for `ml-starter-lab-kit`.

The existing starter generator, generated project structure, labs/workspace, demo datasets, experiment tooling, and optional MLOps capabilities remain intact. The Learning Portal is a separate educational surface in the same ecosystem and should not require a broad refactor of the current UI/runtime.

The goal is to create an interactive ML learning environment where the learner studies theory, practices concepts, receives feedback, builds real competence, and unlocks new skills only when the required knowledge has actually been demonstrated.

Detailed design lives under [`docs/learning-portal/`](docs/learning-portal/README.md).

**Implementation state:** the new Learning Portal is still design/planning only. No React Portal, FastAPI Learning API, or new Lab Runtime has been implemented yet.

Two focused documents now make the implementation target concrete without bypassing the staged design process:

- [`docs/learning-portal/14-autonomous-agent-rl-track.md`](docs/learning-portal/14-autonomous-agent-rl-track.md) — detailed RL/autonomous-agent specialization;
- [`docs/learning-portal/15-implementation-plan.md`](docs/learning-portal/15-implementation-plan.md) — vertical implementation slices and gates.

---

# Program roadmap: four macro work fronts

These are independent work streams that converge later. They are not portal modules.

## Front 1 — Content / pedagogical line

**Purpose:** decide what Machine Learning knowledge belongs in the product and how it should be learned.

**Status:** IN PROGRESS.

### Stages

```text
1. Macro ML knowledge map                    <- CURRENT DEEP RESEARCH
2. Region-by-region refinement
3. Bibliographic/source/licensing research
4. Learning design per region
5. Mastery/evaluation design
6. Consolidated pedagogical Skill Graph
```

### Stage 1 — current research

Goal: establish the high-level architecture of Machine Learning knowledge before deciding final modules or detailed lessons.

Research thread:
- [ChatGPT — ml-starter-lab-kit / Macro ML Knowledge Map](https://chatgpt.com/g/g-p-6a2234c6cdd88191a446f29c401f2ecc-ml-starter-lab-kit/c/6aa77b3c-ce68-83e9-b25b-1c1cc8f5f217)

This stage should identify:

- major knowledge regions;
- real prerequisite relationships;
- minimum ML backbone before specialization;
- topics that can be learned in parallel;
- shared foundations across tracks;
- specialization branches;
- areas where teaching order has weak/conflicting consensus;
- regions requiring focused follow-up research.

It should **not** yet finalize every skill, lesson, exercise, mastery rule, or source/license matrix.

### Important content principle already adopted

Python, data understanding, statistics, probability, and mathematics should enter at the depth and moment needed to understand ML.

They do not need to become long independent prerequisite courses before the learner sees a model. Stage 1 research should help identify where these foundations can be introduced through simple applied ML experiences and revisited later with greater depth.

### Later stages

**Stage 2 — Region refinement:** research each major region independently once Stage 1 defines the real regions.

**Stage 3 — Bibliographic/source research:** find authoritative sources, pedagogical references, open materials, licensing, adaptation rights, attribution, and source restrictions.

**Stage 4 — Learning design:** define theory depth, intuition, worked examples, visualizations, manual executions, experiments, library introduction, exercises, misconceptions, retrieval, and transfer.

**Stage 5 — Mastery/evaluation design:** define pedagogically what evidence proves each competency.

**Stage 6 — Skill Graph consolidation:** reconcile all regions into the final content-side DAG, remove duplicates, normalize prerequisites, identify shared nodes, and define recommended traversals.

---

## Front 2 — Portal / platform

**Purpose:** decide how the educational experience exists technically and visually.

**Status:** BLUEPRINT CREATED; STAGE 1 READY TO REFINE.

Canonical working document:
- [`docs/learning-portal/11-portal-blueprint.md`](docs/learning-portal/11-portal-blueprint.md)

The blueprint already structures:

- portal role and shared application shell;
- Home;
- Skill Graph;
- Skill Workspace;
- Practice Lab;
- Review Center;
- Notes;
- Progress/Profile;
- Project Context / transfer;
- interaction primitive catalog;
- learner flows;
- feedback model;
- execution/error states;
- first-release boundary;
- agent/Jules filling rules.

### Front 2 stages

```text
1. Information architecture + surface responsibilities   <- NEXT FOR FRONT 2
2. Skill Workspace + interaction model
3. Learner flows + state UX
4. Progress/mastery/review presentation
5. Runtime interaction boundary
6. First-release portal specification
```

### Stage 1 — next Front 2 work

For each proposed surface:

- validate whether it should exist independently;
- define its primary learner goal;
- define what belongs there;
- remove overlap with other surfaces;
- define entry/exit paths;
- define main empty/loading/error/returning states;
- identify dependencies on Front 1 or Front 3.

Do **not** yet design React components, API routes, database tables, evaluator schemas, or Python Runner protocols.

Jules/agents should fill **one stage or one bounded surface at a time**, preserving adopted decisions and leaving unresolved alternatives explicitly open.

---

## Front 3 — Product / learning experience

**Purpose:** decide what product we are actually building for the learner, independently of curriculum details and implementation technology.

**Status:** TO DECOMPOSE.

This front must cover:

- primary audience;
- expected starting knowledge;
- onboarding;
- guided path vs learner freedom;
- what “finishing” means;
- what “being proficient” means;
- how progress/mastery are communicated;
- role and limits of gamification;
- review experience;
- abandonment/friction reduction;
- differentiation from a course, Jupyter/Kaggle notebook, documentation site, or LMS;
- MVP definition;
- explicit non-goals.

Next work: break this front into an incremental research/design program similar to Fronts 1 and 2.

---

## Front 4 — Ecosystem / `ml-starter-lab-kit` integration

**Purpose:** decide how the Learning Portal relates to the existing starter kit and generated ML projects.

**Status:** TO DECOMPOSE.

This front must cover:

- how the portal ships with or alongside the starter kit;
- attach/open project behavior;
- project config/metadata access;
- dataset access;
- target/features/demo-scenario integration;
- reuse of experiments, metrics and artifacts;
- transfer of learned skills to the learner's own project;
- installation/distribution;
- local/offline behavior;
- read/write boundaries;
- what remains independent;
- what belongs to starter core vs Learning Portal.

Default principle: **reuse data and capabilities before reusing UI or internal implementation details**.

Next work: break this front into an incremental research/design program similar to Fronts 1 and 2.

---

# Current position

```text
Learning Portal
|
+-- Front 1: Content / pedagogical line
|   +-- Stage 1: Macro ML knowledge map                 <- ACTIVE DEEP RESEARCH
|   +-- Stage 2: Region refinement
|   +-- Stage 3: Bibliographic/source research
|   +-- Stage 4: Learning design
|   +-- Stage 5: Mastery/evaluation
|   +-- Stage 6: Skill Graph consolidation
|
+-- Front 2: Portal / platform
|   +-- Blueprint created
|   +-- Stage 1: Information architecture              <- READY TO REFINE
|   +-- Stage 2: Skill Workspace / interactions
|   +-- Stage 3: Learner flows / state UX
|   +-- Stage 4: Mastery/review presentation
|   +-- Stage 5: Runtime interaction boundary
|   +-- Stage 6: First-release portal spec
|
+-- Front 3: Product / learning experience             <- TO DECOMPOSE
|
+-- Front 4: Ecosystem / integration                   <- TO DECOMPOSE
```

---

# Decisions already made

## Learning methodology

Adopted foundation:

- **Mastery Learning**;
- **Cognitive Load management + Worked Examples + Scaffolding**;
- **Retrieval Practice**;
- **Experiential Learning**;
- **Competency / Skill Graph**.

Gamification may expose XP, badges, acquired skills, branch achievements, and visible graph progression, but XP never replaces mastery.

Default learning progression:

**intuition -> theory -> visualization -> worked example -> guided/manual execution -> prediction -> experiment -> reduced scaffolding -> library abstraction -> realistic application -> mastery checkpoint -> later retrieval -> transfer**

## Skill progression

- A graph node represents a demonstrable competency, not merely a chapter.
- Skills can require multiple prerequisites.
- Completion, acquisition, mastery, and review status are separate concepts.
- A previously acquired skill may later require review without erasing the achievement.
- Knowledge Tracing/BKT is a possible future enhancement, not a first-version requirement.

## Platform direction

Current direction:

- **React + TypeScript** — learner-facing portal;
- **FastAPI + Python** — Learning API/application services;
- **Python Runner** — separate execution boundary for learner code and ML/data activities;
- **Evaluator** — deterministic, structural, algorithm-aware, invariant-based and rubric evaluation;
- **Evidence/Mastery** — progression based on demonstrated competence;
- **SQLite initially** — local learner state;
- **Project Adapter** — narrow integration with generated projects/datasets.

Notebook-like Python cells are supported where useful, but `.ipynb` is not the product shell or canonical learner state.

## Content and copyright

Educational content should be declarative and versionable where practical.

Adapt source material only when licensing explicitly permits it. Protected books/papers may be cited and used as references for original content, but public accessibility alone does not grant adaptation rights.

See [`docs/learning-portal/05-content-sources-and-licensing.md`](docs/learning-portal/05-content-sources-and-licensing.md).

---

# Current proposed implementation proof

The preferred proving workload is now a focused **Reinforcement Learning for autonomous agents** specialization.

It begins with a deliberately small product proof:

```text
reward / return
 -> discounting
 -> MDP
 -> V / Q
 -> Bellman
 -> TD
 -> Q-Learning
 -> function approximation
 -> DQN
```

Later branches extend the same environment family and platform primitives toward:

- partial observability / POMDP;
- memory and belief;
- delayed credit / n-step / TD(lambda);
- model-based planning and rollout;
- options / SMDP / hierarchical policies;
- Behavior Trees and hybrid agent architecture.

This specialization is a **reference vertical slice**, not the center of the global ML curriculum. It exists to force concrete decisions about Skill Workspace, Practice Lab, Runtime execution, evidence, mastery and review while keeping the platform reusable for other ML regions.

Implementation sequencing is canonicalized in [`docs/learning-portal/15-implementation-plan.md`](docs/learning-portal/15-implementation-plan.md).

---

# Immediate next steps

1. **Front 1:** keep the global ML knowledge map broad; use the autonomous-agent RL track as a detailed refinement of one region, not as the root of the curriculum.
2. **Front 2:** finish P2-S1 information architecture, using the RL track as the concrete scenario for Skill Workspace, Practice Lab, Review, Progress and runtime-unavailable states.
3. **Front 2 later stages:** use the same track to validate interaction primitives, learner flows, mastery/review presentation and finally the Portal/Runtime contract.
4. **Implementation gate:** once the staged design reaches implementation readiness, start with the Portal-only Bellman vertical slice before adding a separate Runtime.
5. **Runtime proof:** add deterministic RL simulation first, then controlled Python execution, then Q-Learning/DQN experiments.
6. **Fronts 3/4:** continue decomposing product experience and ecosystem integration without making them depend on RL-specific assumptions.

Do not freeze universal `Skill`, `Activity`, `Evaluation`, `Evidence`, database, API or Runner contracts earlier than the design stages permit. The implementation plan defines minimum concepts to prove, not a final universal schema.

---

# Out of scope for the current Learning Portal

The separate idea of using ML inside game/minigame scenarios is intentionally **not** part of this Learning Portal design. It may become another project later.