# Learning Portal blueprint

## Status

This document is the working skeleton for **Front 2 — Portal / platform**.

It defines the portal surfaces, responsibilities, major flows, interaction primitives, and the questions that still need to be researched or designed.

It is intentionally **not** a component specification, API contract, database schema, or implementation plan yet.

Use the following markers while refining this document:

- **ADOPTED** — already decided and should be treated as a product constraint;
- **PROPOSED** — current direction, still open to refinement;
- **OPEN** — unresolved and should be researched/designed before implementation;
- **LATER** — explicitly deferred beyond the first useful release.

The portal should be refined incrementally. Jules or another agent may fill one section at a time, but should not silently convert open questions into product decisions.

---

# 1. Portal role

**ADOPTED**

The Learning Portal is the learner-facing environment for studying Machine Learning, practicing it interactively, receiving feedback, revisiting weak concepts, and seeing skills become available as competence is demonstrated.

It is a dedicated web application. Jupyter and Streamlit are not the primary product shell.

The portal must support the adopted learning model without forcing every learning activity into the same UI pattern.

Core experience:

```text
orient -> learn -> interact -> practice -> receive feedback -> demonstrate -> unlock -> review -> transfer
```

The portal should feel like an **interactive learning/work environment**, not a traditional LMS organized only as `module -> lesson -> next`.

---

# 2. Global information architecture

## Primary surfaces

Current portal skeleton:

```text
Home
Skill Graph
Skill Workspace
Practice Lab
Review Center
Notes
Progress / Profile
Project Context
```

These names are working names. Their responsibilities should remain separate even if navigation labels change later.

## Navigation model

**PROPOSED**

Persistent primary navigation should make it easy to answer:

- Where am I now?
- What can I learn next?
- What needs review?
- Where can I practice freely?
- Where are my notes?
- What have I actually mastered?

**OPEN**

- desktop navigation shape: sidebar, top navigation, hybrid;
- mobile/responsive behavior;
- whether `Project Context` is a first-class navigation item or contextual mode;
- whether `Practice Lab` is always visible or only appears after relevant skills are acquired.

---

# 3. Shared application shell

## Purpose

Provide stable navigation and context while the central workspace changes between theory, exercises, simulations, code, review, and project transfer.

## Proposed regions

### Primary navigation

May contain:

- Home;
- Skill Graph;
- Practice;
- Review;
- Notes;
- Progress.

### Main workspace

The active learner task occupies the majority of the screen.

It may render:

- explanatory content;
- formulas;
- interactive diagrams;
- tables;
- manual calculation tools;
- code cells;
- DataFrames;
- charts;
- simulations;
- checkpoints;
- review activities.

### Context panel

**PROPOSED**

A contextual side panel may expose, depending on the current activity:

- learner notes;
- skill progress;
- prerequisites;
- related concepts;
- hints;
- glossary terms;
- references;
- current project context.

The context panel should reduce unnecessary navigation away from the active learning task.

**OPEN**

- which contextual functions deserve permanent visibility;
- whether notes and hints share a panel or use separate affordances;
- how much screen space code/data activities need;
- whether the shell supports distraction-free/full-width activity mode.

---

# 4. Home

## Purpose

The Home surface should orient the learner immediately.

It should answer:

1. What am I learning now?
2. What can I do next?
3. What should I review?
4. Is there anything important from my current project that I can practice against?

## Candidate blocks

**PROPOSED**

- Continue current skill;
- recommended next skill;
- skills needing review;
- current learning path / branch;
- recent progress;
- recent notes;
- optional current-project transfer opportunity.

## States to design

**OPEN**

- first visit / no progress;
- active learner;
- all currently available skills completed;
- review backlog exists;
- user opened portal from a generated project;
- user opened portal without a project.

## Questions to resolve

**OPEN**

- Is Home primarily a dashboard or a recommendation surface?
- Should there be one strongly recommended next action or several choices?
- How prominently should review compete with new learning?
- What does the first-run Home show before a path exists?

---

# 5. Skill Graph

## Purpose

The Skill Graph is the learner's visual map of Machine Learning knowledge.

It must make progression and dependency visible rather than presenting an opaque course list.

## Required concepts

**ADOPTED**

The graph must distinguish at least:

- locked;
- available;
- started;
- acquired;
- mastered;
- needs review.

It should show real prerequisite edges and explain why a locked skill is unavailable.

## Core interactions

**PROPOSED**

Selecting a node should expose:

