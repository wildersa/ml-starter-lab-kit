# Learning science foundations

## Status

This document defines the adopted learning-science foundation for the Learning Portal.

These principles are product decisions, not hypotheses to be validated before use. They should guide curriculum design, activity design, progression, review, and gamification unless a future product decision explicitly replaces them.

## Adopted foundation

The Learning Portal combines five primary foundations:

1. **Mastery Learning** — progression is based on demonstrated competence, not merely content completion.
2. **Cognitive Load management + Worked Examples + Scaffolding** — new concepts begin with bounded explanations and guided examples, then assistance is progressively removed.
3. **Retrieval Practice** — review requires recalling or applying knowledge rather than simply rereading it.
4. **Experiential Learning** — learners predict, execute, observe, and explain outcomes through experiments and interactive environments.
5. **Competency / Skill Graph** — learning progression is represented as a graph of demonstrable competencies with explicit prerequisites and unlocks.

Gamification is a presentation and motivation layer over these foundations. It is not the learning model itself.

## 1. Mastery Learning

### Product rule

The learner does not unlock an advanced skill simply because a lesson was viewed or completed.

Progression should depend on evidence that the prerequisite competency was demonstrated at the level required by the dependent skill.

The portal must distinguish:

- exposure;
- completion;
- acquisition;
- mastery;
- retention / review status.

A mastery threshold may be used for unlocking, but the threshold should be defined per skill or skill family rather than assuming one universal number for every competency.

### Product consequences

- Skill unlocks normally depend on mastery or explicit prerequisite completion.
- XP must never substitute for mastery.
- A learner may complete 100% of the activities but still require review.
- A previously acquired skill may later become `needs review` without erasing the achievement.
- Remediation should target the missing concept instead of forcing the learner to repeat an entire module.

## 2. Cognitive Load, Worked Examples, and Scaffolding

These are treated together as one design principle for the portal.

### Product rule

Do not expose a beginner to the full complexity of a concept when a smaller representation can reveal the mechanism first.

The default progression is:

**worked example → partially guided exercise → independent exercise → realistic application**

For mathematical or algorithmic concepts, use a small manual execution when it reveals the hidden mechanism. Stop requiring manual work when it becomes repetitive arithmetic rather than learning.

### Product consequences

- Bellman starts with a tiny state transition or GridWorld, not a large environment.
- Confusion matrix starts with a small set of known predictions.
- K-Means starts with a few points and centroids.
- Gradient descent starts with one understandable update, not a full training loop.
- Hints reveal progressively more structure instead of immediately revealing the answer.
- Guidance is deliberately reduced as the learner demonstrates competence.

The library abstraction should normally appear after the learner understands what the abstraction is doing.

## 3. Retrieval Practice

### Product rule

Review is an active attempt to retrieve or apply knowledge after the original lesson.

Simply reopening the same explanation is not considered sufficient review.

### Product consequences

Review activities may ask the learner to:

- explain a concept without seeing the definition;
- solve a changed numerical example;
- identify an error in a new scenario;
- compare two related concepts;
- apply the skill to a different dataset or environment;
- revisit a recorded misconception.

The portal should reuse evidence from previous attempts to decide what deserves review.

## 4. Experiential Learning

### Product rule

Whenever the concept can produce an observable consequence, the learner should interact with that consequence.

A preferred activity loop is:

**predict → execute → observe → explain**

Prediction before execution is important because it separates prior understanding from retrospective explanation.

### Product consequences

Examples include:

- predict how `gamma` changes the relevance of distant rewards, then run the environment;
- predict how a classification threshold changes precision/recall, then inspect the metrics;
- move a centroid and observe assignments;
- add an outlier and inspect descriptive statistics;
- change rewards in GridWorld and observe policy/value changes;
- change a preprocessing step and inspect model behavior.

The experiment should expose the causal mechanism being taught as clearly as practical.

## 5. Competency / Skill Graph

### Product rule

The portal represents learning as a directed graph of competencies rather than one fixed linear course.

A node represents a demonstrable skill. Edges represent real learning dependencies, not merely textbook adjacency.

### Product consequences

- Multiple prerequisite branches may converge on one advanced skill.
- One mastered skill may unlock multiple possible next paths.
- The learner can have some autonomy over available paths without bypassing required prerequisites.
- The graph must explain why a locked node is locked.
- Completed branches may award meaningful specializations or achievements.

The graph is the product model for progression; the curriculum is one recommended traversal through it.

## Gamification boundary

Gamification should reinforce competence and visible progress without becoming the authority over learning.

Allowed mechanisms include:

- XP;
- skill acquisition animations;
- badges / achievements;
- branch completion;
- visible graph expansion;
- optional challenges;
- streak-like review encouragement if it does not punish normal breaks.

The following rules apply:

- XP does not unlock a skill that requires mastery.
- Completing a screen does not automatically grant a competency.
- Badges should describe meaningful competence or milestones.
- Speed should not be a major score unless fluency is genuinely part of the skill.
- Game mechanics must not encourage skipping explanations, abusing hints, or optimizing points instead of understanding.

## Self-Determination Theory as a UX principle

Self-Determination Theory is not a separate progression engine in the initial product, but its principles should influence UX decisions:

- **competence** — show understandable progress and successful skill acquisition;
- **autonomy** — allow meaningful choice among currently valid learning paths;
- **relatedness** — optional future social/tutor features may support connection, but they are not required for the first version.

Autonomy never means bypassing a real prerequisite.

## Knowledge Tracing boundary

Bayesian Knowledge Tracing, Deep Knowledge Tracing, or another probabilistic learner model is not required for the initial Learning Portal.

The initial system should use explicit, inspectable evidence such as:

- checkpoint results;
- activity results;
- attempt history;
- hints used;
- misconception tags;
- review outcomes;
- transfer exercise results.

A future knowledge-tracing model may estimate mastery from this history, but it must not be necessary to make the first version pedagogically coherent.

## Adopted lesson pattern

Unless a skill has a clear reason to omit a step, authoring should follow this sequence:

1. establish intuition and purpose;
2. introduce vocabulary and theory;
3. visualize the mechanism;
4. show a worked example;
5. require a small guided/manual execution where useful;
6. ask for a prediction;
7. run an interactive experiment;
8. remove part of the scaffolding;
9. introduce the standard library/tool abstraction;
10. apply the concept to a realistic task;
11. perform a mastery checkpoint;
12. revisit the skill later through retrieval practice;
13. transfer the skill to a different or learner-owned dataset/environment when appropriate.

This is the default methodology of the Learning Portal.

## Foundational references

These works inform the adopted design. They are references for the learning methodology; their inclusion here does not imply permission to copy their protected text, figures, exercises, or other content.

- Bloom, B. S. (1968). *Learning for Mastery*.
- Sweller, J. (1988). *Cognitive Load During Problem Solving: Effects on Learning*.
- Atkinson, R. K., Derry, S. J., Renkl, A., & Wortham, D. (2000). *Learning from Examples: Instructional Principles from the Worked Examples Research*.
- Roediger, H. L., & Karpicke, J. D. (2006). *Test-Enhanced Learning: Taking Memory Tests Improves Long-Term Retention*.
- Kolb, D. A. (1984). *Experiential Learning*.
- Ryan, R. M., & Deci, E. L. (2000). *Self-Determination Theory and the Facilitation of Intrinsic Motivation, Social Development, and Well-Being*.

The project should create its own explanations, exercises, visualizations, and examples unless a source is explicitly licensed for adaptation under the policy defined in `05-content-sources-and-licensing.md`.
