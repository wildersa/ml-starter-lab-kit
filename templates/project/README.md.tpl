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
# Create virtual environment
python -m venv .venv

# Activate environment (Linux/macOS)
source .venv/bin/activate

# Activate environment (Windows)
.venv\\Scripts\\activate

# Install basic dependencies and the package itself in editable mode
pip install -r requirements.txt

# For development and testing
pip install -r requirements-dev.txt

# For notebooks
pip install -r requirements-notebook.txt
```

If ML or Torch support was selected (and files were generated), also install:

```bash
# Basic ML (if requirements-ml.txt exists)
pip install -r requirements-ml.txt

# PyTorch (if requirements-torch-*.txt exists)
pip install -r requirements-torch-*.txt
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

**Supervised Learning concepts:**
- **Target**: The column you want to predict. Most projects have **one** main target.
- **Features**: The columns used to make the prediction. You can have **many** feature columns. Existing CSV columns are already candidate features.

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
- `target.column`: The name of your target column.

### 3. Run the Dataset Advisor
If generated, the Advisor analyzes your data and suggests next steps:
```bash
{{ADVISOR_COMMAND}}
```
It creates `reports/dataset-advice.md` and a starting `src/{{PACKAGE_NAME}}/suggested_pipeline.py`.

### 4. Feature Engineering
Edit `src/{{PACKAGE_NAME}}/features.py` to add calculated features.

### 5. Training and Baselines
The generated `src/{{PACKAGE_NAME}}/train.py` is a **simple baseline**, not a final model. It establishes a minimum performance to beat.

## Suggested flow

1. Place the dataset in `data/raw/`
2. Adjust `configs/config.json`
3. Perform EDA in the notebook
4. Edit `src/{{PACKAGE_NAME}}/features.py`
5. Train the model (baseline)
6. Evaluate results
7. Document limitations and next steps

## Suggested commands

```bash
# Process data
python -m {{PACKAGE_NAME}}.data

# (Optional) Get advice
{{ADVISOR_COMMAND}}

# Train baseline
python -m {{PACKAGE_NAME}}.train

# Evaluate
python -m {{PACKAGE_NAME}}.evaluate
```
