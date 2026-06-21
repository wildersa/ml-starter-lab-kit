# {{PROJECT_NAME}}

This is a generated Machine Learning project, not the starter tool itself.

## Project type

`{{TASK}}`

## Structure

```text
configs/             JSON configurations
data/raw/            original data
data/processed/      processed data
notebooks/           exploration and analysis
src/{{PACKAGE_NAME}}/ main code
models/              trained models
reports/             metrics, figures and reports
tests/               minimum tests
```

## Environment and Requirements

This project uses requirements files to manage the local environment.

```bash
# Create virtual environment (POSIX)
python{{PYTHON_VERSION}} -m venv .venv

# Create virtual environment (Windows)
py -{{PYTHON_VERSION}} -m venv .venv

# Activate environment (Linux/macOS)
source .venv/bin/activate

# Activate environment (Windows)
.venv\\Scripts\\activate

# Verify Python version
python --version

# Install basic dependencies and the package itself in editable mode
pip install -r requirements.txt

# For development and testing
pip install -r requirements-dev.txt

# For notebooks
pip install -r requirements-notebook.txt
```

If ML, Torch, or MLflow support was selected (and files were generated), also install:

```bash
# Basic ML (if requirements-ml.txt exists)
pip install -r requirements-ml.txt

# PyTorch (if requirements-torch-*.txt exists)
pip install -r requirements-torch-*.txt

# MLflow Tracking (if requirements-mlflow.txt exists)
pip install -r requirements-mlflow.txt
```

