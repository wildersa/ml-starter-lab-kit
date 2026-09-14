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

## Surface responsibilities & validation (Stage 1)

**ADOPTED**

Each surface must have an independent, non-overlapping learner purpose:

| Surface | Primary Learner Goal | Key Content / Actions | Distinct Ownership (Non-Overlap) |
|---|---|---|---|
| **Home** | Orient & launch next action | Recommendation tiles, active skill entry, review alerts, project transfer prompt | Does not contain full graph visualization or complete lesson content; acts as a launching pad. |
| **Skill Graph** | Map knowledge & prerequisites | Visual DAG of skills, node statuses, dependency edges, unlock requirements | Map/navigation surface only; selecting a node opens detail or launches Workspace, but content is not taught here. |
| **Skill Workspace** | Learn & acquire specific skill | Intuition, theory, visualizations, manual calculations, guided code, mastery checkpoint | The main learning surface; contains interactive pedagogical blocks for a single skill. |
| **Practice Lab** | Open unguided experimentation | Dataset sandbox, parameter tuning, multi-step challenge scenarios, model comparisons | Scaffolding-free environment for applying acquired skills without step-by-step lesson sequences. |
| **Review Center** | Reinforce retained knowledge | Retrieval practice queue, changed numeric problems, misconception resolution | Uses new/varied items for spaced retrieval; does not repeat original Workspace linear teaching text. |
| **Notes** | Synthesize learner understanding | Per-concept reflections, formulas, self-explanations, search/tagging | Learner-authored content only; distinct from platform curriculum source text. |
| **Progress / Profile** | Track mastery & evidence | Acquired skills, mastery evidence log, branch milestones, review health | Evidence dashboard; shows competence history without collapsing metrics into a single gamified score. |
| **Project Context** | Transfer skills to real code | Local project dataset binding, experiment artifacts, leakage checks, MLOps transfer | Bridge to `ml-starter-lab-kit` generated codebase; inspects external runtime artifacts. |

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
- whether `Project Context` is a first-class navigation item or contextual mode/panel;
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

The Home surface should orient the learner immediately upon entering the portal.

Primary learner goal: Answer "What should I do right now to make the best progress?" within 5 seconds.

## Candidate blocks

**PROPOSED**

- **Continue Active Skill:** Quick-resume card for the skill currently in progress;
- **Recommended Next Skill:** Highest-priority available node in the current track;
- **Review Queue Alert:** Notification of skills entering retrieval decay or detected misconceptions;
- **Current Branch Progress:** Visual summary of completion in active track (e.g., Supervised ML, RL);
- **Recent Notes:** Last updated personal reflections;
- **Project Transfer Opportunity:** Prompt to apply newly acquired skill to connected `ml-starter-lab-kit` project.

## Overlap prevention

Home is strictly an orientation/launching pad. It must **not**:
- Render full interactive lesson blocks (delegated to Skill Workspace);
- Render the entire DAG graph (delegated to Skill Graph);
- Store or edit full notes (delegated to Notes).

## Entry and exit paths

- **Entry:** Default landing page after login/launch; return via Primary Navigation "Home" icon.
- **Exit:** Launching a skill (`-> Skill Workspace`), clicking the graph overview (`-> Skill Graph`), starting a review (`-> Review Center`), or transferring to a project (`-> Project Context`).

## UX States (Stage 1)

**PROPOSED**

- **First Visit / Cold Start:** No skills started. Prominently features track selection and starting node recommendation; no review alerts or notes.
- **Active Learner / Normal:** Shows active skill card, next recommendation, and pending review counts.
- **All Track Skills Completed:** Recommends branching to another track or diving into open Practice Lab challenges.
- **Review Backlog Warning:** Highlighted prompt when multiple prerequisite skills are decaying or flagged with misconceptions.
- **Project Connected vs. Disconnected:** Displays active project badge and transfer prompt when a generated project is attached; shows "Connect Project" invitation otherwise.
- **Error / Offline State:** Gracefully displays cached progress and offline-available skills if execution server is disconnected.

## Dependencies

- **Front 1 (Content):** Depends on Front 1 defining prerequisite priority for recommendations.
- **Front 3 (Product):** Depends on Front 3 deciding onboarding choices and initial track selection.

---

# 5. Skill Graph

## Purpose

The Skill Graph is the learner's visual map of Machine Learning knowledge.

Primary learner goal: Provide clear mental model of overall ML domain structure, prerequisite dependencies, and unlocked paths.

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

## Information & Core interactions

**PROPOSED**

Selecting a node exposes a details drawer/modal with:

- skill purpose and learning goals;
- current state (locked/available/mastered/needs review);
- prerequisite nodes and completion status;
- explanation of lock reasons (missing prerequisites);
- concept nodes unlocked upon completion;
- direct action button: "Start Skill", "Continue", or "Review".

## Overlap prevention

The Skill Graph is a visual map and navigation surface. It must **not**:
- Render active interactive exercises or code runners (must launch Skill Workspace);
- Replace the detailed mastery evidence log (delegated to Progress / Profile).

## Entry and exit paths

