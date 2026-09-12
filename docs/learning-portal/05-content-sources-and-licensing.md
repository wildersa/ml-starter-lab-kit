# Content sources and licensing

## Goal

Use high-quality educational and scientific references without turning the project into a copy of external books or courses.

The preferred model is:

1. use openly licensed material when adaptation is useful and license-compatible;
2. use books and papers as theoretical references when adaptation rights are unclear or restricted;
3. write original explanations, examples, diagrams, and exercises whenever practical;
4. preserve attribution and license metadata for every imported or adapted asset.

## Source categories

### Category A — openly licensed educational content

These sources may be candidates for adaptation when their exact license conditions are satisfied.

#### Dive into Deep Learning (D2L)

Use for:

- deep learning foundations;
- neural networks;
- optimization;
- computer vision;
- sequence models;
- reinforcement learning references where useful.

License status:

- book content: Creative Commons Attribution-ShareAlike 4.0 International (`CC BY-SA 4.0`);
- sample/reference code has a separate permissive license described by the project.

Official references:

- https://d2l.ai/
- https://github.com/d2l-ai/d2l-en
- https://github.com/d2l-ai/d2l-en/blob/master/LICENSE

Important consequence: adapted book content must comply with attribution and ShareAlike requirements. Do not mix adapted CC BY-SA material into our own original material without explicitly tracking that provenance.

#### OpenIntro Statistics

Use for:

- descriptive statistics;
- probability;
- distributions;
- statistical foundations;
- regression/statistical interpretation.

License status:

- most OpenIntro resources, including statistics textbooks, are released under `CC BY-SA 3.0`;
- some resources are exceptions and may use different terms;
- if a specific OpenIntro file has no license, do not assume it is openly licensed.

Official references:

- https://www.openintro.org/
- https://www.openintro.org/license/
- https://www.openintro.org/book/os/

#### Hugging Face educational material

Potential use:

- modern ML/deep learning references;
- deep reinforcement learning examples and course structure;
- practical exercises around modern libraries.

The Hugging Face Course repository is published under Apache License 2.0. For any Deep RL-specific content, verify the license of the exact repository or asset before adaptation instead of assuming every Hugging Face educational surface has identical terms.

Official references:

- https://github.com/huggingface/course
- https://huggingface.co/learn
- https://huggingface.co/learn/deep-rl-course

### Category B — open-source library documentation

These are especially useful for the phase after the learner has understood the mechanism manually.

#### scikit-learn

Use for:

- classification;
- regression;
- clustering;
- preprocessing;
- metrics;
- inspection;
- model selection;
- examples of standard library workflows.

License: BSD.

Official reference:

- https://scikit-learn.org/

#### pandas

Use for:

- DataFrame/Series concepts;
- data selection;
- cleaning;
- transformations;
- aggregation;
- tabular data workflow.

License: BSD 3-Clause.

Official references:

- https://pandas.pydata.org/docs/
- https://pandas.pydata.org/docs/getting_started/overview.html

### Category C — scientific books and papers used as references

A freely accessible PDF does not automatically mean that the content may be copied or adapted into the project.

#### Sutton & Barto — Reinforcement Learning: An Introduction

This should be one of the central theoretical references for the RL curriculum.

Use it to validate:

- terminology;
- concept dependencies;
- ordering of foundational ideas;
- MDP/value-function/Bellman structure;
- Monte Carlo and Temporal Difference foundations;
- control methods.

Policy:

- cite the work;
- use chapter/section references where useful;
- write our own explanation;
- create our own diagrams and examples;
- create our own exercises;
- do not copy chapters, figures, tables, or substantial passages merely because an official PDF is available online.

Official author/book site:

- http://incompleteideas.net/book/the-book-2nd.html

#### Research papers

Papers should be used to support historical or algorithmic claims and to link advanced skills to original research.

For each paper:

- record title, authors, year, DOI/arXiv/publisher URL;
- inspect the actual license before reproducing material;
- prefer original explanations and original diagrams;
- quote only when genuinely needed and keep quotations short;
- use citations rather than copied text as the default.

## Content provenance metadata

Every externally derived or adapted educational asset should carry provenance metadata such as:

- `source_title`
- `source_authors`
- `source_url`
- `source_type`
- `license`
- `adapted`
- `attribution_required`
- `changes_noted`
- `original_content`

The exact storage format will be defined during implementation.

## Project copyright rule

> If the license is unknown, do not import or adapt the material. Use it only as a reference for independently written content until licensing is verified.

This applies to:

- text;
- diagrams;
- screenshots;
- exercises;
- datasets;
- notebooks;
- code samples;
- icons and other media.

## Preferred authoring model

Even when adaptation is legally allowed, prefer original project-specific teaching material when it improves consistency.

A strong content unit should normally contain:

- our own explanation;
- our own example;
- our own visualization or interactive representation;
- our own exercise;
- citations to the theoretical sources that support it.

Openly licensed sources are then used as validated foundations and optional further reading, not as a reason to duplicate another course.

## Dataset licensing

Datasets require the same discipline as educational content.

Before bundling any dataset, record:

- source;
- license or terms of use;
- whether redistribution is allowed;
- whether modification is allowed;
- attribution requirements;
- privacy or sensitive-data concerns.

Where redistribution rights are unclear, prefer:

- a download script/instruction that retrieves data from the original source; or
- a project-owned synthetic dataset with documented generation logic.

## Verification status

The source list above is an initial catalog. Exact license terms must be rechecked at the source before we directly adapt a specific external asset because licenses, repositories, and individual files may differ or change.