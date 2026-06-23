# Project Map

This map helps you navigate the generated ML project structure.

## Key Directories and Files

- `configs/`: Contains `config.json` with project-wide settings and optional `bandit_config.json` or `synthetic_data.json`.
- `data/`:
    - `raw/`: The entry point for datasets.
    - `processed/`: Where cleaned and transformed data should be stored.
- `docs/`:
    - `demo-scenario.md`: The business context for the project.
    - `data-dictionary.md`: Definitions of the dataset columns.
    - `learning-path.md`: Task-specific didactic guidance.
- `notebooks/`: A numbered sequence of Jupyter notebooks (00 to 06) for a step-by-step workflow.
- `src/{{PACKAGE_NAME}}/`:
    - `core/`: Fundamental logic for data loading, config, and readiness checks.
    - `data.py`, `features.py`, `train.py`, `evaluate.py`: Standard ML pipeline modules.
    - `lab.py`: CLI entry point for various lab tools.
- `reports/`:
    - `experiment-notes.md`: A template for logging your experimental results.
    - `figures/`: Where plots and charts should be saved.
- `START_HERE.md`: The primary onboarding guide for the user.
- `AGENTS.md`: Guidance for AI agents working in this repository.
