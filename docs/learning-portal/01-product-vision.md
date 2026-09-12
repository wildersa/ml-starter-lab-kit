# Product vision

## Macro objective

Create an interactive learning surface for Machine Learning that helps the learner move from conceptual understanding to practical implementation without hiding important mechanisms too early behind libraries.

The portal should be useful both to someone learning from scratch and to someone who already has a generated ML project and wants guided practice over their own data.

## What the Learning Portal is

A separate application surface in the same ecosystem as `ml-starter-lab-kit`.

It should provide:

- structured learning tracks;
- theory in short, focused units;
- visual and interactive explanations;
- personal notes;
- manual exercises where useful;
- guided experiments;
- practical implementation with standard libraries;
- deterministic evaluation where possible;
- semantic/rubric evaluation where necessary;
- review and spaced revisit opportunities;
- mastery and skill unlocks;
- transfer exercises using the learner's own project/dataset.

## What it is not

The Learning Portal should not force a redesign of the current generator or existing workspace.

It should not become:

- a replacement for the starter generator;
- a mandatory UI for generated projects;
- a monolithic course where all learners follow one fixed line;
- a quiz-only product;
- a game where XP is more important than actual mastery;
- an LLM-dependent experience that cannot function deterministically without a model.

## Product surfaces

### Starter / Experiment mode

Existing project purpose remains intact:

- wizard;
- project generation;
- project structure;
- configs;
- demo datasets;
- labs/workspace;
- reproducible experimentation;
- optional MLOps tooling.

### Learning mode

New portal purpose:

- choose or continue a learning path;
- navigate the skill graph;
- study a concept;
- write notes;
- perform exercises;
- receive feedback;
- review weak concepts;
- unlock dependent skills;
- eventually apply the concept to the current project.

## Integration principle

Reuse data and capabilities, not UI by default.

The Learning Portal may consume:

- generated project metadata;
- project configuration;
- demo scenario metadata;
- dataset paths;
- target/features metadata;
- experiment outputs;
- metrics and artifacts;
- learner-specific progress data.

The portal should remain architecturally separable from the current workspace.

## Long-term product identity

The result should feel less like a fixed ML course and more like an **interactive knowledge map where each node is a demonstrable competency**.

A learner should be able to answer:

- What do I already know?
- What can I learn next?
- Why is this skill blocked?
- What prerequisite am I missing?
- What did I misunderstand?
- Where can I apply this in my own project?

## Product success signal

The system is successful when the learner can move from:

> "I know how to call this library"

into:

> "I understand what the library is doing, when the method is appropriate, how to inspect its result, and how it connects to the rest of ML."