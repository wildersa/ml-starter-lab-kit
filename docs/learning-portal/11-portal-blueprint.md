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

The primary navigation model uses a **collapsible left sidebar (desktop)** combined with a **top header/status bar**.

The primary navigation enables the learner to immediately answer:
- Where am I now? (Active route in header/sidebar)
- What can I learn next? (Home recommendation / Skill Graph)
- What needs review? (Review Center queue count in top header and sidebar badge)
- Where can I practice freely? (Practice Lab)
- Where are my notes? (Notes surface or contextual side panel)
- What have I actually mastered? (Progress / Profile)

### Primary surface access

- **Always-visible primary destinations**: Home, Skill Graph, Practice Lab, Review Center, Notes, Progress / Profile.
- **Contextual mode vs first-class surface**: `Project Context` is accessible via a persistent indicator in the top header when a project is attached, as well as an integrated mode inside Skill Workspace and Practice Lab.
- **Availability rules**: `Practice Lab` is always visible in primary navigation, but specific practice packs or datasets unlock as dependent skills are acquired.

## Desktop and responsive constraints

- **Desktop (>= 1024px)**: Left collapsible sidebar for primary navigation; persistent top header for status and active skill context; main central workspace; right contextual panel (collapsible/toggleable).
- **Tablet (768px - 1023px)**: Left sidebar collapses to icon-only rail or drawer; right contextual panel converts to slide-over drawer or tabbed bottom panel.
- **Mobile (< 768px)**: Bottom navigation bar for core destinations (Home, Graph, Practice, Review, Profile); top app bar with hamburger menu for Notes and Project Context; workspace renders full width.

## Alternatives and trade-offs

- **Top navigation bar only**:
  - *Pros*: Maximizes horizontal workspace width for code/data tables.
  - *Cons*: Limited space for badges (e.g., review queue counters), deep section indicators, or project status.
- **Collapsible left sidebar (Recommended)**:
  - *Pros*: Scales well as learning paths grow; provides clear vertical hierarchy and badge space; can collapse to icon rail during execution/coding tasks.
  - *Cons*: Consumes horizontal width on narrower desktop viewports.
- **Hybrid (Left rail + Contextual right panel) (Adopted Direction)**:
  - *Pros*: Keeps primary navigation stable on the left while keeping task-relevant tools (notes, hints, prerequisites) adjacent to the central workspace on the right.

---

# 3. Shared application shell

## Purpose

Provide stable navigation, persistent learner state, and context while the central workspace transitions between theory, exercises, simulations, code, review, and project transfer.

## Stable shell regions

```text
+-----------------------------------------------------------------------------------+
| Top Header / Status Bar (Global context, active path, review queue, project link) |
+------------------+------------------------------------------+---------------------+
| Primary Nav Rail | Main Workspace                           | Context Panel       |
| (Home, Graph,    | (Explanatory content, code cells,        | (Notes, hints,      |
|  Practice,       |  simulations, checkpoints, charts)       |  prerequisites,     |
|  Review, Notes,  |                                          |  project context)   |
|  Progress)       |                                          |                     |
+------------------+------------------------------------------+---------------------+
```

### 1. Top Header / Status Bar

Provides global situational awareness across all surfaces:
- active skill or learning path breadcrumb;
- review queue badge (e.g., "3 skills due for review");
- connected project context indicator (e.g., "Attached: `bank-campaign`");
- global learner progress summary (e.g., current streak, acquired skills count).

### 2. Primary Navigation Rail (Left)

Stable navigation bar allowing one-click access to all top-level surfaces. Supports collapsed (icon-only) and expanded states.

### 3. Main Workspace Area (Center)

Occupies the majority of the viewport. Holds the active surface content (Skill Workspace, Graph view, Practice Lab canvas, Review session, or Notes manager).

### 4. Contextual Side Panel (Right)

Collapsible side panel that stays synchronized with the active task in the Main Workspace.
- Shares tabs or collapsible sections for: Learner Notes, Hints & Explanations, Skill Prerequisites / Related Concepts, and Project Context details.
- Allows taking notes or consulting references without navigating away from an exercise or code cell.

## Persisted global context

While the learner moves between surfaces, the shell maintains:
- active learning path and current skill selection;
- connected project metadata and adapter connection state;
- review queue counters;
- uncommitted note drafts or workspace inputs;
- execution worker connection status.

## Distraction-free / Full-width mode

For immersive activities (such as writing multi-line Python code, inspecting large DataFrames, or manipulating complex interactive simulations):
- The learner or system can trigger **Distraction-free Mode**.
- Collapses the left primary navigation rail to hidden/hover-only and closes the right contextual side panel.
- Expands the Main Workspace to 100% viewport width.
- Preserves a minimal top bar with exit/toggle affordance and run controls.

