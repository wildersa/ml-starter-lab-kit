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

## Quick Start & Core Concepts

### 1. Data placement
Place your dataset in `data/raw/`.
By default, the project expects the file at: `{{DATASET_PATH}}`.

### 2. Configuration
Review `configs/config.json`. Key fields to check:
- `data.raw_path`: Path to your raw CSV file.
- `data.processed_path`: Where the processed table will be saved (usually `data/processed/modeling_table.csv`).
- `target.column`: The name of the column you want to predict.

### 3. Target vs Features
In supervised learning, you usually have:
- **Target**: The single column you want to predict (e.g., `is_spam`).
- **Features**: The many columns used to make that prediction (e.g., `sender`, `subject_length`, `has_attachments`). The existing columns in your CSV are already candidate features.

**Example CSV:**
```csv
age,city,income,bought_product
25,NY,50000,1
30,SF,80000,0
```
- **Target**: `bought_product`
- **Features**: `age`, `city`, `income`

### 4. Feature Engineering (`features.py`)
Use `src/{{PACKAGE_NAME}}/features.py` to create *new* calculated features from your raw data (like calculating a ratio between two columns or extracting the month from a date).

### 5. Training a Baseline (`train.py`)
Running `python -m {{PACKAGE_NAME}}.train` trains a **baseline model**.
A baseline is a simple, naive model (like always predicting the most frequent category) used as a starting benchmark. It is **not** a final production model, but a reference point that your future, more complex models should try to beat.
{{ADVISOR_QUICKSTART}}
## Suggested flow

```text
1. Place the dataset in data/raw/
2. Adjust configs/config.json
3. Perform EDA in the notebook
4. Edit src/{{PACKAGE_NAME}}/features.py
5. Train the model
6. Evaluate results
7. Document limitations and next steps
```

## Suggested commands

```bash
python -m {{PACKAGE_NAME}}.data
{{ADVISOR_COMMAND}}
python -m {{PACKAGE_NAME}}.train
python -m {{PACKAGE_NAME}}.evaluate
```
