# Synthetic Data Flow

The Synthetic Data Lab allows you to generate controlled, deterministic datasets to test your pipeline or study specific ML scenarios before using real data.

## Workflow steps

1.  **Configure**: Edit `configs/synthetic_data.json` to select a scenario (classification, regression, time-series, etc.) and its parameters.
2.  **Generate**: Run the synthetic command:
    ```bash
    python -m <package>.lab synthetic
    ```
3.  **Inspect**: Check `data/synthetic/` for the CSV and metadata, and review `reports/synthetic-data-summary.md`.
4.  **Connect**:
    - **Automatic**: If `activate_as_project_dataset` is `true` in the config, the project's main `configs/config.json` is updated automatically.
    - **Manual**: Update `data.raw_path` and `target.column` in `configs/config.json` using the values suggested in the terminal output.

## Integration with the Pipeline

Once activated, the synthetic data flows through the standard commands:

```bash
python -m <package>.lab data      # Prepares the synthetic raw data
python -m <package>.lab train     # Trains on the synthetic data
python -m <package>.lab evaluate  # Evaluates performance
```

## When to use it

- **Pipeline testing**: Ensure `data.py` and `train.py` handle the expected data shape.
- **Learning**: Experiment with how imbalanced data (Classification) or noise (Regression) affects metrics.
- **MAB Exploration**: Use Bandit scenarios to understand exploration/exploitation without real-world risk.

## Comparison: Bandit Lab vs. Synthetic Data Lab

It is important to distinguish between these two educational tools:

| Feature | Synthetic Data Lab | Multi-Armed Bandit Lab |
|---|---|---|
| **Nature** | **Logged/Static Data**: Generates a CSV file of past events (e.g., `bank_campaign_bandit`). | **Active Simulation**: An interactive environment where an agent makes decisions and gets feedback. |
| **Feedback Loop** | Fixed. You train models on logs of what already happened. | Dynamic. The agent's choice in round *N* can be evaluated immediately. |
| **Primary Use** | Testing the `data.py` and `train.py` pipeline with Bandit-formatted logs. | Learning about exploration/exploitation strategies (Epsilon-Greedy, Thompson Sampling). |
| **Artifact** | `data/synthetic/scenario.csv` | Markdown tables and plots in the Workspace. |

The **`bank_campaign_bandit`** scenario in the Synthetic Data Lab acts as a bridge: it provides the realistic columns you would see in a real-world Bandit log, which you can then use to "warm up" or test your policies before running a full simulation.

**Note**: Synthetic data is for testing and education. It does not reflect real-world performance.
