# Learning Portal

This folder defines the product, pedagogy, content model, and implementation boundaries for a future interactive learning experience inside the `ml-starter-lab-kit` ecosystem.

The Learning Portal is intentionally documented as a separate surface. The current generator, generated project structure, labs, and existing workspace should not be refactored merely to fit this concept.

## Product idea

The project should support two complementary experiences:

1. **Starter / experiment mode** — generate a clean ML project and work normally.
2. **Learning mode** — learn concepts through an interactive portal that combines theory, notes, visualizations, hand-worked exercises, guided practice, library-based implementation, review, and mastery tracking.

The Learning Portal should reuse project data and services where useful, but it should not depend on the existing UI structure.

## Adopted learning methodology

The Learning Portal follows an explicit learning-science foundation rather than treating its educational model as an open product hypothesis.

The adopted foundation is:

- **Mastery Learning** for progression based on demonstrated competence;
- **Cognitive Load management + Worked Examples + Scaffolding** for how new concepts are introduced and guidance is removed;
- **Retrieval Practice** for review and retained understanding;
- **Experiential Learning** for prediction, execution, observation, and explanation;
- **Competency / Skill Graph** for prerequisite-aware progression and multiple learning paths.

Gamification is a motivation and presentation layer over this foundation. XP, badges, achievements, and graph expansion must not replace evidence of mastery.

See [`09-learning-science-foundations.md`](09-learning-science-foundations.md) for the adopted rules and references.

## Core pedagogical principle

> Important abstractions should not appear for the first time hidden behind a library call.

Whenever a small manual execution exposes the mechanism behind a concept, the learner should perform that execution before using the library abstraction.

The standard learning loop is:

**intuition → theory → visualization → manual execution → guided experiment → library abstraction → application → review → mastery checkpoint**

Manual work is not an end in itself. If a calculation becomes repetitive arithmetic without adding understanding, the portal should prefer visualization, simulation, or an interactive tool.

## Current platform direction

The Learning Portal is a dedicated web application, not a Jupyter notebook or Streamlit application used as the product shell.

Current direction:

- React + TypeScript for the learner-facing portal;
- FastAPI + Python for APIs and learning-engine integration;
- a separate Python execution worker for code/data/ML activities;
- an Evaluator that checks results and pedagogical invariants;
- Evidence as the bridge between activity execution and mastery;
- SQLite initially for local learner state;
- notebook-like Python cells only where code is the appropriate activity surface.

The central technical flow is:

**Skill → Activity → Execution → Evaluation → Evidence → Mastery → Unlock**

See [`10-platform-architecture.md`](10-platform-architecture.md) for the current technical direction.

## Documentation surfaces

- [`01-product-vision.md`](01-product-vision.md) — macro objective, boundaries, and user experience.
- [`02-learning-model.md`](02-learning-model.md) — pedagogical loop and mastery model.
- [`03-skill-graph.md`](03-skill-graph.md) — graph-based progression, prerequisites, unlocks, and gamification.
- [`04-curriculum.md`](04-curriculum.md) — proposed teaching order and learning tracks.
- [`05-content-sources-and-licensing.md`](05-content-sources-and-licensing.md) — theory sources, citation rules, and copyright policy.
- [`06-activities-and-assessment.md`](06-activities-and-assessment.md) — exercises, deterministic checking, open solutions, review, and scoring.
- [`07-portal-experience.md`](07-portal-experience.md) — portal surfaces, notes, progress, review, and project integration.
- [`08-content-and-runtime-boundaries.md`](08-content-and-runtime-boundaries.md) — separation between content, learning engine, portal UI, execution runner, evaluator, and existing project runtime.
- [`09-learning-science-foundations.md`](09-learning-science-foundations.md) — adopted learning-science foundations, gamification boundary, and methodology rules.
- [`10-platform-architecture.md`](10-platform-architecture.md) — adopted web platform direction, Python execution, evaluator, evidence model, persistence, and first technical proof.
- [`11-portal-blueprint.md`](11-portal-blueprint.md) — working blueprint for Front 2: portal surfaces, shared shell, learner flows, interaction primitives, open design questions, and the staged plan for Jules/agent refinement before implementation.

## Status

These documents are product and pedagogical design material, not an implementation contract yet.

The learning methodology and current platform direction are adopted design decisions. Implementation details, thresholds, UI mechanics, security/sandboxing details, and individual curriculum nodes may still evolve within those principles.

Before opening implementation issues, convert this concept into bounded ownership slices. Do not mechanically turn each section or curriculum node into a GitHub issue.