- **Entry:** Primary Navigation "Skill Graph" or clicking "View Graph" on Home/Progress.
- **Exit:** Selecting an available node launches `Skill Workspace`; selecting a node needing review launches `Review Center`.

## UX States (Stage 1)

**PROPOSED**

- **Initial / Unexplored Graph:** Root nodes highlighted as "Available", all downstream nodes shown as "Locked" with visible prerequisite edges.
- **In-Progress Graph:** Nodes colored by status (started, acquired, mastered, needs review).
- **Filtered / Subgraph View:** Option to focus on a single track (e.g., Supervised, Bandit, Time Series).
- **Graph Loading / Error State:** Displays skeleton node layout if backend graph definition loading fails.

## Dependencies

- **Front 1 (Content):** Direct dependency on Front 1 to provide the canonical Skill Graph DAG structure, prerequisite edges, and node metadata.
- **Front 3 (Product):** Depends on Front 3 decision on whether distant locked nodes are visible or hidden (fog of war).

---

# 6. Skill Workspace

## Purpose

The Skill Workspace is the **main learning surface**.

Primary learner goal: Master a specific ML concept through structured, interactive, multi-modal pedagogical blocks.

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

## Overlap prevention

Skill Workspace focuses exclusively on linear/guided acquisition of a single skill. It must **not**:
- Host multi-step open dataset challenges without scaffolding (delegated to Practice Lab);
- Host general notes management (notes written here sync to the Notes surface).

## Entry and exit paths

- **Entry:** Launch from Home ("Continue Active Skill"), Skill Graph node detail, or Review Center recommendation.
- **Exit:** Completing mastery checkpoint unlocks next nodes and returns to Skill Graph or Home; learner can exit anytime with progress auto-saved.

## UX States (Stage 1)

**PROPOSED**

- **In-Progress Stage:** Learner working through blocks; previous completed blocks re-runnable.
- **Evaluation / Checking State:** Runner executing code/calculation; showing loading indicator and deterministic feedback.
- **Mastery Checkpoint Passed:** Celebratory unlock state showing demonstrated evidence and newly unlocked prerequisite branches.
- **Execution Error / Timeout:** Learner code error cleanly separated from platform execution error.

## Dependencies

- **Front 1 (Content):** Defines pedagogical sequence, formulas, worked examples, and checkpoint rubrics.
- **Front 3 (Product):** Defines gating policy (whether skipping explanatory blocks is permitted).

---

# 7. Practice Lab

## Purpose

The Practice Lab provides an unguided, open sandbox environment.

Primary learner goal: Combine and apply multiple acquired skills independently without step-by-step tutorial scaffolding.

## Candidate capabilities & uses

**PROPOSED**

- open dataset exploration and feature engineering sandbox;
- multi-step ML problem solving;
- comparing alternative model algorithms or parameters on identical datasets;
- stress-testing models under noise or dataset drift;
- challenge packs (e.g., "Fix leakage in this baseline pipeline").

## Overlap prevention

Practice Lab is unguided and exploratory. It must **not**:
- Teach initial concepts step-by-step (delegated to Skill Workspace);
- Force structured step-by-step checkpoints required for initial skill acquisition.

## Entry and exit paths

- **Entry:** Primary Navigation "Practice Lab" or "Try in Practice Lab" button at the end of a Skill Workspace.
- **Exit:** Return to Home, Skill Graph, or transfer configuration to Project Context.

## UX States (Stage 1)

**PROPOSED**

- **No Skills Acquired:** Empty state explaining that Practice Lab challenges unlock as relevant skills are acquired.
- **Active Challenge / Sandbox:** Workspace with dataset selector, code/parameter workspace, and evaluation metrics panel.
- **Submission Feedback:** Displays performance comparison against target benchmarks or baseline rules.

## Dependencies

- **Front 1 (Content):** Supply challenge datasets and benchmark criteria.
- **Front 3 (Product):** Decide whether Practice Lab activities generate formal mastery evidence or remain un-scored sandbox practice.

---

# 8. Review Center

## Purpose

The Review Center is an active retrieval practice surface.

Primary learner goal: Reinforce retained knowledge and clear identified misconceptions through targeted retrieval exercises.

## Candidate queues

**PROPOSED**

- **Decay Queue:** Skills due for retrieval based on time elapsed since mastery;
- **Misconception Queue:** Specific concepts flagged due to past checkpoint errors;
- **Prerequisite Review:** Weak prerequisite skills blocking access to a desired downstream node;
- **Manual Review:** Skills manually marked by the learner for re-study.

## Review interaction types

- recall questions with varied phrasing;
- changed numerical calculation problems (different parameters from original lesson);
- diagnosis tasks (identify the flaw in a given pipeline or chart);
- compare/contrast concept choices.

## Overlap prevention

Review Center focuses on active testing and retrieval. It must **not**:
- Re-render the full linear tutorial text of the original Skill Workspace;
- Act as an open coding sandbox (delegated to Practice Lab).

## Entry and exit paths

- **Entry:** Primary Navigation "Review", Home "Skills Needing Review" alert, or Skill Graph node review option.
- **Exit:** Completing a review session updates mastery health and returns to Home or Skill Graph.

