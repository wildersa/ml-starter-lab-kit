# Module 02: Policy Gradients & Actor-Critic Architecture

## 1. Value-Based vs. Policy-Based Reinforcement Learning

In value-based methods like DQN, the policy is implicit: $\pi(a \vert s) = \arg\max_{a} Q(s, a; \theta)$. While effective for low-dimensional discrete action spaces, value-based approaches face fundamental limitations:

1. **Continuous Action Spaces**: Finding $\max_{a} Q(s, a)$ over continuous action spaces $\mathcal{A} \subseteq \mathbb{R}^d$ requires solving an inner optimization problem at every step, which is computationally intractable.
2. **Deterministic / Greedy Limits**: Value-based methods cannot naturally learn stochastic policies (e.g., in partially observable environments where rock-paper-scissors optimal strategies require exact probability distributions).
3. **Action-Value Sensitivity**: Small changes in estimated Q-values can cause abrupt discontinuous jumps in policy actions, leading to optimization oscillation.

### Direct Policy Parameterization

Policy-based methods parameterize the policy directly using a neural network with weights $\theta$:

$$\pi_\theta(a \vert s) = P(A_t = a \vert S_t = s; \theta)$$

- **Discrete Actions**: The network outputs logits transformed by a Softmax layer into an action probability vector.
- **Continuous Actions**: The network outputs distribution parameters (e.g., mean $\mu_\theta(s)$ and standard deviation $\sigma_\theta(s)$ of a Gaussian distribution $\mathcal{N}(\mu, \sigma^2)$).

---

## 2. The Policy Gradient Family & REINFORCE

### The Optimization Objective

We define the performance objective $J(\theta)$ as the expected cumulative discounted return under policy $\pi_\theta$:

$$J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta} [R(\tau)] = \int P(\tau; \theta) R(\tau) d\tau$$

where a trajectory $\tau = (s_0, a_0, s_1, a_1, \dots, s_T)$ has probability $P(\tau; \theta) = \mu(s_0) \prod_{t=0}^{T-1} \pi_\theta(a_t \vert s_t) P(s_{t+1} \vert s_t, a_t)$ and return $R(\tau) = \sum_{t=0}^{T} \gamma^t r_t$.

### The Policy Gradient Theorem & Log-Derivative Trick

Since environment dynamics $P(s_{t+1} \vert s_t, a_t)$ are unknown, we cannot compute $\nabla_\theta P(\tau; \theta)$ directly. Using the **log-derivative trick** ($\nabla_\theta P(\tau; \theta) = P(\tau; \theta) \nabla_\theta \log P(\tau; \theta)$), the policy gradient theorem proves:

$$\nabla_\theta J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta} \left[ \sum_{t=0}^{T} \nabla_\theta \log \pi_\theta(a_t \vert s_t) G_t \right]$$

where $G_t = \sum_{k=t}^{T} \gamma^{k-t} r_k$ is the empirical sample return from step $t$.

Notice that the unknown environment transition probabilities $P(s_{t+1} \vert s_t, a_t)$ disappear completely from the gradient formulation!

```text
Log-Probability Gradient Intuition:
∇_θ log π_θ(a_t | s_t) * G_t
        │                  │
        │                  ▼
        │             Return (Scalar Weight)
        ▼
Direction in parameter space that INCREASES probability of taking action a_t in s_t

- If G_t > 0: Push parameters θ to make action a_t MORE likely.
- If G_t < 0: Push parameters θ to make action a_t LESS likely.
```

### REINFORCE Algorithm (Monte Carlo Policy Gradient)

REINFORCE collects full episode trajectories before performing gradient updates:

$$\theta \leftarrow \theta + \alpha \sum_{t=0}^{T} \nabla_\theta \log \pi_\theta(a_t \vert s_t) G_t$$

**Drawback**: Because REINFORCE uses full trajectory returns $G_t$, sample variance is extremely high. A single lucky or unlucky action in a 1000-step episode corrupts credit assignment for all preceding actions.

---

## 3. Actor-Critic Architecture & Advantage Function

To reduce the high variance of Monte Carlo returns $G_t$, **Actor-Critic** architectures replace the full episode return $G_t$ with a learned value function baseline.

### The Advantage Function $A(s, a)$

The **Advantage** function quantifies how much better taking a specific action $a$ in state $s$ is compared to the average expected value of state $s$:

$$A(s, a) = Q(s, a) - V(s)$$

- $V(s)$: Expected return from state $s$ under current policy (evaluated by the **Critic**).
- $Q(s, a)$: Expected return taking action $a$ in state $s$ (evaluated by step environment execution).
- $A(s, a) > 0$: Action $a$ performed better than expected $\rightarrow$ increase action probability.
- $A(s, a) < 0$: Action $a$ performed worse than expected $\rightarrow$ decrease action probability.

### Actor-Critic Dual Network Split

An Actor-Critic agent splits responsibilities into two distinct roles:

```text
                       ┌─────────────────────────┐
                       │     State Vector s      │
                       └────────────┬────────────┘
                                    │
           ┌────────────────────────┴────────────────────────┐
           ▼                                                 ▼
┌─────────────────────┐                           ┌─────────────────────┐
│  Actor π_θ(a | s)   │                           │    Critic V_ϕ(s)    │
│  (Policy Network)   │                           │   (Value Network)   │
└──────────┬──────────┘                           └──────────┬──────────┘
           │                                                 │
           ▼ Output                                          ▼ Output
Action Distribution P(a|s)                           State Value V(s)
           │                                                 │
           └────────────────────────┬────────────────────────┘
                                    ▼
                     1-Step TD Error (Advantage Est)
                     δ_t = r_t + γ V_ϕ(s_{t+1}) - V_ϕ(s_t)
```

