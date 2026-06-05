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