> **Note on CUDA**: CUDA installations may require the correct PyTorch wheel index and local driver compatibility.
> Check at: [pytorch.org](https://pytorch.org/get-started/locally/)

### Environment validation

```bash
# Validate if the package is installed correctly
python -c "import {{PACKAGE_NAME}}; print('Package {{PACKAGE_NAME}} ready')"

# Validate PyTorch and CUDA (if installed)
python -c "import torch; print(f'Torch {torch.__version__} available. CUDA: {torch.cuda.is_available()}')"
```

## Getting Started

### 1. Prepare your data
Place your dataset at `data/raw/dataset.csv` (or the path you configured).
{% if INCLUDE_DEMO == "true" %}
**Demo Dataset**: This project includes a synthetic dataset for learning.
Check `docs/demo-scenario.md` for the scenario and data dictionary.
{% endif %}

{% if TASK != "bandit" %}
**Supervised Learning concepts:**
- **Target**: The column you want to predict. Most projects have **one** main target.
- **Features**: The columns used to make the prediction. You can have **many** feature columns. Existing CSV columns are already candidate features.
{% else %}
**Bandit Learning concepts:**
- **Reward**: The metric you want to maximize (e.g. click, conversion, success).
- **Arms**: The available choices or actions the agent can take.
{% endif %}

Example `dataset.csv`:
```csv
feature_1,feature_2,feature_3,target_column
1.2,0,red,0
2.1,1,blue,1
```

### 2. Configure the project
Review and edit `configs/config.json`:
- `data.raw_path`: Your input data path.
- `data.processed_path`: Where cleaned data goes.
- `target.column`: Your target column name.

### 3. Run the Project Guide
Validate if your dataset and configuration are ready for the pipeline:
```bash
python -m {{PACKAGE_NAME}}.lab check
```
The guide checks if the CSV exists and if the target column is correctly identified.

{% if LEARNING_ENABLED == "true" %}
## Interactive Learning Workspace (Recommended)

This project includes a visual workspace to guide you through the ML process.

```bash
python -m {{PACKAGE_NAME}}.lab workspace
```

**IMPORTANT**: You must run the **Exploratory Data Analysis (EDA)** step before the workspace can show model suggestions, baselines, or learning notes.

### Visual Flow
1. **Check**: Validate data readiness.
2. **Explore (EDA)**: Generate the dataset summary.
3. **Workspace**: Open the Streamlit app for interactive insights.
{% endif %}

{% if GENERATE_BANDIT == "true" or GENERATE_SYNTHETIC == "true" %}
## Educational Labs & Synthetic Data

{% if GENERATE_SYNTHETIC == "true" %}
- **Synthetic Data Lab**: Generate deterministic datasets to test your pipeline or study ML behavior.
  Check the **[Synthetic Data Flow Guide](docs/synthetic-data-lab.md)** to start.
{% endif %}

{% if GENERATE_BANDIT == "true" %}
- **Multi-Armed Bandit Lab**: Explore adaptive decision-making and sequential experiments.
  Check the **[Bandit Walkthrough](docs/bandit-walkthrough.md)** and the **[MAB Lab Reference](docs/mab-lab.md)**.
{% endif %}

You can explore these labs via the Visual Workspace (if enabled) or the CLI:
```bash
{% if GENERATE_SYNTHETIC == "true" %}
# Generate synthetic data
python -m {{PACKAGE_NAME}}.lab synthetic
{% endif %}
{% if GENERATE_BANDIT == "true" %}
# Run Bandit simulation
python -m {{PACKAGE_NAME}}.lab bandit
{% endif %}
```
{% endif %}

{% if LEARNING_ENABLED == "false" %}
{% if GENERATE_ADVISOR == "true" %}
### 4. Run the Dataset Advisor
If enabled, the Advisor performs a deeper heuristic analysis of your data to suggest modeling strategies:
```bash
python -m {{PACKAGE_NAME}}.lab advisor
```
It creates `reports/dataset-advice.md` and a starting `src/{{PACKAGE_NAME}}/suggested_pipeline.py`.

Note: The **Project Guide** is a readiness/validation check, while the **Dataset Advisor** provides explainable modeling suggestions.
{% endif %}

### 5. Feature Engineering
Edit `src/{{PACKAGE_NAME}}/features.py` to add calculated features.

### 6. Training and Baselines
The generated `src/{{PACKAGE_NAME}}/train.py` is a **simple baseline**, not a final model. It establishes a minimum performance to beat.
{% endif %}

## Suggested flow

1. Place the dataset in `data/raw/`
2. Adjust `configs/config.json`
3. Run `python -m {{PACKAGE_NAME}}.lab check` to validate readiness
4. **Follow the Notebook Trail**: Open `notebooks/00_start_here.ipynb` and follow the sequence (00 to 06).
5. Edit `src/{{PACKAGE_NAME}}/features.py` as you progress through the notebooks.
6. Use the CLI/Workspace for automation and interactive study.

## Suggested commands

{% if LEARNING_ENABLED == "true" %}
**Visual Workspace:**
```bash
python -m {{PACKAGE_NAME}}.lab workspace
```

**CLI Alternatives:**
{% endif %}
```bash
# Validate readiness
python -m {{PACKAGE_NAME}}.lab check

{% if GENERATE_EDA == "true" %}
# Run EDA (Generates required artifacts for Advisor/Baseline/Notes)
python -m {{PACKAGE_NAME}}.lab eda
{% endif %}

{% if GENERATE_ADVISOR == "true" %}
# (Optional) Get modeling advice
python -m {{PACKAGE_NAME}}.lab advisor
{% endif %}

{% if GENERATE_LEARNING == "true" %}
# (Optional) Generate learning notes
python -m {{PACKAGE_NAME}}.lab learn
{% endif %}

{% if GENERATE_BASELINE == "true" %}
# (Optional) Run educational baseline lab
python -m {{PACKAGE_NAME}}.lab baseline
{% endif %}

{% if GENERATE_BANDIT == "true" %}
# (Optional) Run educational Multi-Armed Bandit Lab (adaptive decisions)
python -m {{PACKAGE_NAME}}.lab bandit
{% endif %}

# Train baseline
python -m {{PACKAGE_NAME}}.lab train

# Evaluate
python -m {{PACKAGE_NAME}}.lab evaluate

{% if GENERATE_MONITOR == "true" %}
# (Optional) Run educational monitoring/drift stub
python -m {{PACKAGE_NAME}}.lab monitor
{% endif %}

# Run all steps
python -m {{PACKAGE_NAME}}.lab all
```
{% if ENABLE_MLFLOW == "true" %}
## Experiment Tracking (MLflow)

You can view your runs by starting the local server:

```bash
mlflow server --port 5000
```

Then open your browser at [http://localhost:5000](http://localhost:5000).
{% endif %}
