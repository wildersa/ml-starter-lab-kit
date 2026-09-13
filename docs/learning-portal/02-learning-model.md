# Learning model

## Adopted foundation

The Learning Portal uses the methodology defined in [`09-learning-science-foundations.md`](09-learning-science-foundations.md) as its default educational model.

The core foundations are:

- Mastery Learning;
- Cognitive Load management + Worked Examples + Scaffolding;
- Retrieval Practice;
- Experiential Learning;
- Competency / Skill Graph progression.

Gamification is layered on top of this model and must not become the authority for progression.

## Standard learning loop

Each skill should follow the same conceptual progression unless the subject clearly does not need every step:

1. **Intuition** — explain what problem the concept solves and why it exists.
2. **Theory** — introduce the formal concept and vocabulary.
3. **Visualization** — make the mechanism observable whenever possible.
4. **Worked example** — show one small, understandable execution before asking for independent problem solving.
5. **Manual or guided execution** — perform one small calculation or state transition when doing so exposes the mechanism.
6. **Prediction** — ask what the learner expects before an experiment is run.
7. **Guided experiment** — change inputs/parameters and observe what happens.
8. **Reduced scaffolding** — require a similar task with less help.
9. **Library abstraction** — show the standard library/tool that performs the same operation at useful scale.
10. **Application** — solve a realistic task.
11. **Mastery checkpoint** — demonstrate enough understanding to acquire/unlock dependent skills.
12. **Retrieval review** — revisit the skill later without simply rereading it.
13. **Transfer** — apply the skill to a different or learner-owned dataset/environment where appropriate.

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

## Worked examples and scaffolding

A beginner should not be pushed directly from theory into a full independent problem when a smaller guided progression can expose the mechanism first.

The preferred progression is:

**worked example → partially guided exercise → independent exercise → realistic application**

Hints and structural guidance should decrease as competence increases.

## Prediction before execution

Whenever practical, ask the learner to predict the effect before running the experiment.

Examples:

- If `gamma` increases, what should happen to the importance of distant rewards?
- If K increases in K-Means, what do you expect to happen to within-cluster distance?
- If the classification threshold increases, what direction should precision/recall move?

This separates understanding from passive observation and supports the experiential loop:

**predict → execute → observe → explain**

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

A learner may keep an acquired skill while its review status changes if later retrieval evidence shows that understanding weakened.

## Error memory

The portal should retain meaningful misconceptions, not only scores.

Examples:

- confused reward with return;
- confused feature with target;
- interpreted correlation as causation;
- mixed validation and test usage;
- calculated precision using the recall denominator.

A future review can target these misconceptions directly.

## Retrieval review

Review should require the learner to retrieve or apply knowledge again instead of only reopening the lesson.

Examples:

- explain the concept without seeing the definition;
- solve a changed numerical example;
- diagnose a new scenario;
- compare two similar concepts;
- transfer the skill to another dataset or environment.

## LLM role

An LLM may help with:

- explanation in alternative wording;
- Socratic hints;
- semantic feedback;
- personalized examples;
- note summarization;
- open-ended review.

However, deterministic exercises should remain deterministically checkable whenever possible. Core progression must not require an LLM to decide results that can be verified by code or a known expected state.

## Initial mastery implementation

The first version should use explicit and inspectable evidence such as checkpoint results, attempts, hint usage, misconception tags, review outcomes, and transfer activities.

Probabilistic Knowledge Tracing is intentionally deferred. It may be added later without changing the learning model.