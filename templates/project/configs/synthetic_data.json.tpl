{
  "scenario": "classification",
  "seed": 42,
  "output_dir": "data/synthetic",
  "parameters": {
    "n_samples": 1000,
    "n_features": 10,
    "n_informative": 5,
    "n_redundant": 2,
    "weights": [0.7, 0.3]
  },
  "available_scenarios": [
    "classification",
    "regression",
    "clustering",
    "timeseries",
    "bandit_simple",
    "bandit_contextual_events"
  ],
  "scenario_examples": {
    "regression": {
      "n_samples": 1000,
      "n_features": 5,
      "noise": 0.5
    },
    "clustering": {
      "n_samples": 500,
      "n_features": 2,
      "centers": 4
    },
    "timeseries": {
      "n_periods": 365,
      "freq": "D",
      "trend_slope": 0.05,
      "seasonal_period": 7,
      "noise_std": 0.5,
      "include_promotion": true
    },
    "bandit_simple": {
      "n_rounds": 1000,
      "arms": ["A", "B", "C"],
      "probabilities": [0.02, 0.05, 0.04]
    },
    "bandit_contextual_events": {
      "n_samples": 2000,
      "n_features": 4,
      "arms": ["strategy_a", "strategy_b"],
      "include_delay": true
    }
  }
}
