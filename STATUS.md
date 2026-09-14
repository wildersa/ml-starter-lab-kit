# Project Status

_Last updated: 2026-09-14_

## Current focus

The current design effort is the new **Learning Portal** for `ml-starter-lab-kit`.

The existing starter generator, generated project structure, labs/workspace, demo datasets, experiment tooling, and optional MLOps capabilities remain intact. The Learning Portal is a separate educational surface in the same ecosystem and should not require a broad refactor of the current UI/runtime.

The goal is to create an interactive ML learning environment where the learner studies theory, practices concepts, receives feedback, builds real competence, and unlocks new skills only when the required knowledge has actually been demonstrated.

Detailed design lives under [`docs/learning-portal/`](docs/learning-portal/README.md).

---

## Program roadmap: four macro work fronts

The Learning Portal effort is divided into **four macro work fronts**. These are the main streams of work for the project; they are not portal modules and should not be collapsed into one implementation plan too early.

### Front 1 — Content / pedagogical line

**Purpose:** decide what Machine Learning knowledge belongs in the product and how it should be learned.

This front covers:

- macro knowledge map;
- prerequisite relationships;
- applied foundations;
- curriculum and learning paths;
- theory depth;
- where mathematics/statistics/programming enter;
- authoritative sources;
- source licensing and attribution;
- examples and datasets;
- manual calculation vs visualization/simulation;
- when libraries are introduced;
- exercises and practice;
- misconceptions;
- retrieval/review;
- transfer to other contexts;
- pedagogical mastery/evaluation criteria.

**Status:** IN PROGRESS.

The current Deep Research is only the **first step of this front**.

### Front 2 — Portal / platform

**Purpose:** decide how the educational experience exists technically and visually.

This front covers:

- information architecture;
- Home;
- Skill Graph;
- Skill Workspace;
- Practice/Lab;
- Review Center;
- Notes;
- Progress/Profile;
- navigation and learner flow;
- theory/formula rendering;
- manual-calculation interactions;
- visualizations and simulations;
- Python/code cells;
- DataFrame/chart/model outputs;
- hints and feedback;
- FastAPI services;
- Python Runner;
- Evaluator;
- persistence;
- evidence/mastery implementation;
- sandbox/execution boundaries;
- frontend/backend contracts.

**Status:** NOT YET DECOMPOSED.

The next work here is to define the portal surfaces and learner flow before freezing schemas, APIs, or runner contracts.

### Front 3 — Product / learning experience

**Purpose:** decide what product we are actually building for the learner, independently of curriculum details and implementation technology.

This front covers:

- primary audience;
- expected starting knowledge;
- onboarding;
- guided path vs learner freedom;
- what “finishing” means;
- what “being proficient” means;
- how progress is communicated;
- how mastery is communicated;
- role and limits of gamification;
- review UX;
- abandonment/friction reduction;
- what differentiates the product from a course, Jupyter notebook, Kaggle notebook, documentation site, or LMS;
- MVP scope;
- explicit non-goals.

**Status:** NOT YET DECOMPOSED.

### Front 4 — Ecosystem / `ml-starter-lab-kit` integration

**Purpose:** decide how the Learning Portal relates to the existing starter kit and generated ML projects.

This front covers:

- how the portal ships with or alongside the starter kit;
- how it opens/attaches to a generated project;
- project metadata/config consumption;
- dataset access;
- target/features/demo scenario integration;
- reuse of experiments, metrics, and artifacts;
- transfer of learned skills to the learner’s own project;
- installation/distribution;
- local/offline behavior;
- what stays independent;
- what belongs to the starter core vs Learning Portal;
- how to avoid refactoring the existing workspace/runtime unnecessarily.

**Status:** NOT YET DECOMPOSED.

Default principle: **reuse data and capabilities before reusing UI or internal implementation details**.

---

## Current position

```text
Learning Portal
|
+-- Front 1: Content / pedagogical line       <- ACTIVE
|   +-- Stage 1: Macro ML knowledge map       <- CURRENT DEEP RESEARCH
|   +-- Stage 2: Region-by-region refinement
|   +-- Stage 3: Bibliographic/source research
|   +-- Stage 4: Learning design per region
|   +-- Stage 5: Mastery/evaluation design
|   +-- Stage 6: Consolidated pedagogical Skill Graph
|
+-- Front 2: Portal / platform                <- TO DECOMPOSE
+-- Front 3: Product / learning experience    <- TO DECOMPOSE
+-- Front 4: Ecosystem / integration          <- TO DECOMPOSE
```

The current research does **not** cover the Learning Portal project as a whole. It covers only the beginning of **Front 1**.

---

## Front 1 research program

