# Project Status

_Last updated: 2026-09-14_

## Current focus

The current design effort is the new **Learning Portal** for `ml-starter-lab-kit`.

The existing starter generator, generated project structure, labs/workspace, demo datasets, experiment tooling, and optional MLOps capabilities remain intact. The Learning Portal is a separate educational surface in the same ecosystem and should not require a broad refactor of the current UI/runtime.

The goal is to create an interactive ML learning environment where the learner studies theory, practices concepts, receives feedback, builds real competence, and unlocks new skills only when the required knowledge has actually been demonstrated.

Detailed design lives under [`docs/learning-portal/`](docs/learning-portal/README.md).

## Decisions already made

### Learning methodology

The adopted methodology is:

- **Mastery Learning** — progression depends on demonstrated competence, not lesson completion;
- **Cognitive Load management + Worked Examples + Scaffolding** — begin with bounded examples and progressively remove assistance;
- **Retrieval Practice** — review requires recalling/applying knowledge instead of simply rereading;
- **Experiential Learning** — prefer `predict -> execute -> observe -> explain` when a concept has observable behavior;
- **Competency / Skill Graph** — learning is represented as a graph of real prerequisite relationships rather than one rigid linear course.

Gamification may expose XP, badges, acquired skills, branch achievements, and visible graph progression, but XP never replaces mastery.

The default lesson progression is:

**intuition -> theory -> visualization -> worked example -> guided/manual execution -> prediction -> experiment -> reduced scaffolding -> library abstraction -> realistic application -> mastery checkpoint -> later retrieval -> transfer**

### Skill progression

- A graph node represents a demonstrable competency, not merely a chapter.
- Skills can require multiple prerequisite skills.
- Completion, acquisition, mastery, and review status are separate concepts.
- A previously acquired skill may later require review without erasing the achievement.
- Knowledge Tracing/BKT is a possible future enhancement, not a requirement for the first version.

### Platform direction

The Learning Portal will be a dedicated web application rather than Jupyter/Streamlit as the primary product shell.

Current technical direction:

- **React + TypeScript** — learner-facing portal;
- **FastAPI + Python** — Learning API and application services;
- **Python Runner** — separate execution boundary for learner code and ML/data activities;
- **Evaluator** — deterministic, structural, algorithm-aware, invariant-based, and rubric evaluation;
- **Evidence/Mastery** — progression should be based on proof of competence;
- **SQLite initially** — learner state, notes, attempts, review, progress and evidence;
- **Project Adapter** — narrow integration with generated projects/datasets without coupling learning content to generator internals.

The portal may provide notebook-like Python cells with inline execution, but `.ipynb` is not the product shell or canonical learner state.

### Content and copyright

Educational content should be declarative and versionable where practical.

The project may adapt sources only when licensing explicitly permits it and attribution/share-alike requirements are respected. Protected books and papers may be cited and used as references for original explanations, but their text, figures, and exercises should not be copied merely because they are publicly accessible.

The current source/licensing policy is documented in [`docs/learning-portal/05-content-sources-and-licensing.md`](docs/learning-portal/05-content-sources-and-licensing.md).

## Work fronts

The project should now be advanced through four **macro work fronts**. These are not portal modules; they are separate streams of product/design work that can evolve largely in parallel and meet later.

### 1. Content / pedagogical line

Owns **what is taught and how learning is structured**.

This front must define:

- what ML knowledge belongs in the product;
- curriculum order and prerequisite relationships;
- theory and learning-science basis;
- authoritative/reference sources;
- source licensing and attribution rules;
- examples and datasets used for teaching;
- where manual calculation is pedagogically useful;
- where visualization/simulation is preferable;
- when standard libraries are introduced;
- exercise types;
- how understanding should be evaluated pedagogically;
- what counts as sufficient mastery for each type of competency;
- review/retrieval strategy;
- misconception handling;
- transfer from controlled examples to real datasets/projects.

This front produces the actual **learning design and skill graph content**.

### 2. Portal / platform

Owns **how the educational product is materialized technically and visually**.

