{
  "lab": "multi_armed_bandit",
  "status": "active",
  "description": "Educational Bernoulli Multi-Armed Bandit simulation config.",
  "n_rounds": 1000,
  "seed": 42,
  "reward_model": "bernoulli",
  "arms": [
    {
      "name": "A",
      "true_reward_probability": 0.03
    },
    {
      "name": "B",
      "true_reward_probability": 0.05
    },
    {
      "name": "C",
      "true_reward_probability": 0.08
    }
  ],
  "policies": [
    "random",
    "epsilon_greedy",
    "ucb1",
    "thompson_sampling"
  ],
  "epsilon": 0.1,
  "expected_outputs": [
    "configs/bandit_results.json",
    "reports/bandit-results.md",
    "reports/bandit-history.csv"
  ]
}
