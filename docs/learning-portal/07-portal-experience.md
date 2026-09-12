# Portal experience

## Home

The home surface should answer three questions immediately:

- What am I learning now?
- What can I learn next?
- What needs review?

Suggested blocks:

- current skill;
- recommended next skill;
- skills needing review;
- current branch/specialization progress;
- recent notes;
- link to the full skill graph.

## Skill graph view

The graph is the main map of the learning system.

It should show:

- acquired skills;
- mastered skills;
- available skills;
- locked skills;
- prerequisite edges;
- review warnings;
- current path;
- branch achievements.

Selecting a locked node should explain exactly why it is locked.

## Skill detail

A skill page should not be one long static article.

Suggested sequence:

1. why this matters;
2. intuition;
3. concise theory;
4. interactive visualization;
5. learner notes;
6. manual activity when useful;
7. guided experiment;
8. standard library/tool usage;
9. practical activity;
10. checkpoint;
11. references/further reading;
12. transfer to current project when applicable.

The learner should be able to leave and return without losing intermediate state.

## Notes

Each skill should provide a personal notebook area.

Suggested note sections:

- My explanation
- What I did not understand
- My example
- Mistakes I made
- Summary

Notes should belong to the learner's progress state, not to the source curriculum content.

Future LLM assistance may:

- summarize notes;
- compare a note with required concepts;
- generate recall questions from the learner's own wording;
- identify unresolved questions.

The learner should always retain the original notes.

## Exercise workspace

The portal should support different interaction surfaces depending on the activity:

- numeric/formula input;
- tables/grids;
- drag/drop or visual state manipulation;
- DataFrame preview;
- chart interaction;
- small code/runtime cells;
- notebook-like experiment areas;
- text response;
- parameter controls and simulation.

Do not force every activity into a notebook or every activity into a form.

## Manual calculation workspace

For formula-based concepts, the UI should expose intermediate terms.

Example: discounted return

```text
Rewards: 2, 3, -1
Gamma: 0.9

G_t = ____ + ____ × ____ + ____ × ____²
Result = ____
```

Example: Q-learning

Show separately:

- current Q;
- reward;
- gamma;
- max next Q;
- TD target;
- TD error;
- learning rate;
- updated Q.

This makes the equation observable rather than asking for one opaque final number.

## Visual simulation

Concepts that benefit from spatial or temporal intuition should have interactive simulations.

Examples:

- GridWorld for MDP/value/Bellman/RL;
- movable points/centroids for K-Means;
- threshold slider for classification;
- regression line and residuals;
- train/validation/test timeline for time series;
- tiny neural network forward/backward visualization.

## Review center

The portal should have a dedicated review surface driven by evidence.

Priorities may include:

- skill marked `needs review`;
- repeated misconception;
- prerequisite weakness affecting a desired skill;
- long time since successful retrieval;
- learner manually requesting review.

Review should use new variants rather than simply reopen the original lesson.

## Project transfer

When the user opens the portal from a generated project, learning activities may use project context.

Examples:

- identify the project's target and features;
- perform EDA on the current dataset;
- build a baseline;
- calculate real project metrics;
- inspect feature importance;
- detect potential leakage;
- connect experiment results to MLOps skills.

The portal should clearly distinguish:

- controlled teaching data;
- public/curated datasets;
- generated demo data;
- user's own data.

## Offline / deterministic baseline

Core navigation, theory, exercises, notes, deterministic checking, progress, and graph unlocking should work without an LLM.

An LLM is an enhancement layer, not the learning portal's runtime foundation.

## Accessibility and pedagogy

The portal should avoid visually impressive interactions that obscure the concept.

Every visualization should answer a pedagogical question.

Examples:

- What changed?
- Why did it change?
- Which term in the formula caused it?
- What would happen if I changed this parameter?

## First implementation target

The first portal version does not need all tracks.

A good vertical slice should prove the engine with a small connected subgraph, for example:

- RL foundations;
- return and discounting;
- MDP;
- value functions;
- Bellman equation;
- one small interactive GridWorld.

This slice exercises graph dependencies, theory, notes, manual calculations, visualization, checkpoints, and unlocking without requiring the entire curriculum.