- skill purpose;
- current status;
- prerequisite skills;
- why it is locked, when applicable;
- mastery/progress state;
- concepts it unlocks;
- option to start/continue/review when available.

## Graph views to investigate

**OPEN**

- full ML map;
- recommended path focus;
- specialization/branch focus;
- weak/review overlay;
- completed-only / progress view;
- project-relevant skills overlay.

## Questions to resolve

**OPEN**

- how much of the future graph is visible initially;
- whether distant advanced skills are visible but locked;
- how to keep a large graph usable;
- whether branches collapse/expand;
- how recommended paths are represented without turning the DAG back into a fixed course;
- how graph updates/unlocks are animated without becoming distracting gamification.

---

# 6. Skill Workspace

## Purpose

The Skill Workspace is the **main learning surface**.

A skill should not be rendered as one long article. The workspace must compose different learning interactions according to what the concept needs.

## Default learning sequence

**ADOPTED**

The pedagogy may use this sequence where appropriate:

```text
why / intuition
-> theory
-> visualization
-> worked example
-> guided/manual execution
-> prediction
-> experiment
-> reduced scaffolding
-> library/tool abstraction
-> realistic application
-> mastery checkpoint
-> later retrieval
-> transfer
```

A specific skill may omit steps that do not add pedagogical value.

## Workspace blocks

The workspace needs a reusable vocabulary of blocks rather than one hard-coded lesson template.

### Content blocks

**PROPOSED**

- explanation/text;
- definition/concept;
- formula;
- callout / misconception;
- worked example;
- reference/further reading;
- glossary link.

### Interactive blocks

**PROPOSED**

- numeric/formula input;
- structured step-by-step calculation;
- table/grid interaction;
- slider/parameter control;
- drag/manipulation interaction;
- visualization;
- simulation;
- prediction-before-run prompt;
- short written interpretation.

### Code/data blocks

**ADOPTED DIRECTION**

- editable Python cell;
- run action;
- inline structured result;
- stdout/error presentation;
- DataFrame preview;
- chart output;
- model/metric result;
- evaluator feedback.

The notebook interaction model may be used, but `.ipynb` state is not the canonical product model.

## Progress within a skill

**OPEN**

Need to decide whether a skill appears as:

- one continuous scroll/canvas;
- explicit stages/steps;
- hybrid sections with free navigation;
- adaptive sequence based on demonstrated understanding.

Also resolve:

- which completed blocks remain editable/re-runnable;
- how returning to an unfinished skill works;
- when checkpoint access becomes available;
- whether learners may intentionally skip explanatory blocks.

---

# 7. Practice Lab

## Purpose

The Practice Lab should provide a less guided environment than the Skill Workspace.

The Skill Workspace teaches and scaffolds. The Practice Lab asks the learner to combine or independently apply acquired skills.

## Possible uses

**PROPOSED**

- open dataset exploration;
- multi-step ML problems;
- code/data experimentation;
- comparing models;
- modifying parameters and interpreting outcomes;
- challenge exercises;
- practice using the learner's current project.

## Relationship to skills

**OPEN**

Determine whether Practice Lab experiences are:

- attached to specific skills;
- attached to branches;
- independent challenge packs;
- generated from project context;
- some combination of the above.

## Questions to resolve

**OPEN**

- how much scaffolding remains;
- whether hints are available;
- whether practice affects mastery;
- whether failures are stored as evidence or only practice history;
- how a learner knows which skills are being exercised.

---

# 8. Review Center

## Purpose

Review is an active learning surface, not a list of lessons to reread.

It should prioritize retrieval, changed examples, misconceptions, and weak prerequisite knowledge.

## Candidate queues

**PROPOSED**

- skills marked `needs review`;
- repeated misconception;
- weak prerequisite blocking a desired skill;
- time since last successful retrieval;
- manually requested review;
- failed transfer/application activity.

## Review interaction types

Possible forms:

- recall question;
- changed numerical example;
- diagnosis task;
- quick calculation;
- compare/contrast concepts;
- new dataset/context;
- explain a previous misconception.

## Questions to resolve

**OPEN**

- how review priority is calculated initially;
- whether review is scheduled or recommendation-based;
- what happens to mastery after failed review;
- how review is presented without feeling punitive;
- whether review sessions should be short mixed sets or skill-specific sessions.

---

# 9. Notes

## Purpose

Notes represent the learner's own knowledge, not curriculum source content.

## Per-skill note model

**PROPOSED**

Suggested prompts:

- My explanation;
- What I did not understand;
- My example;
- Mistakes I made;
- Summary.

