# Learning model

## Standard learning loop

Each skill should follow the same conceptual progression unless the subject clearly does not need every step:

1. **Intuition** — explain what problem the concept solves and why it exists.
2. **Theory** — introduce the formal concept and vocabulary.
3. **Visualization** — make the mechanism observable whenever possible.
4. **Manual execution** — perform one small calculation or state transition when doing so exposes the mechanism.
5. **Guided experiment** — change inputs/parameters and predict what will happen.
6. **Library abstraction** — show the standard library/tool that performs the same operation at useful scale.
7. **Application** — solve a realistic task.
8. **Review** — retrieve the idea later without simply rereading it.
9. **Mastery checkpoint** — demonstrate enough understanding to unlock dependent skills.

## Manual-first rule

Important abstractions should not appear for the first time hidden behind a library call.

Examples where a manual execution is useful:

- mean over a few values;
- normalization of a few values;
- Euclidean distance between two points;
- one K-Means assignment/update step;
- one prediction from a known linear equation;
- building a confusion matrix from a small prediction set;
- precision/recall from that matrix;
- one gradient-descent weight update;
- discounted return in RL;
- one Bellman backup;
- one Q-learning update.

The portal should not require manual calculation when the operation becomes repetitive arithmetic without adding conceptual value.

## Prediction before execution

Whenever practical, ask the learner to predict the effect before running the experiment.

Examples:

- If `gamma` increases, what should happen to the importance of distant rewards?
- If K increases in K-Means, what do you expect to happen to within-cluster distance?
- If the classification threshold increases, what direction should precision/recall move?

This separates understanding from passive observation.

## Library-after-mechanism

After the learner performs the small mechanism manually, explicitly connect it to the abstraction:

> You just performed one operation that this library applies automatically and at scale.

The library phase should then teach:

- what the API hides;
- which inputs matter;
- which defaults matter;
- what the output means;
- common misuse;
- how to inspect the result.

## Transfer to the learner's project

Controlled examples are used first because they are easy to reason about.

As mastery increases, exercises should move through:

**toy data → curated public dataset → generated demo dataset → learner's own project/dataset**

This transfer is a core feature, not an optional appendix.

## Learning state

A skill may move through states such as:

- locked;
- available;
- started;
- theory reviewed;
- practice in progress;
- checkpoint attempted;
- acquired;
- needs review;
- mastered.

Completion and mastery are different concepts.

## Error memory

The portal should retain meaningful misconceptions, not only scores.

Examples:

- confused reward with return;
- confused feature with target;
- interpreted correlation as causation;
- mixed validation and test usage;
- calculated precision using the recall denominator.

A future review can target these misconceptions directly.

## LLM role

An LLM may help with:

- explanation in alternative wording;
- Socratic hints;
- semantic feedback;
- personalized examples;
- note summarization;
- open-ended review.

However, deterministic exercises should remain deterministically checkable whenever possible. Core progression must not require an LLM to decide results that can be verified by code or a known expected state.