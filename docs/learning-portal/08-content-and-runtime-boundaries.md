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
- deterministic assessment;
- mastery calculation;
- unlock rules;
- review scheduling/status;
- learner notes metadata;
- achievements/XP if enabled.

The engine should not depend on Streamlit-specific UI behavior.

### Learning Portal UI

Owns the interactive learner experience:

- home/dashboard;
- skill graph;
- lesson/skill rendering;
- notes;
- activity rendering;
- interactive visualizations;
- feedback;
- review center;
- project-transfer UX.

Streamlit is a reasonable initial UI technology because the project already uses Python and interactive ML workflows, but the content and engine should remain portable enough that a future UI does not require rewriting curriculum data.

### Project adapter

A narrow integration layer may expose current generated-project context to the Learning Portal.

Potential read surfaces:

- project config;
- dataset path/metadata;
- target;
- features;
- demo scenario;
- experiment outputs;
- metrics/artifacts.

Avoid having learning content directly know internal generator/runtime paths.

## Learner state

Learner-specific state should be separate from curriculum source content.

Potential state includes:

- progress;
- mastery;
- attempts;
- misconception history;
- notes;
- review state;
- earned skills/achievements;
- current learning position.

The exact persistence format is intentionally not fixed here.

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

After the engine is proven, add a classical ML vertical slice over a small public or synthetic tabular dataset to validate DataFrame/code/result-based activities.

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
- learner-state persistence;
- project adapter;
- first RL content pack.

Group work by coherent delivery and ownership. If two tasks require the same shell, service, state store, schema, or test file, prefer one cohesive issue or sequence them instead of claiming fake parallelism.