Free-form notes should also be possible.

## Portal behavior

**OPEN**

- notes inline in Skill Workspace vs centralized Notes surface;
- search/tagging;
- links from notes back to skills/activities;
- whether notes can attach to a formula, output, chart, or failed attempt;
- later LLM-assisted summarization or recall-question generation.

Original learner notes must remain preserved if AI assistance is added later.

---

# 10. Progress / Profile

## Purpose

Show competence development without reducing learning to XP or completion percentage.

## Distinct concepts

**ADOPTED**

Do not collapse these into one score:

- progress;
- acquired skills;
- mastery;
- review status;
- achievements/XP when enabled.

## Candidate views

**PROPOSED**

- acquired/mastered skills;
- branch/specialization progress;
- skills needing review;
- activity/evidence history;
- misconceptions improved/resolved;
- achievements;
- transfer/application history.

## Questions to resolve

**OPEN**

- whether numeric mastery percentages are useful or falsely precise;
- what the learner should see about evidence;
- what progress visualization encourages learning rather than point optimization;
- whether there is a public/shareable profile later.

---

# 11. Project Context / transfer

## Purpose

Connect learned concepts to a generated `ml-starter-lab-kit` project without making project integration mandatory for basic learning.

## Candidate capabilities

**PROPOSED**

When a project is connected, the portal may expose:

- dataset identity/path;
- target/features;
- demo scenario;
- project config;
- metrics;
- experiment artifacts;
- relevant learning opportunities.

Examples:

- apply EDA skill to current dataset;
- identify target/features;
- create a baseline;
- calculate current project metrics;
- inspect leakage risk;
- interpret feature importance;
- connect project experiments to MLOps skills.

## Questions to resolve

**OPEN**

- whether project context is a mode, panel, or dedicated surface;
- when transfer becomes available;
- how controlled teaching data and learner data are visibly distinguished;
- read-only vs write actions against the project;
- how to prevent educational experiments from damaging project artifacts.

Detailed integration ownership belongs to Front 4.

---

# 12. Interaction primitive catalog

Front 2 should define a reusable catalog of learner interactions before implementing individual skills.

Initial candidate primitives:

```text
content_text
formula
worked_example
numeric_input
multi_step_calculation
choice
short_text
prediction_prompt
table_grid
parameter_control
interactive_visualization
simulation
python_cell
dataframe_output
chart_output
model_output
checkpoint
hint
feedback
note
reference
```

This list is **PROPOSED**, not yet a schema.

The purpose is to ensure the portal can express varied learning experiences without creating a custom application for every skill.

**OPEN**

For each primitive eventually define:

- learner action;
- visual behavior;
- possible states;
- feedback behavior;
- accessibility expectations;
- whether execution is local UI, backend, Python Runner, or evaluator-assisted;
- what evidence it may produce.

---

# 13. Cross-surface learner flows

The portal must eventually document complete journeys, not only screens.

## Flow A — first-time learner

```text
enter portal
-> orient/onboard
-> determine starting point
-> see initial graph/path
-> start first skill
-> complete first learning interaction
-> receive feedback
-> acquire/unlock first meaningful progression
```

## Flow B — returning learner

```text
Home
-> continue current skill OR review weak skill OR choose available branch
```

## Flow C — skill acquisition

```text
Skill Workspace
-> checkpoint/evidence
-> mastery decision
-> skill acquired
-> graph changes
-> next choices explained
```

## Flow D — failed/weak understanding

```text
activity/checkpoint
-> specific feedback
-> misconception/hint/remediation
-> retry or alternate activity
-> later review if needed
```

## Flow E — review

```text
Home/Review Center
-> retrieval activity
-> result
-> mastery/review state update
-> return to current learning path
```

## Flow F — project transfer

```text
acquired skill
-> suitable project context detected
-> transfer activity
-> run against learner project/data
-> feedback/evidence
-> return to learning path or Practice Lab
```

**OPEN**

Each flow must later be expanded with success, error, interruption, resume, and no-data states.

---

# 14. Feedback model

## Principles

**ADOPTED DIRECTION**

Feedback should explain the learning-relevant difference between the learner result and the expected behavior whenever possible.

Avoid reducing every activity to green/red correctness.

Possible feedback layers:

- immediate correctness/result;
- intermediate-step feedback;
- misconception-specific explanation;
- hint progression;
- comparison against baseline/expected behavior;
- what to inspect next;
- whether the result contributes to mastery.

## Questions to resolve

**OPEN**

