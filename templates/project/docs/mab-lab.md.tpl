# Multi-Armed Bandit Lab — Reference

Multi-Armed Bandit (MAB) is a sequential decision-making problem under uncertainty.

## 1. What is Multi-Armed Bandit

The classic idea is: there is a set of options, called **arms** or **actions**. In each round, the agent chooses one of these actions, observes a reward from that action, and uses this feedback to make better decisions in future rounds.

Unlike supervised learning, the agent does not receive a fixed dataset with a known target for all examples. It learns while deciding.

Simplified comparison:

```txt
Supervised Learning:
fixed dataset -> known target -> training -> evaluation

Multi-Armed Bandit:
choose an action -> observe partial reward -> update policy -> choose again
```

This difference is central. MAB represents another type of problem: **sequential decision making with partial feedback**.

## 2. Key Concepts

### Arm / Action
An **arm** is an option the agent can choose.
Examples: different versions of an offer, different marketing messages, or different product recommendations.

### Reward
The **reward** is the feedback observed after choosing an arm. In the simplest case, it is binary: 1 for success, 0 for failure.

### Policy
The **policy** defines how the agent chooses the next arm.
Examples: Random, Epsilon-Greedy, UCB, Thompson Sampling.

### Exploration vs. Exploitation
The central dilemma of MAB is balancing:
- **Exploration**: testing less-known arms to learn more.
- **Exploitation**: using the arm that seems best so far.

### Regret
**Regret** measures how much the agent missed out on by not always choosing the best arm. In a simulation, we calculate it as the difference between the best possible reward and the reward obtained by the policy.

## 3. Recommended Policies

### Epsilon-Greedy
Mixes random exploration with exploitation. With probability `epsilon`, it explores; otherwise, it chooses the best known arm.

### UCB1 (Upper Confidence Bound)
Chooses arms optimistically by adding an uncertainty bonus to the observed mean. Arms that are less tested get a higher bonus.

### Thompson Sampling
A Bayesian approach that maintains a probability distribution for each arm and samples from it to make decisions. It handles exploration naturally through uncertainty.

## 4. Next Steps

If you are coming from a supervised learning background, we recommend reading the **[Bandit Walkthrough](bandit-walkthrough.md)** to understand how to map your dataset to these concepts.

## Learn more

- **Theory**: Aleksandrs Slivkins, [Introduction to Multi-Armed Bandits](https://arxiv.org/abs/1904.07272).
- **General ML Metrics**: scikit-learn [Model Evaluation Guide](https://scikit-learn.org/stable/modules/model_evaluation.html).

**Limitation**: The MAB Lab uses simplified simulations. Real-world results may vary due to complex environmental factors not captured in these models.