1. **Actor** ($\pi_\theta(a \vert s)$): Selects actions. Updated via policy gradient weighted by Advantage:
   $$\nabla_\theta J(\theta) \approx \mathbb{E} \left[ \nabla_\theta \log \pi_\theta(a_t \vert s_t) A(s_t, a_t) \right]$$
2. **Critic** ($V_\phi(s)$): Evaluates state values. Updated by minimizing Temporal Difference (TD) error:
   $$\mathcal{L}(\phi) = \frac{1}{2} \left( r_t + \gamma V_\phi(s_{t+1}) - V_\phi(s_t) \right)^2$$

### 1-Step Advantage Estimation (TD Error as Advantage)

Using the 1-step TD target $r_t + \gamma V_\phi(s_{t+1})$ as an unbiased estimator of $Q(s_t, a_t)$, the 1-step TD error $\delta_t$ serves as an immediate sample of the Advantage function:

$$\hat{A}_t = \delta_t = r_t + \gamma V_\phi(s_{t+1}) - V_\phi(s_t)$$

---

## 4. Proximal Policy Optimization (PPO)

### The Problem with Standard Policy Gradients: Unstable Policy Shifts

In standard policy gradients, taking a gradient step with a bad batch of data can drastically alter policy weights $\theta$. Because data collection depends directly on policy $\pi_\theta$, a damaged policy samples bad trajectories, leading to unrecoverable performance collapse.

### PPO Clipped Surrogate Objective

PPO (Schulman et al., 2017) prevents destructive policy updates by enforcing a trust-region constraint directly in the loss function without complex second-order optimizations.

Define the probability ratio $r_t(\theta)$ between the new policy $\pi_\theta$ and the old policy $\pi_{\theta_{\text{old}}}$ used to collect the data:

$$r_t(\theta) = \frac{\pi_\theta(a_t \vert s_t)}{\pi_{\theta_{\text{old}}}(a_t \vert s_t)}$$

- When $r_t(\theta) = 1$, the new policy matches the old policy.
- When $r_t(\theta) > 1$, the action is more likely under the new policy.

PPO defines its **Clipped Surrogate Objective** as:

$$L^{\text{CLIP}}(\theta) = \hat{\mathbb{E}}_t \left[ \min\left( r_t(\theta) \hat{A}_t, \, \text{clip}(r_t(\theta), 1 - \epsilon, 1 + \epsilon) \hat{A}_t \right) \right]$$

where $\epsilon$ is a hyperparameter (typically $\epsilon \in [0.1, 0.2]$).

```text
           PPO Clipped Objective behavior when Advantage A > 0 (Good Action):

    L_CLIP
      ▲
      │                              / (Unclipped r_t * A)
      │                             /
  (1+ε)A ───────────────────────────┬────────────── (Clipped Ceiling)
      │                            /
      │                           /
      │                          /
      │                         /
      └────────────────────────┴────────────────────► r_t(θ)
      0                       1.0          1+ε
```

### How Clipping Protects Optimization

1. **Positive Advantage ($\hat{A}_t > 0$)**: The action was better than average. We want to increase $r_t(\theta)$. However, once $r_t(\theta) > 1 + \epsilon$, the `clip` function caps the objective at $(1 + \epsilon) \hat{A}_t$. The gradient becomes zero, preventing the update from pushing the policy too far away from $\pi_{\theta_{\text{old}}}$.
2. **Negative Advantage ($\hat{A}_t < 0$)**: The action was worse than average. We want to decrease $r_t(\theta)$. Once $r_t(\theta) < 1 - \epsilon$, the objective is capped at $(1 - \epsilon) \hat{A}_t$, preventing excessive penalty steps.

This simple clipping mechanism guarantees stable, monotonic policy improvements across multiple minibatch training epochs on the same collected trajectory dataset.

---

## 5. Value vs. Policy vs. Actor-Critic Tradeoffs

| Mechanism | Primary Representation | Action Space Compatibility | Sample Efficiency | Training Stability | Primary Failure Mode |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **DQN / Double DQN** | $Q(s, a; \theta)$ (Value Network) | Discrete only | High (Off-policy Replay Buffer) | Moderate (Requires Target Net) | Overestimation bias; unstable continuous optimization. |
| **REINFORCE** | $\pi_\theta(a \vert s)$ (Policy Network) | Discrete & Continuous | Low (On-policy Monte Carlo) | Low (High variance returns) | High return variance; slow convergence. |
| **Actor-Critic** | $\pi_\theta(a \vert s)$ & $V_\phi(s)$ | Discrete & Continuous | Moderate (On/Off-policy variants) | High (Critic reduces variance) | Critic approximation bias; unstable joint learning rate. |
| **PPO** | $\pi_\theta(a \vert s)$ & $V_\phi(s)$ + Clipped Objective | Discrete & Continuous | High for Policy Methods | Very High (Clipped Trust Region) | Sensitivity to entropy coefficient and clip threshold $\epsilon$. |