- when feedback is immediate vs delayed until submission;
- whether learners can inspect expected solutions before retrying;
- how hint usage affects mastery or only XP;
- how to handle multiple valid solutions;
- how semantic/LLM feedback is visually distinguished from deterministic evaluation.

---

# 15. Error and execution states

The portal must distinguish learning failure from platform failure.

## Examples

Learner errors:

- incorrect calculation;
- invalid model result;
- misconception;
- Python exception caused by learner code.

Platform/runtime errors:

- runner unavailable;
- timeout;
- dependency unavailable;
- evaluator failure;
- project file unavailable.

**OPEN**

Design clear states for:

- loading;
- running;
- success;
- learner error;
- validation feedback;
- timeout;
- infrastructure error;
- retry;
- lost/disconnected project context.

The learner should not lose notes, progress, or previous attempts because an execution service fails.

---

# 16. First-release boundary

The first release does not need every surface at full maturity.

**OPEN — must be decided after Fronts 1 and 3 progress further**

Potential first-release minimum:

- Home/orientation;
- Skill Graph;
- Skill Workspace;
- notes;
- a small interaction primitive set;
- deterministic feedback;
- progress/mastery display;
- simple Review entry point;
- first learning vertical slice.

Practice Lab, deep project integration, sophisticated recommendations, adaptive sequencing, advanced analytics, and social features may be staged later.

---

# 17. Front 2 research/design stages

This is the recommended incremental program for filling this blueprint.

## Stage 1 — Information architecture and surface responsibilities

Define and validate:

- portal surfaces;
- what belongs to each surface;
- navigation model;
- shared shell;
- boundaries between Skill Workspace, Practice, Review, Notes, Progress, and Project Context.

**Current document provides the initial skeleton for this stage.**

## Stage 2 — Skill Workspace and interaction model

Define:

- lesson/workspace composition;
- block/interaction vocabulary;
- theory/practice continuity;
- code/data execution UX;
- manual calculation UX;
- visualization/simulation embedding;
- hints;
- feedback;
- interruption/resume.

## Stage 3 — Learner flows and state UX

Define complete flows for:

- onboarding;
- start/continue;
- acquire/unlock;
- remediation;
- review;
- branch selection;
- project transfer;
- errors/recovery.

## Stage 4 — Progress, mastery, and review presentation

Define how the learner sees:

- progress;
- mastery;
- evidence;
- weak skills;
- review;
- achievements/gamification;
- graph changes.

This stage consumes pedagogical decisions from Front 1 and product decisions from Front 3.

## Stage 5 — Runtime interaction boundary

Only after the learner experience is clear, define the detailed portal/runtime contracts for:

- Python Runner;
- Evaluator;
- structured outputs;
- persistence;
- execution state;
- frontend/backend boundaries;
- sandbox/error UX.

This stage refines `10-platform-architecture.md`; it should not be used to dictate earlier UX decisions.

## Stage 6 — First-release portal specification

Consolidate the approved design into an implementable first-release spec:

- included surfaces;
- included flows;
- supported interaction primitives;
- explicit deferred capabilities;
- responsive/accessibility requirements;
- implementation ownership boundaries.

Only then should Front 2 be sliced into implementation issues.

---

# 18. Jules / agent filling rules

When using Jules or another agent to refine this blueprint:

1. Work on **one stage or one surface at a time**.
2. Preserve `ADOPTED` decisions unless the task explicitly asks to reconsider them.
3. Do not convert an `OPEN` question into a final decision without giving rationale/evidence.
4. Do not design database/API/component schemas unless working on Stage 5 or later.
5. Do not let current React/FastAPI implementation convenience dictate the learning UX.
6. Distinguish research findings, product recommendations, and final decisions.
7. Prefer concrete learner flows and states over generic UX advice.
8. Avoid copying patterns from LMS products when they conflict with the Skill Graph/mastery model.
9. Record unresolved trade-offs instead of inventing certainty.
10. Keep this document as the canonical portal blueprint; create specialized supporting docs only when a section becomes too large.

---

# 19. Immediate next work for Front 2

The first refinement should focus only on **Stage 1 — Information architecture and surface responsibilities**.

For each proposed surface:

- validate whether it deserves to exist independently;
- define its primary learner goal;
- define what information/actions belong there;
- identify overlap with other surfaces;
- define entry/exit paths;
- identify major empty/loading/error/returning states;
- identify decisions that depend on Front 1 or Front 3.

Do **not** yet design React components, API routes, database tables, evaluator schemas, or runner protocols.
