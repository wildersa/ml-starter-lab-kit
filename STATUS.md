# Project Status

_Last updated: 2026-09-14_

## Current focus

The current design effort is the new **Learning Portal** for `ml-starter-lab-kit`.

The existing starter generator, generated project structure, labs/workspace, demo datasets, experiment tooling, and optional MLOps capabilities remain intact. The Learning Portal is a **separate educational surface** in the same ecosystem and should not require a broad refactor of the current UI/runtime.

The goal is to move beyond static documentation or notebook-only learning and create an interactive platform where a learner acquires ML skills only after producing evidence that the underlying competency was actually demonstrated.

The central flow is:

**Skill -> Activity -> Execution -> Evaluation -> Evidence -> Mastery -> Unlock**

Detailed design lives under [`docs/learning-portal/`](docs/learning-portal/README.md).

## Decisions already made

### Learning model

The adopted methodology is:

- **Mastery Learning** — progression depends on demonstrated competence, not lesson completion;
- **Cognitive Load management + Worked Examples + Scaffolding** — begin with bounded examples and progressively remove assistance;
- **Retrieval Practice** — review requires recalling/applying knowledge instead of simply rereading;
- **Experiential Learning** — prefer `predict -> execute -> observe -> explain` when a concept has observable behavior;
- **Competency / Skill Graph** — learning is represented as a DAG of real prerequisite relationships rather than one rigid linear course.

Gamification may expose XP, badges, acquired skills, branch achievements, and visible graph progression, but **XP never replaces mastery**.

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

Current direction:

- **React + TypeScript** — portal UI, Skill Graph, lessons, notes, visualizations, activity surfaces;
- **FastAPI + Python** — Learning API and application services;
- **Python Runner** — separate execution boundary for learner code, pandas, NumPy, scikit-learn, etc.;
- **Evaluator** — deterministic, structural, algorithm-aware, invariant-based, and rubric evaluation;
- **Evidence Store** — records the proof used to support mastery decisions;
- **SQLite initially** — learner state, attempts, notes, evidence, mastery, review, achievements;
- **Project Adapter** — narrow integration with generated projects/datasets without coupling learning content to generator internals.

The portal may provide notebook-like Python cells with inline execution, but `.ipynb` is not the product state model. Notebook export can be added later.

### Evaluation direction

The evaluator should validate the **meaning of the result**, not require the learner to reproduce reference code line by line.

Examples:

- numeric result with tolerance;
- matrix/DataFrame shape, columns, types, null rules, and expected values;
- confusion matrix correctness;
- Bellman or Q-learning update;
- clustering equivalence without depending on arbitrary cluster IDs;
- model performance against hidden evaluation data;
- target leakage prevention;
- train/validation/test discipline;
- time-aware split invariants;
- semantic/rubric checks only where deterministic evaluation is insufficient.

`Evidence` is a first-class product entity. The Learning Engine updates mastery and unlocks from accumulated evidence.

### Content and copyright

Educational content should be declarative and versionable where practical.

The project may adapt sources only when licensing explicitly permits it and attribution/share-alike requirements are respected. Protected books and papers may be cited and used as references for original explanations, but their text, figures, and exercises should not be copied merely because they are publicly accessible.

The current source/licensing policy is documented in [`docs/learning-portal/05-content-sources-and-licensing.md`](docs/learning-portal/05-content-sources-and-licensing.md).

## Current proposed first vertical slice

The first technical proof should be a small connected Reinforcement Learning path:

```text
RL vocabulary
 -> Return and discounting
 -> MDP
 -> Value functions
 -> Bellman equation
```

Use one small **GridWorld** across the path where useful.

This vertical slice is intended to prove:

- skill definitions and prerequisites;
- graph resolution and unlocks;
- theory rendering;
- learner notes;
- worked examples and scaffolding;
- manual formula/intermediate-step activities;
- deterministic evaluation;
- evidence capture;
- mastery calculation;
- review state;
- progress persistence;
- one interactive visualization/simulation.

A later second vertical slice should use classical/tabular ML to prove:

- Python code cells;
- pandas/NumPy/scikit-learn execution;
- DataFrame validation;
- model evaluation;
- hidden evaluation data;
- invariant-based checking such as leakage and split discipline.

## What is still missing

Before implementation issues should be opened, the design still needs the following concrete contracts:

1. **Minimal skill/content schema**
   - required skill metadata;
   - prerequisites;
   - theory blocks;
   - activity definitions;
   - references/provenance;
   - misconceptions;
   - mastery/evidence requirements;
   - transfer activities.

2. **Activity/evaluation contract**
   - supported first activity types;
   - learner input/output contract;
   - deterministic evaluator interface;
   - evidence produced by each activity;
   - failure/feedback representation.

3. **Mastery rule for the first slice**
   - what evidence is required to acquire a skill;
   - how attempts and hints affect evidence;
   - when a skill becomes `needs review`;
   - exact unlock semantics for the initial graph.

4. **Learner-state model**
   - skills/progress;
   - attempts;
   - evidence;
   - mastery;
   - notes;
   - misconceptions;
   - review state.

5. **Python Runner boundary**
   - process model for the local version;
   - allowed dependencies;
   - timeout/resource limits;
   - structured output format;
   - error handling;
   - how activity state is passed safely into evaluation.

6. **First RL content specification**
   - exact skill nodes;
   - prerequisite edges;
   - learning objectives;
   - theory references;
   - worked/manual exercises;
   - evaluator expectations;
   - GridWorld behavior;
   - mastery checkpoints.

7. **Implementation ownership/slicing**
   - only after the contracts above are stable enough;
   - issues must be grouped by code ownership and cohesive delivery, not one issue per skill or documentation section.

## Immediate next step

**Define the minimal Skill + Activity + Evaluation + Evidence contract using the first RL vertical slice as the concrete example.**

Do not start by building the React shell or a generic runner in isolation. First define one end-to-end learning unit precisely enough that the platform contract can be derived from a real case.

The immediate design target should answer, for `Return and discounting` and then `Bellman equation`:

- What exactly is the skill being claimed?
- What prerequisite does it require?
- What theory/content blocks are shown?
- What manual/worked activity does the learner perform?
- What inputs are submitted?
- What does the evaluator check?
- What evidence is stored?
- What mastery condition unlocks the next node?
- What should be revisited later through retrieval practice?

Once this contract is concrete for the first connected RL nodes, use it to finalize the content schema, learner-state model, evaluator interface, and then slice the implementation work into bounded issues.

## Not part of the current Learning Portal scope

The separate idea of using ML inside game/minigame scenarios is intentionally **not** part of this current portal design. It may become another project later.
