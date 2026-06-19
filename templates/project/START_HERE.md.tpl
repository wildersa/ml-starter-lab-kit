# Welcome to {{PROJECT_NAME}}!

This guide will help you navigate your new Machine Learning project.

## 1. Project Overview

- **Project Name**: {{PROJECT_NAME}}
- **ML Task**: {{TASK}}
- **Package Name**: `{{PACKAGE_NAME}}`
- **Python Version**: {{PYTHON_VERSION}}

## 2. Quick Environment Setup

Open your terminal in this folder and run:

```bash
# 1. Create virtual environment
{% if PYTHON_VERSION == "3.12" %}
py -3.12 -m venv .venv           # Windows
python3.12 -m venv .venv         # POSIX
{% else %}
py -{{PYTHON_VERSION}} -m venv .venv
python{{PYTHON_VERSION}} -m venv .venv
{% endif %}

# 2. Activate environment
.venv\Scripts\activate           # Windows
source .venv/bin/activate        # POSIX

# 3. Install dependencies and the project
pip install -r requirements.txt
pip install -e .
```

## 3. Recommended Learning Path

Follow these steps in order to get the best experience:

### Step 1: Data Readiness Check
Validate if your dataset and configuration are ready:
```bash
python -m {{PACKAGE_NAME}}.lab check
```

### Step 2: Exploratory Data Analysis (EDA) — **DO NOT SKIP**
Before training any model, you must understand your data.
- **Notebook (Recommended for beginners)**: Open `notebooks/01_eda.ipynb`
- **CLI Alternative**: `python -m {{PACKAGE_NAME}}.lab eda`

> **Note**: EDA generates artifacts required for the Advisor and Learning Workspace.

### Step 3: Interactive Learning Workspace
If you are in Guided Mode, open the visual workspace:
```bash
python -m {{PACKAGE_NAME}}.lab workspace
```

### Step 4: Modeling Advice & Baselines
- **Advisor**: `python -m {{PACKAGE_NAME}}.lab advisor` (Modeling suggestions)
- **Train Baseline**: `python -m {{PACKAGE_NAME}}.lab train`
- **Evaluate**: `python -m {{PACKAGE_NAME}}.lab evaluate`

---

## 4. Project Structure & Key Files

- `data/raw/`: Place your dataset here (Default: `{{DATASET_PATH}}`).
- `configs/config.json`: Main project configuration (Target column, paths).
- `src/{{PACKAGE_NAME}}/features.py`: Define your feature engineering logic here.
- `notebooks/01_eda.ipynb`: Your starting point for data exploration.

## 5. Notebooks vs. Python Pipeline

- **Use Notebooks (`notebooks/`)**: For exploration, visualization, and iterative learning.
- **Use Python Pipeline (`src/`)**: For repeatable execution, version control, and production-ready code.

## 6. Documentation

Check the `docs/` folder for detailed guides:
- [Data Dictionary](docs/data-dictionary.md)
{% if INCLUDE_DEMO == "true" %}
- [Demo Scenario](docs/demo-scenario.md)
{% endif %}
- [Learning Path](docs/learning-path.md)
{% if GENERATE_BANDIT == "true" %}
- [Bandit Lab Guide](docs/mab-lab.md)
{% endif %}
{% if GENERATE_SYNTHETIC == "true" %}
- [Synthetic Data Guide](docs/synthetic-data-lab.md)
{% endif %}
