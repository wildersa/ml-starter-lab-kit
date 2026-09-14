# Content and runtime boundaries

## Objective

Keep the new learning experience separable from the current starter generator and workspace so the project can evolve without a broad refactor.

## Conceptual layers

### Existing starter core

Continues to own:

- wizard and project creation;
- generated project structure;
- configuration;
- demo datasets/scenarios;
- current labs/workspace;
- experiment/runtime capabilities;
- optional MLOps integrations.

The Learning Portal should not require these surfaces to be rewritten merely to reuse them.

### Learning content

Owns declarative educational material:

- skill definitions;
- prerequisite relationships;
- theory units;
- references/provenance;
- activities;
- rubrics;
- expected deterministic results;
- misconception tags;
- transfer exercise definitions.

Content should be as independent from the UI framework as practical.

### Learning engine

Owns progression semantics:

- graph dependency resolution;
- skill state;
- attempts;
- deterministic assessment orchestration;
- mastery calculation;
- unlock rules;
- review scheduling/status;
- learner notes metadata;
- achievements/XP if enabled;
- evidence produced by activities and checkpoints.

The engine must remain separate from UI-specific behavior.

### Learning Portal UI

Owns the interactive learner experience:

- home/dashboard;
- skill graph;
- lesson/skill rendering;
- notes;
- activity rendering;
- interactive visualizations;
- notebook-like code cells where useful;
- feedback;
- review center;
- project-transfer UX.

The adopted direction is a dedicated web application rather than Streamlit or Jupyter as the primary product shell.

Current platform direction:

- React + TypeScript for the learner-facing portal;
- FastAPI + Python for application APIs and learning-engine integration;
- Python execution workers for code/data/ML activities;
- SQLite initially for local learner state, with persistence kept behind a replaceable boundary.

Notebook-style interaction is a UI capability, not the platform architecture. The portal may later export or interoperate with notebooks, but `.ipynb` is not the primary learning state model.

### Python execution runner

Owns controlled execution of learner code and ML tasks.

Responsibilities include:

- execute Python submitted from an activity;
- expose the libraries allowed by that exercise;
- collect structured outputs, errors, artifacts, metrics, and intermediate evidence;
- enforce execution boundaries appropriate to the local environment;
- remain replaceable by stronger sandboxing/container isolation if the portal later becomes a hosted service.

The initial target is local execution associated with the generated project/environment. Hosted execution should use a stronger sandbox boundary rather than trusting arbitrary learner code in the application process.

### Evaluator

Owns deciding whether an activity result satisfies its pedagogical contract.

Evaluation may be:

- deterministic numeric comparison with tolerance;
- expected matrix/table/DataFrame properties;
- structural invariants;
- hidden test-set performance;
- process evidence when the skill requires correct procedure rather than only a final score;
- rubric/semantic evaluation only where deterministic validation is not appropriate.

The evaluator should validate outcomes and required invariants rather than exact source-code text whenever multiple valid solutions exist.

### Evidence model

Evidence is the bridge between activity execution and mastery.

Examples:

- a correct manual calculation;
- a valid confusion matrix;
- an expected DataFrame transformation;
- a model exceeding a baseline on a hidden evaluation set;
- proof that target leakage was avoided;
- a successful transfer exercise on another dataset;
- a review result demonstrating retained understanding.

Skills are unlocked from evidence/mastery rules, not because a page was viewed or because XP was earned.

### Project adapter

A narrow integration layer may expose current generated-project context to the Learning Portal.

Potential read surfaces:

- project config;
- dataset path/metadata;
- target;
- features;
- demo scenario;
- experiment outputs;
- metrics/artifacts;
- Python environment/runtime information needed by learning activities.

Avoid having learning content directly know internal generator/runtime paths.

## Learner state

Learner-specific state should be separate from curriculum source content.

Potential state includes:

- progress;
- mastery;
- attempts;
- evidence;
- misconception history;
- notes;
- review state;
- earned skills/achievements;
- current learning position.

The exact persistence format is intentionally replaceable. SQLite is the initial platform direction for local use.

If learner state is stored inside a generated project, prefer a dedicated namespace such as `.learning/` rather than mixing it into source code or experiment artifacts.

## Content packaging

Potential logical packages:

```text
foundations
classical-ml
unsupervised-ml
reinforcement-learning
deep-learning
time-series
computer-vision
mlops
```

These are content domains, not necessarily Python package boundaries.

## Stable content contract

Before producing large amounts of curriculum content, define a small stable skill schema that can express:

- metadata;
- prerequisites;
- theory blocks;
- activities;
- deterministic checks;
- rubric checks;
- references;
- misconceptions;
- mastery rules;
- evidence requirements;
- transfer activities.

Start with the smallest schema required by one vertical slice rather than designing every future activity type up front.

## First vertical slice recommendation

Use a connected RL subgraph because it exercises several unique portal capabilities:

```text
RL vocabulary
 -> Return and discounting
 -> MDP
 -> Value functions
 -> Bellman equation
```

Include one GridWorld reused across these skills.

This can validate:

- skill prerequisites;
- unlock behavior;
- theory rendering;
- notes;
- manual formula entry;
- intermediate-step checking;
- visual simulation;
- mastery;
- review;
- progress persistence.

After the engine is proven, add a classical ML vertical slice over a small public or synthetic tabular dataset to validate DataFrame/code/result-based activities through the Python runner and evaluator.

## Implementation-boundary rule

Do not refactor an existing portal/workspace simply because the Learning Portal could theoretically reuse its UI components.

Prefer:

- reuse of domain services;
- reuse of data contracts;
- reuse of project metadata;
- isolated adapters;

before:

- shared UI state;
- shared page shells;
- broad component migrations;
- generator/runtime restructuring.

## Future issue slicing

When implementation begins, do not open one issue per Markdown section or one issue per skill.

First identify actual code ownership surfaces such as:

- content schema/parser;
- learning engine/state;
- graph resolver;
- portal shell/navigation;
- graph visualization;
- activity renderer(s);
- Python execution runner;
- evaluator/evidence layer;
- learner-state persistence;
- project adapter;
- first RL content pack.

Group work by coherent delivery and ownership. If two tasks require the same shell, service, state store, schema, or test file, prefer one cohesive issue or sequence them instead of claiming fake parallelism.