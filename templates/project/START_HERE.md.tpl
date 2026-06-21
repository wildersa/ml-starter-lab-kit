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

### Step 2: Follow the Learning Trail (Notebooks) — **RECOMMENDED**
The best way to learn is by following the sequential notebook trail.
- **Start here**: Open `notebooks/00_start_here.ipynb`
- **Sequence**: 00 (Start) → 01 (Understanding) → 02 (EDA) → 03 (Features) → 04 (Baseline) → 05 (Evaluation) → 06 (Notes).

> **Note**: These notebooks import code from `src/{{PACKAGE_NAME}}`, allowing you to see how the reusable modules work behind the scenes.

{% if LEARNING_ENABLED == "true" %}
### Step 3: Interactive Learning Workspace
If you are in Guided Mode, open the visual workspace:
```bash
python -m {{PACKAGE_NAME}}.lab workspace
```
{% endif %}

### Step 4: Modeling Advice & Baselines
{% if GENERATE_ADVISOR == "true" %}
- **Advisor**: `python -m {{PACKAGE_NAME}}.lab advisor` (Modeling suggestions)
{% endif %}
- **Train Baseline**: `python -m {{PACKAGE_NAME}}.lab train`
- **Evaluate**: `python -m {{PACKAGE_NAME}}.lab evaluate`

---

## 4. Project Structure & Key Files

- `data/raw/`: Place your dataset here (Default: `{{DATASET_PATH}}`).
- `configs/config.json`: Main project configuration (Target column, paths).
- `src/{{PACKAGE_NAME}}/features.py`: Define your feature engineering logic here.
- `notebooks/`: Your learning path, from data understanding to model evaluation.

## 5. Notebooks vs. Python Pipeline

- **Use Notebooks (`notebooks/`)**: For exploration, visualization, and iterative learning.
- **Use Python Pipeline (`src/`)**: For repeatable execution, version control, and production-ready code.

{% if GENERATE_DOCS == "true" %}
## 6. Documentation

Check the `docs/` folder for detailed guides:
- [Learning Path](docs/learning-path.md)
- [Data Dictionary](docs/data-dictionary.md)
- [Evaluation Guide](docs/evaluation.md)
{% if INCLUDE_DEMO == "true" %}
- [Demo Scenario](docs/demo-scenario.md)
{% endif %}
{% if GENERATE_BANDIT == "true" %}
- [Bandit Lab Guide](docs/mab-lab.md)
{% endif %}
{% if GENERATE_SYNTHETIC == "true" %}
- [Synthetic Data Guide](docs/synthetic-data-lab.md)
{% endif %}
{% if GENERATE_MONITOR == "true" %}
- [Monitoring Guide](docs/monitoring.md)
{% endif %}
{% endif %}