This front includes the entire portal/platform concern:

- information architecture;
- Home;
- Skill Graph;
- Skill Workspace;
- Practice/Lab surfaces;
- Review Center;
- Notes;
- Progress/Profile;
- navigation and learner flow;
- formula and manual-calculation interactions;
- visualizations and simulations;
- Python/code cells;
- DataFrame/chart/model output rendering;
- hints and feedback;
- FastAPI services;
- Python Runner;
- Evaluator;
- persistence;
- evidence/mastery implementation;
- sandbox/execution boundaries;
- frontend/backend contracts.

The next work in this front is not yet schema design. First define **what the portal contains, how each surface behaves, and how the learner moves through it**.

### 3. Product / learning experience

Owns **what product we are actually building for the learner**, independent of curriculum details and implementation technology.

This front must define:

- primary audience(s);
- expected starting knowledge;
- onboarding experience;
- how a learner chooses or receives a learning path;
- how much freedom vs guidance the product provides;
- what “finishing” means;
- what “being proficient” means at product level;
- how progress is communicated;
- how mastery is communicated without making the product feel punitive;
- role and limits of gamification;
- how to reduce abandonment/friction;
- how review is surfaced to the learner;
- what differentiates the product from a course, Jupyter notebook, Kaggle notebook, documentation site, or LMS;
- scope of the first useful release/MVP;
- explicit non-goals.

This front should keep the product coherent while Content and Portal evolve independently.

### 4. Ecosystem / `ml-starter-lab-kit` integration

Owns **how the Learning Portal relates to the existing project and generated ML projects**.

This front must define:

- whether/how the portal ships with the starter kit;
- how it opens or attaches to a generated project;
- how it consumes project configuration and metadata;
- how it uses the learner's dataset safely;
- how target/features/demo scenario are exposed;
- how experiment outputs and artifacts can be reused;
- how a learned skill is transferred to the learner's real project;
- installation/distribution model;
- offline/local behavior;
- which boundaries must remain independent;
- what stays in the starter core vs Learning Portal;
- how to avoid forcing a refactor of the current workspace/runtime.

The default architectural principle remains: **reuse data and capabilities before reusing UI or internal implementation details**.

## Current proposed first vertical slice

A small Reinforcement Learning path is still a useful candidate for the first implementation proof because it exercises theory, formulas, intermediate calculations, visualization, mastery and graph dependencies:

```text
RL vocabulary
 -> Return and discounting
 -> MDP
 -> Value functions
 -> Bellman equation
```

A small GridWorld can be reused where appropriate.

However, this is **not the immediate next task**. The four work fronts must first be decomposed enough to confirm the product, learning, portal, and integration requirements before implementation contracts are frozen.

## What is still missing

The project has a strong direction but the four fronts are still too broad.

Before opening implementation issues, each front needs to be broken into smaller research/design topics, decisions, dependencies, and concrete outputs.

Examples of later questions include:

- exact curriculum and skill graph;
- exact portal surfaces and navigation model;
- exact learner journey and MVP experience;
- exact integration boundary with generated projects;
- only after those are clearer: content schemas, activity/evaluation contracts, persistence models, runner contracts, and implementation slicing.

## Immediate next step

**Break down each of the four work fronts.**

For each front, define:

1. subfronts / topics that must be researched or designed;
2. decisions already made;
3. open questions;
4. dependencies on another front;
5. concrete deliverables/documents expected from that front;
6. what must be resolved before implementation can begin.

Do this before designing the detailed `Skill`, `Activity`, `Evaluation`, `Evidence`, database, or API contracts.

The immediate continuation point is therefore:

```text
1. Content / pedagogical line
2. Portal / platform
3. Product / learning experience
4. Ecosystem / ml-starter-lab-kit integration

-> decompose each front
-> identify research/decisions/deliverables
-> then converge the fronts
-> only then freeze implementation contracts and open implementation issues
```

## Not part of the current Learning Portal scope

The separate idea of using ML inside game/minigame scenarios is intentionally not part of this current portal design. It may become another project later.
