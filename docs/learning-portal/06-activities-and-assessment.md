# Activities and assessment

## Objective

Assessment should verify understanding and practical ability, not only content exposure.

The portal should support multiple activity types because ML skills are not demonstrated by multiple-choice questions alone.

## Activity types

### Recall

Retrieve a concept without looking at the explanation.

Examples:

- explain reward vs return in your own words;
- define feature and target;
- explain why a test set should not guide model tuning.

### Calculation

Execute a small mathematical operation that exposes a mechanism.

Examples:

- compute discounted return;
- calculate precision/recall from a confusion matrix;
- perform one Q-learning update;
- calculate Euclidean distance;
- perform one centroid update.

### Prediction

Predict what will happen before executing an experiment.

Examples:

- change `gamma` and predict the effect;
- change a threshold and predict metric trade-offs;
- change K and predict clustering behavior.

### Manipulation

Interact with a visual or parameterized model and observe consequences.

Examples:

- move cluster centroids;
- change a decision threshold;
- alter reward values in a grid world;
- add an outlier and observe summary statistics.

### Diagnosis

Inspect a result and identify what is wrong.

Examples:

- detect leakage;
- explain poor validation behavior;
- identify an inappropriate metric;
- inspect a policy/value table and find the inconsistency.

### Implementation

Reach a defined result using code or a notebook/runtime cell.

The evaluator should prefer checking the result and required invariants rather than requiring one exact implementation path.

### Experiment

Run a controlled experiment, record the result, and interpret it.

### Challenge

Solve a problem with reduced scaffolding.

### Transfer

Apply the concept to the learner's current generated project or dataset.

This is the highest-value bridge between the educational portal and the starter kit.

## Evaluation modes

### Deterministic

Use whenever the result is objectively checkable.

Examples:

- numerical answer with tolerance;
- expected matrix;
- expected DataFrame shape/content;
- metric value;
- environment state transition;
- learned table/value within an expected bound.

### Structural

Validate constraints that matter even when multiple implementations are valid.

Examples:

- target separated from features;
- train/test leakage avoided;
- original source data not mutated;
- time-aware split used for time series;
- required experiment metadata produced.

### Rubric / semantic

Use for explanations or interpretations where many valid answers exist.

A rubric should identify required ideas rather than an exact sentence.

An LLM may assist, but the portal should preserve the rubric and evidence so feedback is auditable.

## Open-solution principle

Where there are multiple valid implementation paths, define:

- input contract;
- required output;
- invariants;
- forbidden shortcuts when pedagogically relevant;
- optional efficiency/style feedback.

Do not require the learner's code to match a reference solution line-by-line.

## Hints

Hints should be progressive.

Suggested levels:

1. conceptual nudge;
2. identify the relevant concept/formula;
3. expose the next intermediate step;
4. show a partially solved example;
5. reveal the solution with explanation.

Using hints may affect XP but should not erase learning progress.

## Attempts and feedback

For each attempt, retain enough information to support later review:

- result;
- intermediate answer when applicable;
- hint usage;
- misconception tags;
- time/attempt count if useful;
- feedback shown.

Avoid turning speed into a major score unless the skill genuinely requires fluency.

## Mastery

Mastery should combine evidence from more than one activity type where appropriate.

Example for `Confusion Matrix`:

- construct a matrix from predictions;
- calculate one derived metric;
- interpret a false positive/false negative scenario.

This is stronger than ten multiple-choice questions.

## Review

Review should test retrieval rather than merely replaying the same lesson.

Possible review forms:

- short recall prompt;
- a changed numerical example;
- diagnose a new scenario;
- redo a previously weak concept;
- transfer to a different dataset.

## Misconception-driven review

When repeated errors reveal a specific confusion, create targeted review.

Example:

```text
Detected misconception: reward vs return

Before continuing to Bellman equations:
1. identify immediate reward in a trajectory;
2. compute return from the same point;
3. explain why the two values differ.
```

## Scoring layers

Keep these separate:

- **progress** — what was completed;
- **mastery** — demonstrated competence;
- **XP** — motivational/game layer;
- **review status** — whether retained understanding should be checked again.

A skill unlock should normally depend on mastery or explicit prerequisite completion, not raw XP.