## Global vs surface-local indicators

| Indicator / Control | Shell Scope | Owning Surface |
| --- | --- | --- |
| Route Navigation | Global (Shell) | Shared Shell |
| Review Queue Count | Global (Shell Top Bar) | Review Center |
| Connected Project Status | Global (Shell Top Bar) | Project Context |
| Active Skill Progress / Stage | Surface-Local | Skill Workspace |
| Graph Filters / Views | Surface-Local | Skill Graph |
| Code Execution Controls | Surface-Local | Skill Workspace / Practice Lab |
| Local Note Editor | Contextual Panel | Notes / Skill Workspace |

## Dependencies on other fronts

- **Front 3 (Product/UX)**: Final preference on gamification counter visibility (XP/streak) in the top header vs Profile surface.
- **Front 4 (Ecosystem/Integration)**: Metadata contract for connected project indicator (project name, dataset status, read-only safeguards).

---

# 4. Home

## Learner purpose and core job

**ADOPTED DIRECTION**

Home's single primary learner job is to act as an **orientation and momentum launchpad**.

When a learner opens the portal, Home must instantly answer one central question:
> **"What is my single best next learning step right now to maintain momentum?"**

Home is **not** a general-purpose analytical dashboard, a full course catalog, or an execution environment. It eliminates decision paralysis by evaluating current progress, spaced-repetition review needs, and connected project opportunities to recommend one immediate, high-priority primary action while keeping alternative paths easily reachable.

---

## Recommendation model: Bounded hybrid

**ADOPTED DIRECTION**

Home adopts a **bounded hybrid model** (1 Hero Recommendation + up to 3 secondary choices):

1. **Primary Hero Action (Single CTA)**: One prominent primary action card at the top of the surface.
   - If a skill is in progress -> "Resume [Skill Name]".
   - If high-priority review is due -> "Start Retrieval Session ([N] items due)".
   - If previous skill was mastered -> "Start Next Skill: [Skill Name]".
2. **Bounded Secondary Choices (Max 3 Cards)**:
   - *Review Status*: Summary of items due for retrieval practice (launches Review Center).
   - *Active Branch / Graph Snapshot*: Current position in the active learning track (launches Skill Graph focused on current branch).
   - *Project Transfer Opportunity*: Available transfer activity if an `ml-starter-lab-kit` project is connected (launches Project Context or Practice Lab).

### Rationale and trade-offs

- **Alternative 1: Pure Single-Recommendation (e.g., Netflix "Play Next")**:
  - *Pros*: Minimizes cognitive load and decision latency.
  - *Cons*: Frustrates learners who want to switch focus (e.g., review before starting new material or practice on their project).
- **Alternative 2: Open Dashboard (Grid of all widgets and metrics)**:
  - *Pros*: Maximum information density in one place.
  - *Cons*: Causes decision paralysis, duplicates Skill Graph and Progress/Profile, and dilutes learning momentum.
- **Decision (Bounded Hybrid)**: Provides a clear, low-friction default path (Hero CTA) while respecting learner autonomy through 2-3 structured alternative entry points.

---

## Learner states and UX behavior

Home adapts its layout and content dynamically based on learner lifecycle and context:

### 1. First-visit state (No prior progress)
- **Learner Context**: New user entering the portal for the first time without learning history.
- **Primary Hero Action**: "Start Onboarding Track" or "Begin Foundation: [First Skill Name]".
- **Surface Content**: A welcoming orientation block introducing the Skill Graph model, a track selector (e.g., "Supervised Learning", "Time Series", "Bandits"), and a single primary action to start the first node.
- **Secondary Cards**: Hidden or collapsed into a quick orientation preview.

### 2. Returning-learner state (Active learning track)
- **Learner Context**: Active user with at least one in-progress or recently completed skill.
- **Primary Hero Action**: "Resume [Active Skill]" showing current stage (e.g., "Stage 3: Guided Execution").
- **Secondary Cards**:
  - Current Track progress summary card ("3 of 8 skills in Classical ML").
  - Spaced repetition summary badge ("1 item due for review").
  - Connected project transfer prompt (if attached).

### 3. Review-needed state (Retrieval backlog exists)
- **Learner Context**: Spaced repetition algorithm flags one or more acquired skills as `needs review`.
- **Primary Hero Action**: If review backlog exceeds urgency threshold (e.g., critical prerequisite weak or review overdue), the Hero CTA temporarily switches to "Start Critical Review: [Skill Name]". Otherwise, review remains a high-priority secondary card.
- **Behavior**: Prominently displays why review is suggested (e.g., "Prerequisite for upcoming node 'Random Forests' needs reinforcement").

