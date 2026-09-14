# Platform architecture

## Status

This document records the current platform direction for the Learning Portal.

The portal is a dedicated web application with notebook-like execution surfaces where useful. Jupyter notebooks and Streamlit are not the primary product shell.

The Portal and Lab Runtime are separate architectural responsibilities in **all** deployment modes, including local installations. Detailed access/runtime rules are canonicalized in [`13-access-and-runtime-boundaries.md`](13-access-and-runtime-boundaries.md).

## Product architecture

The platform is split into two major planes.

### Portal / control plane

Owns:

1. **Web Portal** — learner-facing experience.
2. **Learning API / Learning Engine** — skill graph, progression, mastery, review, unlocks, and orchestration.
3. **Evidence / Learner State** — competence evidence, notes, attempts, review state, ownership-aware learner state.
4. **Identity / Authorization** — who may access which learner/content/project/runtime capability.
5. **Content delivery** — published curriculum/activity definitions and references.

### Lab Runtime / execution plane

Owns:

1. **Python Runner** — executes learner code and ML/data activities.
2. **Execution-side evaluation helpers** — collect/check runtime-dependent results and invariants where necessary.
3. **Runtime-local Project Adapter** — controlled project/environment access when an activity is permitted to use it.
4. **Execution artifacts/resources** — files, charts, model outputs, resource limits, cancellation and cleanup.

The pedagogical **Evaluator** spans the boundary conceptually: the Portal owns the activity/evaluation intent and mastery decision; runtime-dependent evidence may be produced by the Lab Runtime through a controlled contract.

Conceptually:

```text
                    PORTAL / CONTROL PLANE

Browser
   |
   v
Web Portal
   |
   v
Learning API
   |
   +--> Identity / Authorization
   +--> Learning Engine
   +--> Content / Skill Graph
   +--> Learner State / Evidence / Mastery / Review
   |
   +------ scoped runtime/session request ------+
                                                 |
                                                 v
                    LAB RUNTIME / EXECUTION PLANE

                                      Runtime endpoint / agent
                                         |
                                         +--> Python Runner
                                         +--> NumPy / pandas / sklearn / ML deps
                                         +--> Runtime-local Project Adapter
                                         +--> project/data capabilities
                                         +--> execution artifacts/results
```

Local, SaaS, and hybrid deployments may place these processes on different infrastructure, but they must not collapse their responsibilities or trust boundary merely for convenience.

## Deployment topologies

### Local

The Portal and Runtime may execute on the same machine but should remain explicit processes/services/boundaries.

```text
local Portal -> local Runtime -> local project/environment
```

### SaaS

The hosted Portal remains the control plane. Arbitrary learner code executes only in isolated hosted runtime sessions.

```text
hosted Portal -> runtime broker/session -> isolated Lab Runtime
```

### Hybrid

A hosted Portal may use a scoped authenticated connection to a learner-controlled local Runtime/agent for local projects/private datasets.

```text
hosted Portal -> scoped connection -> local Lab Runtime -> local project/data
```

The product must not require project/data upload to the Portal merely to support this topology.

## Access profiles and separation of duties

The architecture must not assume one global user responsibility.

Initial responsibility classes are:

- **Learner** — consumes learning content, owns progress/notes/evidence, starts permitted Lab Runtime sessions and uses permitted own projects/data.
- **Content Author / Maintainer** — creates/versions educational content; does not automatically gain access to learner project/runtime data.
- **Platform Administrator / Operator** — manages platform/runtime policy and operations; does not automatically gain pedagogical impersonation or unrestricted learner project access.
- **Reviewer / Instructor / Mentor** — optional later role with explicit assignment/review permissions rather than inherited admin access.

Detailed RBAC/ABAC schemas are deferred, but authorization must be enforced server-side. UI visibility alone is never the security boundary.

The current Portal IA should be understood primarily as the **Learner** experience unless a later product decision explicitly adds author/admin surfaces.

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

Portal surfaces must distinguish activities that are Portal-only from those that require a Lab Runtime capability and expose useful unavailable/denied/disconnected states where relevant.

## Backend

Adopted direction:

- FastAPI;
- Python;
- application APIs around skills, activities, attempts, notes, evidence, mastery, review, identity/authorization, and project/runtime orchestration.

The API layer must not execute arbitrary learner code directly inside the Portal application process.

The Portal should request runtime **capabilities/sessions** instead of importing Runner internals or assuming one concrete runtime implementation.

## Python Runner / Lab Runtime

Learner code must run through an execution boundary separate from the Portal/API application process.

Responsibilities include:

- execute Python submitted from a permitted activity;
- expose libraries allowed by that activity/runtime policy;
- collect structured outputs, errors, artifacts, metrics, and intermediate evidence;
- enforce execution time/resource limits;
- support timeout/cancellation/cleanup;
- operate under a scoped learner/session/project capability;
- expose project/dataset access only when explicitly authorized.

Local execution may use the learner's generated project/Python environment where appropriate, but the Portal should reach that environment through the Runtime boundary rather than importing/executing it directly.

Hosted execution requires stronger per-session/per-exercise sandbox/container isolation. Hybrid execution may use a local Runtime/agent connected to a hosted Portal.

Possible structured outputs include:

- stdout/stderr;
- scalar values;
- arrays/matrices;
- DataFrame metadata/content samples;
- charts/artifact references;
- trained-model handles or evaluation outputs;
- activity-specific evidence.

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

Hidden evaluation material and results must follow the same learner/session/runtime authorization boundary as the activity that consumes them.

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

- which learner owns this evidence?
- which skill did this support?
- which activity produced it?
- what was checked?
- what result was observed?
- were hints used?
- was a misconception detected?
- which runtime/session/project context produced runtime-dependent evidence?
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
- achievements/XP if enabled;
- runtime/project associations where required.

Learner-specific records must be conceptually ownership-aware even if the first local release uses one implicit local learner identity.

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

The content model must not require a specific frontend component for every future activity type and must not depend on one concrete Runtime implementation.

## Project integration

The Learning Portal remains a separate surface from the existing generator/workspace.

The Portal may know safe product-level metadata such as whether a project is connected, its display identity, and declared capabilities.

Direct filesystem/environment inspection belongs behind a Lab Runtime/runtime-local Project Adapter boundary.

A Project Adapter may expose, according to granted capability:

- dataset and paths/metadata;
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

Any vertical slice that performs code execution must prove the Portal/Runtime boundary rather than introducing direct execution into the Portal process as a temporary shortcut.

## Architectural rules

The platform exists to prove learning, not merely code execution.

The central learning flow is:

**Skill -> Activity -> Execution -> Evaluation -> Evidence -> Mastery -> Unlock**

A learner receives a skill because sufficient evidence demonstrates the competency, not because the lesson page was completed.

Cross-cutting platform constraints:

1. Portal/control-plane and Lab Runtime/execution-plane responsibilities remain separate locally, in SaaS, and in hybrid mode.
2. Arbitrary learner code never executes inside the Portal/API process.
3. Direct learner project/environment access stays behind the scoped Runtime/Project Adapter boundary.
4. Authorization is server-enforced and ownership-aware.
5. Learner, content-authoring, and platform-administration responsibilities are separate.
6. Detailed runtime/auth contracts are intentionally deferred to Portal Stage `P2-S5`.