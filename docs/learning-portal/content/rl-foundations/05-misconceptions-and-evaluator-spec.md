---
id: rl-foundations-05-misconceptions
title: Misconceptions Taxonomy and Portal Evaluator Specification
track: reinforcement-learning
node_id: rl-misconceptions-and-evaluator-spec
prerequisites: [rl-worked-examples-and-checkpoints]
unlocks: [portal-rl-evaluator-engine]
sources_ref: sources-and-licenses.md
---

# Misconceptions Taxonomy and Portal Evaluator Specification

## Overview

This specification establishes a machine-readable taxonomy of student misconceptions in Reinforcement Learning. When a learner submits a calculation, code snippet, or diagnostic answer in the Learning Portal, the **Evaluator Engine** matches error patterns against these misconception codes to provide targeted pedagogical feedback rather than generic failure messages.

---

## 1. Misconceptions Taxonomy (`MISC_*`)

### Category A: RL Vocabulary & MDP Foundations

| Misconception Code | Title | Description | Diagnostic Detection Rule |
| :--- | :--- | :--- | :--- |
| `MISC_REWARD_VS_RETURN` | Confusing Reward with Return | Adding or reporting immediate scalar reward $R_{t+1}$ as if it were total return $G_t$. | Calculated return $G_t$ equals immediate $R_{t+1}$ while future rewards exist and $\gamma > 0$. |
| `MISC_DISCOUNT_RANGE` | Invalid Discount Factor | Setting or assuming $\gamma \ge 1.0$ or $\gamma < 0.0$. | Input $\gamma \ge 1.0$ or $\gamma < 0$. |
| `MISC_MARKOV_MEMORY` | Over-attributing State Memory | Assuming a Markov state must store historical trajectories $(S_0, S_1, \dots)$ explicitly. | Answering that $S_t$ requires full historical trajectory log rather than sufficient summary features. |
| `MISC_OBS_VS_STATE` | Treating Observation as True State in POMDP | Assuming local sensor observation $O_t$ contains complete world state in partially observable environments. | Ignoring hidden environment variables in probability transition calculations. |

---

### Category B: Value Functions & Bellman Equations

| Misconception Code | Title | Description | Diagnostic Detection Rule |
| :--- | :--- | :--- | :--- |
| `MISC_V_VS_Q` | Confusing $V(s)$ with $Q(s,a)$ | Treating state value $V(s)$ as action-dependent or attempting to index $V(s)$ with an action $a$. | Calling `V[s][a]` or defining $V(s,a)$ as a function of action. |
| `MISC_BELLMAN_MAX_VS_AVG` | Using $\max_a$ in Expectation Equation | Replacing policy probabilities $\sum_a \pi(a \mid s)$ with $\max_a$ when calculating $V^\pi(s)$ for a non-greedy policy. | Calculating $V^\pi(s) = \max_a Q(s,a)$ when policy $\pi$ is stochastic/non-greedy. |
| `MISC_BELLMAN_DISCOUNT_OMISSION` | Omitting Discount in Bellman Backup | Computing $V(s) = R + V(s')$ without multiplying the future state value by $\gamma$. | Calculated $V(s) = R + V(s')$ when $\gamma \neq 1.0$. |
| `MISC_TRANSITION_PROB_SUM` | Non-Normalized Transition Probabilities | Failing to sum expected values over all possible transition states $s'$ weighted by $\mathcal{P}(s' \mid s,a)$. | Multiplying by only one branch in a stochastic branch transition. |

---

### Category C: Temporal Difference & Control Algorithms