## UX States (Stage 1)

**PROPOSED**

- **Queue Empty / All Clear:** Displays confirmation that retention health is optimal with no pending reviews.
- **Active Review Session:** Flashcard / calculation / diagnosis interaction sequence.
- **Session Complete:** Summary showing items answered correctly, misconceptions cleared, and updated retention strength.

## Dependencies

- **Front 1 (Content):** Provision of varied question variants, changed numeric examples, and misconception diagnostic items.
- **Front 3 (Product):** Definition of spaced retrieval algorithms and impact of failed review on mastery status.

---

# 9. Notes

## Purpose

Notes represent the learner's personal knowledge base and reflections.

Primary learner goal: Record, organize, and reference personal explanations, insights, and formulas across all skills.

## Note model & Capabilities

**PROPOSED**

- Structured per-skill prompts ("My explanation", "Key takeaway", "Common mistakes to avoid");
- Free-form Markdown notes;
- Inline note creation inside Context Panel during Skill Workspace sessions;
- Global search and tagging across all personal notes.

## Overlap prevention

Notes store learner-generated commentary only. It must **not**:
- Modify or overwrite canonical platform content;
- Serve as a progress log (delegated to Progress / Profile).

## Entry and exit paths

- **Entry:** Primary Navigation "Notes" or Context Panel tab inside Skill Workspace.
- **Exit:** Clicking a note's source skill link opens `Skill Workspace` or `Skill Graph`.

## UX States (Stage 1)

**PROPOSED**

- **Empty Notes State:** Displays prompts inviting learner to take notes during their next skill session.
- **Notes List / Search View:** Searchable index grouped by track and skill node.
- **Context Panel View:** Compact slide-out panel accessible while working on a skill.

## Dependencies

- **Front 3 (Product):** Policy on whether AI-assisted note summarization or self-generated quiz questions will be supported.

---

# 10. Progress / Profile

## Purpose

Provide transparent visualization of competence development and evidence history.

Primary learner goal: Inspect demonstrated skills, mastery evidence, milestone achievements, and learning history.

## Distinct concepts

**ADOPTED**

Do not collapse these into one score:

- progress (completion percentage);
- acquired skills (skills with passing checkpoints);
- mastery (sustained competence verified over time/retrieval);
- review status (retention decay metrics);
- achievements/XP when enabled.

## Information & Candidate views

**PROPOSED**

- **Competency Matrix:** Detailed list of acquired and mastered skills categorized by domain;
- **Evidence Log:** Audit trail of passed checkpoints, code runs, and calculation scores;
- **Track Milestones:** Completion status across ML tracks;
- **Misconception Resolution History:** Record of identified and resolved misconceptions.

## Overlap prevention

Progress / Profile is an analytical dashboard. It must **not**:
- Launch interactive exercises directly without going through Skill Workspace or Review Center.

## Entry and exit paths

- **Entry:** Primary Navigation "Progress" or clicking profile icon in shell.
- **Exit:** Clicking any listed skill opens `Skill Graph` or `Skill Workspace`.

## UX States (Stage 1)

**PROPOSED**

- **New Learner:** Shows clean slate with 0 acquired skills and onboarding milestone trackers.
- **Established Learner:** Full breakdown of mastery level, evidence history timeline, and branch badges.

## Dependencies

- **Front 1 (Content):** Mapping of skills to macro domains and mastery evidence criteria.
- **Front 3 (Product):** Decisions on gamification visibility (XP, badges) vs pure mastery evidence display.

---

# 11. Project Context / transfer

## Purpose

Connect portal learning directly to a generated `ml-starter-lab-kit` local project dataset and code structure.

Primary learner goal: Apply theoretical ML concepts to real project code and datasets generated in the local workspace.

## Candidate capabilities

**PROPOSED**

- Automatically detect attached `ml-starter-lab-kit` project configuration (`config.json`, dataset path, target feature);
- Run diagnostic checks (leakage inspection, class imbalance, missing value analysis) on project data;
- Generate transfer tasks (e.g., "Build baseline for your bank_campaign project");
- Compare project metrics against portal benchmark implementations.

## Overlap prevention

Project Context is a bridge to local generated projects. It must **not**:
- Replace standard tutorial datasets used in foundational Skill Workspaces (teaching data must remain controlled and clean);
- Overwrite user project source files directly without confirmation.

## Entry and exit paths

- **Entry:** Home "Project Transfer" card, Context Panel "Project" tab, or starting portal via `python -m <pkg>.lab portal`.
- **Exit:** Return to Home or Skill Workspace.

## UX States (Stage 1)

**PROPOSED**

- **No Project Connected:** Displays instructions on how to attach a generated `ml-starter-lab-kit` project.
- **Project Attached & Validated:** Displays project metadata (Dataset: Bank Campaign, Task: Binary Classification, Target: `y`).
- **Transfer Task Ready:** Highlights relevant skills that can now be executed against the connected project dataset.

## Dependencies

- **Front 4 (Ecosystem / Integration):** Complete dependency on Front 4 for project metadata format, local file IPC/API contracts, and safe read/write boundaries.

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
