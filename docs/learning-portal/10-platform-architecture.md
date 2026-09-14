# Platform architecture

## Status

This document records the current platform direction for the Learning Portal.

The portal is a dedicated web application with notebook-like execution surfaces where useful. Jupyter notebooks and Streamlit are not the primary product shell.

## Product architecture

The platform is divided into six major responsibilities:

1. **Web Portal** — learner-facing experience.
2. **Learning Engine** — skill graph, progression, mastery, review, and unlocks.
3. **Python Runner** — executes learner code and ML/data activities.
4. **Evaluator** — checks expected results and pedagogical invariants.
5. **Evidence Store** — records what demonstrates competence.
6. **Project Adapter** — connects learning activities to a generated ML project when appropriate.

Conceptually:

```text
Web Portal
   |
   v
FastAPI / Learning API
   |
   +--> Learning Engine
   |
   +--> Python Runner
   |       |
   |       v
   |    learner code / pandas / NumPy / scikit-learn / project environment
   |
   +--> Evaluator
   |       |
   |       v
   |    Evidence
   |
   +--> Learner State / Mastery / Unlocks
   |
   +--> Project Adapter
```

## Frontend

Adopted direction:

- React;
- TypeScript;
- web-first interaction;
- dedicated Skill Graph surface;
- lesson/activity rendering;
- personal notes;
- visual simulations;
- tables/grids/formula workspaces;
- code cells where code is the appropriate activity surface;
- immediate structured feedback.

The UI should select the interaction type that best exposes the concept. Not every exercise should be code and not every exercise should be a form.

## Backend

Adopted direction:

- FastAPI;
- Python;
- application APIs around skills, activities, attempts, notes, evidence, mastery, review, and project integration.

The API layer should not execute arbitrary learner code directly inside the web application process.

## Python Runner

Learner code must run through an execution boundary separate from the normal API request logic.

Initial local direction:

- execute against the local project/Python environment where appropriate;
- support NumPy, pandas, scikit-learn, matplotlib and other explicitly enabled learning dependencies;
- return structured results rather than only raw console text;
- capture errors without crashing learner state;
- enforce time/resource limits appropriate to a local educational tool.

Possible structured outputs include:

- stdout/stderr;
- scalar values;
- arrays/matrices;
- DataFrame metadata/content samples;
- charts/artifact references;
- trained-model handles or evaluation outputs;
- activity-specific evidence.

If the platform later becomes a hosted service, arbitrary code execution must move to stronger per-session/per-exercise sandbox or container isolation.

## Notebook-like cells, not notebook-as-product

The portal may present editable Python cells with `Run` behavior and inline output.

This provides the useful interaction model of notebooks while keeping control over:

- execution order;
- exercise state;
- expected inputs/outputs;
- evaluation;
- progression;
- feedback;
- mastery evidence.

The canonical learner state should not depend on `.ipynb` execution state.

Notebook export may be added later as an artifact or interoperability feature.

## Evaluator

Each activity should declare an evaluation contract.

The evaluator should prefer checking the meaning of the result instead of comparing source code.

### Numeric

Examples:

- expected value with tolerance;
- metric range;
- probability distribution properties.

### Structured data

Examples:

- expected shape;
- required columns;
- dtypes;
- null constraints;
- selected values;
- ordering only when pedagogically relevant.

### Algorithm-aware

Examples:

- clustering equivalence without assuming fixed cluster label IDs;
- model performance above a defined baseline on hidden data;
- valid confusion matrix;
- expected Bellman/Q-learning update;
- correct time-aware split.

### Process/invariant

Used when the learning objective requires correct procedure, not merely a good final score.

Examples:

- target not present in features;
- test set not used during training/tuning;
- preprocessing can transform unseen examples;
- original raw dataset remains unchanged;
- time-series split preserves temporal ordering.

### Semantic/rubric

Used only when an explanation or interpretation cannot be reduced to deterministic validation.

An LLM may assist semantic evaluation, but deterministic checks remain authoritative whenever the result is objectively checkable.

## Hidden evaluation data

Some practical ML checkpoints should evaluate against data the learner does not directly optimize against.

Example:

```text
training data available to learner
        |
        v
learner solution/model
        |
        v
hidden evaluation set
        |
        v
metric + invariant checks
```

This prevents a learner from passing a model-building skill by printing a known answer or overfitting to the visible example.

The hidden set is pedagogical assessment data, not necessarily a production-grade benchmark.

## Evidence

Evidence is a first-class product concept.

An activity result becomes evidence when it supports a specific competency claim.

Examples:

- learner calculated discounted return correctly;
- learner distinguished reward from return in a review;
- learner constructed a valid confusion matrix;
- learner trained a classifier that generalizes above the required baseline;
- learner avoided leakage;
- learner transferred the concept successfully to another dataset.

Evidence should retain enough provenance to answer:

- which skill did this support?
- which activity produced it?
- what was checked?
- what result was observed?
- were hints used?
- was a misconception detected?
- when did this occur?

The Learning Engine consumes evidence to update mastery and unlock dependencies.

## Learner state

Initial local persistence direction: SQLite.

Likely data domains include:

- skill progress;
- mastery;
- unlock status;
- activity attempts;
- evidence;
- notes;
- misconception tags;
- review state/history;
- achievements/XP if enabled.

Persistence should remain behind an application boundary so a future hosted version can use another database without changing curriculum semantics.

## Content model

Educational content should remain declarative and versionable in the repository where practical.

A skill definition needs to connect:

- theory;
- prerequisites;
- activities;
- interaction type;
- evaluation contract;
- mastery/evidence requirements;
- references/provenance;
- misconceptions;
- transfer activities.

The content model must not require a specific frontend component for every future activity type.

## Project integration

The Learning Portal remains a separate surface from the existing generator/workspace.

A Project Adapter may expose:

- dataset and paths;
- config;
- target/features;
- demo scenario;
- experiment outputs;
- metrics/artifacts;
- environment information.

Learning content should request project capabilities through this adapter instead of importing generator internals directly.

## First technical proof

The first implementation should prove the architecture with a small connected skill path rather than attempting a complete curriculum.

Recommended first vertical slice:

```text
RL vocabulary
 -> Return and discounting
 -> MDP
 -> Value functions
 -> Bellman equation
```

This slice can validate:

- skill graph and unlocks;
- theory rendering;
- notes;
- manual formula workspace;
- deterministic evaluator;
- evidence/mastery;
- review;
- one interactive GridWorld.

A second vertical slice should use classical ML/tabular data to validate Python cells, pandas/scikit-learn execution, hidden evaluation data, and invariant-based assessment.

## Architectural rule

The platform exists to prove learning, not merely code execution.

The central flow is:

**Skill -> Activity -> Execution -> Evaluation -> Evidence -> Mastery -> Unlock**

A learner receives a skill because sufficient evidence demonstrates the competency, not because the lesson page was completed.