### 4. Project-connected state (`ml-starter-lab-kit` attached)
- **Learner Context**: Portal opened from or connected to a local generated ML project (e.g., `bank-campaign-bandit`).
- **Surface Behavior**:
  - Header indicator confirms project linkage.
  - Displays a dedicated "Project Transfer Opportunity" card (e.g., "Apply Feature Analysis to your `bank-campaign` dataset").
  - Hero action offers one-click transfer when the active skill directly aligns with project state.

### 5. Project-independent state (Standalone learning)
- **Learner Context**: Portal running in standalone educational mode without a linked local project.
- **Surface Behavior**:
  - Standard curriculum path and synthetic teaching datasets are used for all exercises.
  - Secondary card displays a subtle invitation: "Connect a generated project to practice on your own data."

### 6. Branch completion / Endpoint state
- **Learner Context**: Learner has completed all available nodes in the active branch or current release.
- **Primary Hero Action**: "Explore Next Branch in Skill Graph" or "Attempt Practice Lab Challenge".
- **Surface Content**: Congratulatory summary, milestone evidence summary, and direct links to secondary branches or Practice Lab.

---

## Surface boundaries and separation of responsibilities

To prevent Home from degenerating into a bloated dashboard, strict boundaries are enforced against other portal surfaces:

| Surface | What Home OWNS (Summary / Launchpad) | What Home explicitly DOES NOT OWN (Deep Surface) |
| --- | --- | --- |
| **Skill Graph** | Single next recommended node; current branch name and step count summary. | Full DAG visualization, interactive node exploration, edge dependency inspection, path switching. |
| **Skill Workspace** | Launch button ("Resume / Start") and active stage snippet. | Interactive content rendering, Python code execution, formula inputs, simulations, checkpoints. |
| **Review Center** | Review queue count, urgency warning badge, direct launch trigger. | Spaced repetition queue management, retrieval question cards, review history, performance scoring. |
| **Practice Lab** | Single optional project/challenge transfer prompt. | Open dataset exploration, multi-step unguided exercises, sandbox coding canvas. |
| **Progress / Profile** | High-level momentum indicators (e.g., streak, total acquired skills count). | Detailed skill mastery breakdown, evidence logs, misconception history, XP/achievement lists. |
| **Notes** | Optional snippet of last edited note or bookmark link. | Note editor, search, tag filtering, full note repository management. |
| **Project Context** | Project connection badge (e.g., `bank-campaign`) and transfer readiness status. | Raw dataset browser, project config editor, pipeline artifact inspector, execution logs. |

---

## Summary-only information boundary

Home must only store and render **summary-level projections** of learner state:

- **Allowed on Home**:
  - Active skill title, progress percentage, and current stage label.
  - Review queue total item count and top urgent skill name.
  - Active learning track title and overall completion ratio (e.g., "4/10 acquired").
  - Connected project name and 1-line transfer status.
  - Current active streak count.
- **Prohibited on Home**:
  - Full activity cards, interactive exercises, or code editors.
  - Complete list of acquired/locked skills.
  - Full review item queue list or question previews.
  - Detailed evidence logs, test attempt histories, or raw metrics tables.

---

## Entry and exit paths

### Entry paths into Home
- **Default root route**: Direct landing upon opening the web application (`/`).
- **Global Header**: Clicking the application logo or "Home" icon in the top/left navigation rail.
- **Post-Session exit**: Returning to Home after completing a Skill Workspace checkpoint or Review session.

### Exit paths from Home
- **Hero CTA click** -> Navigates directly into **Skill Workspace** (or **Review Center** if review hero is active).
- **Review Card click** -> Navigates to **Review Center**.
- **Track / Graph Card click** -> Navigates to **Skill Graph** focused on the active branch.
- **Project Transfer Card click** -> Navigates to **Project Context** or transfer mode in **Practice Lab**.

---

## Dependencies on other fronts

1. **Front 1 (Content & Pedagogy)**:
   - Recommendation ranking rules (determining whether a review item overrides a new skill recommendation).
   - Track structure and default starting nodes for first-visit orientation.
2. **Front 3 (Product & UX)**:
   - Onboarding survey/preference decisions (whether new learners pick a track manually or take a diagnostic placement).
   - Final policy on streak/gamification visual priority on Home.
3. **Front 4 (Ecosystem & Integration)**:
   - Contract for detecting local project presence (`.ml-starter-project.json` or adapter handshake) to trigger project-connected states.

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