### Stage 1 — Macro ML knowledge map — CURRENT

Goal: establish the high-level architecture of Machine Learning knowledge before deciding modules or detailed lessons.

The research should identify:

- major knowledge regions;
- real prerequisite relationships;
- the minimum ML backbone before specialization;
- topics that can be learned in parallel;
- shared foundations across tracks;
- specialization branches;
- areas where teaching order has weak/conflicting consensus;
- topics that deserve dedicated follow-up research.

Research thread:
- [ChatGPT — ml-starter-lab-kit / Macro ML Knowledge Map](https://chatgpt.com/g/g-p-6a2234c6cdd88191a446f29c401f2ecc-ml-starter-lab-kit/c/6aa77b3c-ce68-83e9-b25b-1c1cc8f5f217)

This stage must **not** attempt to finalize modules, every individual skill, exercises, mastery rules, or a complete bibliography/license matrix.

### Stage 2 — Region-by-region refinement

After the macro map is reviewed, research each major region independently and in greater depth.

Examples may include:

- applied ML foundations;
- classical/supervised ML;
- unsupervised learning;
- deep learning;
- reinforcement learning/bandits;
- time series;
- computer vision;
- NLP;
- recommendation systems;
- experimentation/MLOps;
- responsible ML.

The exact regions should come from Stage 1 rather than being frozen beforehand.

### Stage 3 — Bibliographic/source research

Once a region is sufficiently stable, identify the material we can use to build it.

For each region/skill family, determine:

- authoritative/primary references;
- strong pedagogical references;
- open educational material when available;
- official library/documentation sources;
- licensing;
- whether content may be adapted or should only be cited/referenced;
- attribution/share-alike requirements;
- sources to avoid because licensing or authority is weak/unclear.

Bibliographic/licensing research is deliberately **after** the first content-map work so effort is spent on sources we are actually likely to use.

### Stage 4 — Learning design per region

Turn the researched knowledge structure and sources into teachable experiences.

Define:

- theory depth;
- intuition;
- worked examples;
- visualizations;
- manual executions when useful;
- simulations/experiments;
- when libraries appear;
- practical exercises;
- common misconceptions;
- retrieval practice;
- transfer exercises.

### Stage 5 — Mastery/evaluation design

Define how the learner demonstrates each kind of competency.

Possible mechanisms include:

- deterministic checks;
- numerical tolerance;
- structural checks;
- invariants;
- hidden evaluation datasets;
- baseline comparison;
- interpretation/rubrics;
- multiple pieces of evidence.

This is pedagogical evaluation first; the technical Evaluator implementation belongs to Front 2.

### Stage 6 — Consolidated pedagogical Skill Graph

After the regions are researched, sourced, and designed, reconcile them into the actual learning graph:

- remove duplicated skills;
- normalize prerequisite relationships;
- identify shared foundation nodes;
- decide recommended traversals;
- preserve alternative paths where valid;
- mark specializations;
- connect review/transfer requirements;
- produce the content-side contract that Front 2 can implement.

---

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

### Foundations should not become prerequisite courses by default

Python, data understanding, statistics, probability, and mathematics should enter at the depth and moment needed to understand Machine Learning.

They do not need to be isolated into long preparatory modules before the learner sees a model. Stage 1 research should help identify where these foundations can be introduced inside simple applied ML experiences and revisited later at greater depth.

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

---

## Current proposed first implementation proof

A small Reinforcement Learning path remains a useful candidate for a later vertical slice because it exercises theory, formulas, intermediate calculations, visualization, mastery, and graph dependencies:

```text
RL vocabulary
 -> Return and discounting
 -> MDP
 -> Value functions
 -> Bellman equation
```

A small GridWorld can be reused where appropriate.

This is **not the current task** and should not constrain Stage 1 research into making RL the center of the overall curriculum.

---

## Immediate next steps

### Now

Complete **Front 1 / Stage 1 — Macro ML Knowledge Map** and review the research result.

The review should decide:

- whether the macro knowledge regions are correct;
- whether prerequisite relationships make sense;
- whether the proposed backbone is appropriate;
- where foundations can be integrated into applied ML;
- which region should receive the next focused research.

### Next project-design session

Decompose **Fronts 2, 3, and 4** with the same level of clarity currently being developed for Front 1:

- subfronts/topics;
- decisions already made;
- open questions;
- dependencies;
- expected deliverables;
- what must be resolved before implementation.

Do not freeze `Skill`, `Activity`, `Evaluation`, `Evidence`, database, API, or runner contracts before the four fronts are sufficiently understood.

---

## Not part of the current Learning Portal scope

The separate idea of using ML inside game/minigame scenarios is intentionally **not** part of this Learning Portal design. It may become another project later.
