# Theory and Reference Map

This document provides a curated list of trusted sources to help you verify concepts and go deeper into the machine learning theory used in this project.

## Core Machine Learning

### [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
- **What it supports**: General machine learning workflows, preprocessing, and model selection.
- **Where it applies**: Throughout the project, specifically during data preparation and training.
- **Beginner note**: This is the industry-standard documentation for Python ML. It is very dense but includes excellent narrative explanations alongside the code.
- **Limitation**: Focused on traditional machine learning; it does not cover deep learning or complex bandit scenarios in depth.

### [scikit-learn Model Evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html)
- **What it supports**: Definitions and math behind metrics like Accuracy, Precision, Recall, and RMSE.
- **Where it applies**: During the evaluation phase (`lab evaluate`) and when interpreting results.
- **Beginner note**: Essential for understanding *why* you choose one metric over another.
- **Limitation**: Focuses on how to calculate metrics, not necessarily how to handle business-specific costs of errors.

### [scikit-learn Generated Datasets](https://scikit-learn.org/stable/datasets/sample_generators.html)
- **What it supports**: The logic behind synthetic data generation.
- **Where it applies**: The Synthetic Data Lab and `lab synthetic` commands.
- **Beginner note**: Useful if you want to understand how "fake" data can still have realistic mathematical properties.
- **Limitation**: Covers standard distributions but won't explain how to simulate complex, domain-specific business rules.

## Multi-Armed Bandits (MAB)

### [Introduction to Multi-Armed Bandits (Slivkins)](https://arxiv.org/abs/1904.07272)
- **What it supports**: The mathematical foundations of bandit algorithms like UCB and Thompson Sampling.
- **Where it applies**: The Multi-Armed Bandit Lab and `bandit_lab.py`.
- **Beginner note**: This is a rigorous academic text. Start with the introduction and the first few chapters to get the intuition before diving into the proofs.
- **Limitation**: High mathematical overhead; might be overwhelming for absolute beginners without a calculus/statistics background.

### [Reinforcement Learning: An Introduction (Sutton & Barto)](http://incompleteideas.net/book/the-book-2nd.html)
- **What it supports**: Optional background on the broader field of Reinforcement Learning, of which MAB is a part.
- **Where it applies**: Theoretical context for decision-making under uncertainty.
- **Beginner note**: A classic "bible" of RL. Chapter 2 is dedicated entirely to Multi-Armed Bandits and is highly recommended.
- **Limitation**: Covers a much wider scope than this project requires; most of the book deals with sequential decision-making (MDPs) rather than the "one-shot" decisions in MAB.

---

*Note: These sources are external. While we trust them for theory, always prioritize the project's internal guides for specific implementation details.*
