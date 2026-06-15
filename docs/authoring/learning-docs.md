# Learning Documentation Authoring Guide

This guide defines the rules for authoring learning content to ensure it is copyright-safe, accurate, and concise.

## Source Roles

When authoring documentation, stick to these approved sources based on the content type:

| Role | Source | Scope |
|---|---|---|
| **Practical / API** | [scikit-learn documentation](https://scikit-learn.org/) | Primary source for classical Machine Learning topics, implementation details, and API patterns. |
| **Theory** | [Slivkins (2019) - Introduction to Multi-Armed Bandits](https://arxiv.org/abs/1904.07272) | Primary source for Multi-Armed Bandit (MAB) theory. |
| **Optional Background** | [Sutton & Barto (2018) - Reinforcement Learning: An Introduction](http://incompleteideas.net/book/the-book-2nd.html) | Background context for Reinforcement Learning (RL) only. |

## Copyright-Safe Rules

To protect intellectual property and avoid plagiarism:

1.  **No Direct Copying**: Do not copy paragraphs, figures, tables, paper abstracts, or exercises from any source, including the approved ones.
2.  **Synthesize and Rephrase**: Explain concepts in your own words. Focus on how the concept applies to this project's tools and workflows.
3.  **No Independent Research**: Do not ask AI agents (like Jules) to research new bibliography or external sources unless explicitly requested by a human author.
4.  **No Invented Bibliography**: Only use the sources listed in this guide or those specifically provided for a task.

## Authoring Principles

-   **Conciseness over Academic Depth**: Prefer short "Learn more" sections over academic-heavy documentation. The goal is to get the user started, not to provide a comprehensive theoretical foundation.
-   **Practical Focus**: Always link theoretical concepts back to the project's code, CLI commands (`lab`), or generated artifacts.
-   **Limitation Notes**: Every document covering theoretical concepts **must** include a "Limitations" or "When not to use" note to provide realistic expectations.

## Agent Instructions

If you are an AI agent:
- Follow the rules above strictly.
- Do not "hallucinate" or search for additional academic papers to cite.
- If a concept is not covered by the approved sources and you haven't been given specific material, keep the explanation high-level and focused on the practical implementation in the codebase.
