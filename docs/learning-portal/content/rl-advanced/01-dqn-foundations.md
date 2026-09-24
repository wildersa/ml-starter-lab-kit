# Module 01: Deep Q-Networks (DQN) Foundations

## 1. The Conceptual Bridge: Tabular Q-Table to Neural Function Approximator

In tabular Q-Learning, the action-value function $Q(s, a)$ is stored as a 2D lookup matrix `Q[state_index, action_index]`. When an agent experiences transition $(s, a, r, s')$, the Bellman optimality update directly alters a single table cell:

$$Q[s, a] \leftarrow Q[s, a] + \alpha \left( r + \gamma \max_{a'} Q[s', a'] - Q[s, a] \right)$$

This tabular formulation breaks down in real-world environments with large or continuous state spaces (e.g., pixel inputs or physical sensor streams). An uncountably infinite state space makes full coverage impossible and prevents generalization: learning what action to take in state $s$ provides zero information about state $s + \epsilon$.

### The Function Approximation Bridge

To scale to high-dimensional state spaces, we replace the lookup table with a parameterized function approximator (a deep neural network with parameters $\theta$):

$$\text{Tabular Lookup: } Q[s, a] \quad \longrightarrow \quad \text{Neural Approximator: } Q(s, a; \theta) \approx Q^*(s, a)$$

```text
Tabular Approach (Lookup):
[State Index] ---> [ Matrix Lookup Q[s, :] ] ---> [Q(s, a1), Q(s, a2), Q(s, a3)]

Neural Function Approximator (DQN):
[Continuous State Vector s] ---> [ Neural Network (Weights θ) ] ---> [Q(s, a1; θ), Q(s, a2; θ), Q(s, a3; θ)]
```

In this architecture:
1. The neural network takes the continuous state vector $s \in \mathbb{R}^d$ as input.
2. The output layer outputs a vector of scalar $Q$-values, one for each discrete action $a \in \mathcal{A}$.
3. Updating $\theta$ via gradient descent allows the network to generalize $Q$-value predictions across similar unvisited states.

---

## 2. Why Naive Deep Q-Learning Fails: The 3 Instabilities

Simply substituting $Q(s, a; \theta)$ into the standard Temporal Difference (TD) update and fitting via online stochastic gradient descent (SGD) causes extreme instability or complete divergence. Deep Q-learning requires three critical mechanisms to achieve convergence.

```text
Sequential Experience (s_t, a_t, r_t, s_{t+1})
               │
               ▼
┌──────────────────────────────┐
│     1. Replay Buffer         │ ───► Breaks temporal correlations & enables i.i.d. minibatches
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│     2. Minibatch SGD         │ ───► Reduces gradient variance & stabilizes parameter updates
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│     3. Target Network θ⁻     │ ───► Fixes moving target problem during Bellman updates
└──────────────────────────────┘
```

---

## 3. Step 1: Replay Buffer (Experience Replay)

### The Problem: Temporal Correlations
Online RL collects data sequentially: $(s_t, a_t, r_t, s_{t+1}), (s_{t+1}, a_{t+1}, r_{t+1}, s_{t+2}), \dots$. Sequential transitions are strongly non-i.i.d. (independent and identically distributed). Standard SGD optimization assumes i.i.d. samples. Training a neural network on highly correlated sequential transitions leads to catastrophic forgetting and feedback loops (e.g., if the agent turns left, the next 50 samples are all "turning left in state $s'$", causing gradient updates to overfit to localized spatial regions).

### The Mechanism
A **Replay Buffer** $\mathcal{D}$ is a bounded, first-in-first-out (FIFO) memory pool storing state transitions:

$$\mathcal{D} = \{ e_1, e_2, \dots, e_N \}, \quad \text{where } e_t = (s_t, a_t, r_t, s_{t+1}, d_t)$$

where $d_t \in \{0, 1\}$ is a boolean flag indicating episode termination.

```python
import random
from collections import deque

class ReplayBuffer:
    def __init__(self, capacity: int):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size: int):
        transitions = random.sample(self.buffer, batch_size)
        # Unpack tuple batch into aligned arrays
        states, actions, rewards, next_states, dones = zip(*transitions)
        return states, actions, rewards, next_states, dones

    def __len__(self):
        return len(self.buffer)
```

### Why it works
1. **Breaks Correlations**: Sampling transitions uniformly at random from $\mathcal{D}$ decorrelates consecutive training samples, satisfying the i.i.d. assumption of gradient descent.
2. **Sample Efficiency**: Each experience transition is sampled multiple times across training steps rather than thrown away after one online update.

---

## 4. Step 2: Minibatch Updates & TD Loss

### The Loss Function
Instead of single-sample updates, DQN updates network weights $\theta$ by minimizing a Mean Squared Error (MSE) loss over a minibatch $B$ sampled from $\mathcal{D}$:

$$\mathcal{L}(\theta) = \frac{1}{|B|} \sum_{(s, a, r, s', d) \in B} \left( y_{\text{target}} - Q(s, a; \theta) \right)^2$$

where $y_{\text{target}}$ is the Temporal Difference (TD) target:

$$y_{\text{target}} = r + (1 - d) \cdot \gamma \max_{a'} Q(s', a'; \theta)$$

### Minibatch Optimization
A mini-batch update averages gradients over $|B|$ transitions (typically $|B| \in [32, 256]$):

$$\nabla_\theta \mathcal{L}(\theta) = - \frac{1}{|B|} \sum_{(s, a, r, s', d) \in B} \left[ y_{\text{target}} - Q(s, a; \theta) \right] \nabla_\theta Q(s, a; \theta)$$

Averaging over minibatches reduces variance in gradient direction, preventing isolated extreme rewards from destabilizing network weights.

---

## 5. Step 3: Target Network $\theta^-$

### The Moving Target Problem
In naive Deep Q-learning, the same weight parameters $\theta$ are used to calculate both the current prediction $Q(s, a; \theta)$ and the TD target $y = r + \gamma \max_{a'} Q(s', a'; \theta)$.

When backpropagation adjusts $\theta$ to bring $Q(s, a; \theta)$ closer to $y$, it simultaneously changes $Q(s', a'; \theta)$ for all next states. This is analogous to a dog chasing its own tail: the target moves every time the network updates, leading to oscillations or divergence.

### The Mechanism
DQN introduces a separate **Target Network** with parameters $\theta^-$. The target network is periodically cloned from the online network parameters $\theta$ every $C$ steps, and kept frozen in between:

$$y_{\text{target}}^{\text{DQN}} = r + (1 - d) \cdot \gamma \max_{a'} Q(s', a'; \theta^-)$$

```text
Online Network θ:    Updated every step via SGD on L(θ)
                          │
                          │ Clone weights every C steps
                          ▼
Target Network θ⁻:   Frozen parameters used ONLY to compute stable target y
```

Holding $\theta^-$ static for $C$ steps provides a fixed optimization objective, guaranteeing that gradient descent minimizes true function approximation error rather than chasing a non-stationary target.

---

## 6. Action Selection: $\epsilon$-Greedy Policy in DQN

Exploration remains mandatory when using function approximators. To balance exploring unvisited state-action regions and exploiting current $Q$-value estimates, DQN applies an $\epsilon$-greedy strategy over network outputs:

$$\pi(a \vert s) = \begin{cases} \text{argmax}_{a \in \mathcal{A}} Q(s, a; \theta) & \text{with probability } 1 - \epsilon \\ \text{random action from } \mathcal{A} & \text{with probability } \epsilon \end{cases}$$

### Annealing Schedule
$\epsilon$ is linearly or exponentially decayed from $1.0$ (pure exploration) down to a small baseline $\epsilon_{\text{min}} \in [0.01, 0.10]$ over $S_{\text{decay}}$ training steps:

$$\epsilon(t) = \max\left(\epsilon_{\text{min}}, \epsilon_{\text{start}} - t \cdot \frac{\epsilon_{\text{start}} - \epsilon_{\text{min}}}{S_{\text{decay}}}\right)$$

This ensures broad initial exploration when $Q$-value estimates are random, gradually transitioning to exploitation as parameters $\theta$ converge.

---

## 7. Double DQN: Mitigating Overestimation Bias

### The Overestimation Problem
Standard DQN uses the maximum estimated action value in its target calculation: $\max_{a'} Q(s', a'; \theta^-)$.

Because function approximators contain approximation noise $Q(s, a; \theta) = Q^*(s, a) + \epsilon$, taking the maximum over noisy estimates introduces a positive systematic bias:

$$\mathbb{E}\left[ \max_{a'} Q(s', a'; \theta^-) \right] \ge \max_{a'} \mathbb{E}\left[ Q(s', a'; \theta^-) \right]$$

This overestimation bias propagates back through Bellman updates, leading to severely inflated Q-values and sub-optimal policy convergence.

### The Double DQN Decoupled Solution
Double DQN (van Hasselt et al., 2016) eliminates overestimation bias by decoupling **action selection** from **action evaluation**:

1. Use the **Online Network** $\theta$ to select the best action in the next state:
   $$a^* = \arg\max_{a} Q(s', a; \theta)$$
2. Use the **Target Network** $\theta^-$ to evaluate the value of that selected action $a^*$:
   $$y_{\text{target}}^{\text{DoubleDQN}} = r + (1 - d) \cdot \gamma \, Q\left(s', \arg\max_a Q(s', a; \theta); \theta^-\right)$$

```text
Standard DQN Target:
y = r + γ * max_{a'} Q(s', a'; θ⁻)          <--- Selects AND evaluates using θ⁻ (maximization bias)

Double DQN Target:
a* = argmax_{a} Q(s', a; θ)                <--- Action selection using Online Network θ
y  = r + γ * Q(s', a*; θ⁻)                 <--- Action evaluation using Target Network θ⁻
```

This simple algorithmic change prevents noisy spikes in value estimation from dominating training updates without adding extra neural network parameters.

---

## 8. Summary of Minimal DQN Training Loop Algorithm

```text
1. Initialize Replay Buffer D with capacity N
2. Initialize Online Network Q(s, a; θ) with random weights
3. Initialize Target Network Q(s, a; θ⁻) with weights θ⁻ = θ
4. For episode = 1 to M:
5.    Reset state s
6.    For step t = 1 to T:
7.       Select action a = epsilon_greedy(s, Q(·; θ), epsilon)
8.       Execute action a, observe reward r, next_state s', done d
9.       Store transition (s, a, r, s', d) in D
10.      Sample minibatch B ~ D
11.      Compute TD targets y_i for each sample in B:
            a* = argmax_a Q(s_i', a; θ)                            [Double DQN]
            y_i = r_i + (1 - d_i) * γ * Q(s_i', a*; θ⁻)
12.      Update θ by SGD step on loss: L(θ) = 1/|B| Σ (y_i - Q(s_i, a_i; θ))^2
13.      Every C steps: update target network parameters θ⁻ ← θ
14.      s ← s'
15.      If d is True: break
```
