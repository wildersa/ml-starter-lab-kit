# Synthetic Data Lab

This lab provides a configurable mechanism for generating deterministic synthetic datasets for various Machine Learning scenarios.

## Why Synthetic Data?

Synthetic data is an excellent tool for:
- **Educational scenarios**: Learning how different algorithms respond to controlled data patterns.
- **Unit testing**: Ensuring your pipeline handles specific data shapes or distributions correctly.
- **Prototyping**: Building your project structure before real data is available.

**Important**: Synthetic data is for study and testing. It does not prove real-world performance.

## How to use

1.  Review and edit `configs/synthetic_data.json` to choose a scenario and adjust its parameters.
2.  Run the generation command:
    ```bash
    python -m {{PACKAGE_NAME}}.lab synthetic
    ```
3.  The generated artifacts will be stored in `data/synthetic/`.
4.  A summary of the generation is available in `reports/synthetic-data-summary.md`.

## Project Integration (Auto-Activation)

By default, generating synthetic data creates files in `data/synthetic/` but doesn't change your project's main training source.

To automatically point your ML pipeline to use the synthetic data, edit `configs/synthetic_data.json` and set:
```json
"activate_as_project_dataset": true
```

When this flag is `true`, running the `synthetic` command will:
1. Generate the CSV file.
2. Update `configs/config.json` to set `data.raw_path` to the new synthetic file.
3. Update `configs/config.json` to set the correct `target.column` for the chosen scenario.

## Available Scenarios

### 1. Classification
Generates a dataset with tabular features and a binary target.
- **Configurable**: Number of samples, features, informative features, and class imbalance.

### 2. Regression
Generates a dataset with tabular features and a numeric target.
- **Configurable**: Noise level and number of features.

### 3. Clustering
Generates unlabeled "customer-style" segments.
- **Configurable**: Number of clusters (centers) and features.

### 4. Time Series
Generates a date-indexed dataset with trend, seasonality, and noise.
- **Configurable**: Trend slope, seasonal period, and optional promotion/event flags.

### 5. Multi-Armed Bandit (Simple)
Generates a Bernoulli interaction history.
- **Structure**: `round`, `arm`, `reward`.
- Suitable for basic MAB experimentation.

### 6. Multi-Armed Bandit (Contextual Events)
Generates events with context (features), actions (arms), and rewards.
- **Structure**: Context columns, action column, reward column.
- **Advanced**: Supports optional `delay_steps` to simulate delayed rewards.

### 7. Bank Campaign Bandit (`bank_campaign_bandit`)
Generates a deterministic contextual Bandit event table simulating a bank marketing campaign.
- **Context**: `age`, `balance`, `job`, `segment`, `channel_preference`, `previous_contacts`.
- **Arms/Actions**: `term_deposit_email`, `term_deposit_phone`, `investment_advisor_call`, `credit_card_push`.
- **Business Outcomes**: `reward`, `conversion`, `revenue`, `delay_days`.
- **Educational Value**: Demonstrates how specific customer profiles respond differently to various channels and offers.

## Reproducibility

The Synthetic Data Lab is **deterministic**. As long as you use the same `seed` in the configuration, the generated data will be identical across different runs.

## Relation to Learning Types

- **Supervised Learning**: Use Classification or Regression to test training and evaluation loops.
- **Unsupervised Learning**: Use Clustering to test segmentation and dimensionality reduction.
- **Time Series**: Use the Time Series scenario to test forecasting models like ARIMA, Prophet, or LSTMs.
- **Adaptive Decisions (Bandits)**: Synthetic events allow you to simulate environments where decisions impact future interactions, unlike static supervised datasets.

## Learn more

- **Practical Source**: scikit-learn [Dataset Generation Documentation](https://scikit-learn.org/stable/datasets/sample_generators.html).
- **Evaluation**: scikit-learn [Model Evaluation Guide](https://scikit-learn.org/stable/modules/model_evaluation.html).

**Limitation**: Synthetic data is useful for pipeline testing and educational purposes but does not capture the complexity and noise of real-world production environments. Always validate your models with real data before deployment.