| Misconception Code | Title | Description | Diagnostic Detection Rule |
| :--- | :--- | :--- | :--- |
| `MISC_Q_MAX_VS_POLICY` | Confusing Q-Target with Executed Action | Believing Q-Learning requires the agent to execute action $\arg\max_{a'} Q(S_{t+1}, a')$ at $t+1$. | Stating that Q-Learning cannot explore because its target uses $\max_a$. |
| `MISC_SARSA_ON_POLICY` | Treating SARSA as Off-Policy | Using $\max_{a'} Q(S_{t+1}, a')$ in a SARSA target instead of $Q(S_{t+1}, A_{t+1})$. | Student labels SARSA update as off-policy or uses $\max$ in SARSA calculation. |
| `MISC_ALPHA_OVERFLOW` | Invalid Learning Rate | Setting $\alpha > 1.0$ or $\alpha \le 0.0$. | Update value diverges or $\alpha$ parameter out of $(0, 1]$ bounds. |
| `MISC_TD_TARGET_CONFUSION` | Mixing MC Return into TD Update | Using total episode return $G_t$ inside a 1-step TD update instead of $R_{t+1} + \gamma V(S_{t+1})$. | Student equation uses $G_t$ in $V(S_t) \leftarrow V(S_t) + \alpha [G_t - V(S_t)]$. |

---

## 2. Automated Feedback & Diagnostic Responses

### Example 1: Learner commits `MISC_BELLMAN_DISCOUNT_OMISSION`

- **Learner Submission**:
  $$V(S_0) = 15.0 + 30.0 = 45.0 \quad (\text{with } \gamma = 0.9, R = 15, V(S_1) = 30)$$
- **Evaluator Diagnostic**:
  - Detected: Student added $R + V(S_1)$ directly without applying discount $\gamma$.
- **Evaluator Response**:
  > ⚠️ **Misconception Detected (`MISC_BELLMAN_DISCOUNT_OMISSION`)**:
  > You added the immediate reward ($15.0$) directly to the future state value ($30.0$) without discounting!
  > Remember that future rewards are worth less today. Multiply $V(S_1)$ by $\gamma = 0.9$ before adding immediate reward:
  > $$V(S_0) = R + \gamma V(S_1) = 15.0 + (0.9 \times 30.0) = 15.0 + 27.0 = 42.0$$

---

### Example 2: Learner commits `MISC_SARSA_ON_POLICY`

- **Learner Submission**:
  Calculating SARSA target as $R_{t+1} + \gamma \max_{a'} Q(S_{t+1}, a')$.
- **Evaluator Diagnostic**:
  - Detected: Student used max operator in SARSA update step.
- **Evaluator Response**:
  > ⚠️ **Misconception Detected (`MISC_SARSA_ON_POLICY`)**:
  > You used $\max_{a'} Q(S_{t+1}, a')$ inside a SARSA update!
  > That is the **Q-Learning** target (Off-Policy).
  > For **SARSA** (On-Policy), you must evaluate the actual action $A_{t+1}$ chosen by the current policy:
  > $$\text{Target}_{\text{SARSA}} = R_{t+1} + \gamma Q(S_{t+1}, A_{t+1})$$

---

## 3. Evaluator JSON Schema Contract

When an exercise cell is evaluated in the portal, the evaluator outputs structured feedback matching this schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "RLEvaluatorFeedback",
  "type": "object",
  "properties": {
    "skill_id": { "type": "string" },
    "exercise_id": { "type": "string" },
    "passed": { "type": "boolean" },
    "score": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
    "misconception_tag": { "type": ["string", "null"] },
    "diagnostic_message": { "type": "string" },
    "remediation_hint": { "type": "string" },
    "suggested_review_node": { "type": "string" }
  },
  "required": ["skill_id", "exercise_id", "passed", "score", "diagnostic_message"]
}
```

---

## 4. Remediation Mapping

| Trigger Tag | Remediation Reading | Targeted Practice Activity |
| :--- | :--- | :--- |
| `MISC_REWARD_VS_RETURN` | Read `01-agent-environment-and-mdp.md#reward-vs-return` | Solve 3 discounted return trajectories with different $\gamma$. |
| `MISC_BELLMAN_MAX_VS_AVG` | Read `02-policies-and-value-functions.md#bellman-expectation` | Perform one expectation backup on a 3-action stochastic policy. |
| `MISC_SARSA_ON_POLICY` | Read `03-temporal-difference-and-control.md#sarsa-vs-qlearning` | Calculate side-by-side Q-Learning vs SARSA updates on the same transition. |
