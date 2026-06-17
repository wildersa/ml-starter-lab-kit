# ML Starter Lab Kit

**Interactive scaffold for small Machine Learning projects.**

The ML Starter Lab Kit is a **project generator** that helps you jumpstart ML experiments with a professional folder structure, boilerplate code, and didactic guidance.

- **What it is**: A tool to create a clean, organized workspace for your ML code.
- **What it is not**: It is not an AutoML platform or a training library. It does not train models automatically; it provides the "skeleton" and best practices so you can focus on the Machine Learning part.

## Quick start

1. **Clone** this repository:

   ```bash
   git clone https://github.com/wildersa/ml-starter-lab-kit.git
   cd ml-starter-lab-kit
   ```

2. **Generate** your project:

   ```bash
   python create_ml_starter.py
   ```

3. **Go** to your generated project folder (it is created as a sibling to this tool):

   ```bash
   cd ../your-project-name
   ```

4. **Initialize**: Create a virtual environment and install requirements:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

5. **Start**: Place your data in `data/raw/` and follow the generated `README.md`.

Recommended layout:

```text
workspace/
├── ml-starter-lab-kit/      # this tool
└── my-ml-project/           # your generated project
```

See [starter and generated project layout](docs/usage/project-layout.md) and a [generated project sample](examples/generated-project-sample/).

## Available project types

- **generic**: Standard ML project structure.
- **supervised**: For classification and regression tasks.
- **unsupervised**: For clustering and dimensionality reduction.
- **timeseries**: For forecasting and sequence analysis.
- **vision**: For image classification and detection.
- **bandit**: For Multi-Armed Bandits and adaptive decisions (exploration-exploitation).

## Key Features

- **Synthetic Data Lab**: Generate deterministic datasets (Classification, Regression, MAB, etc.) to test pipelines or study ML behavior without real data.
- **Interactive Workspace**: A guided visual environment (using Streamlit) for EDA, training baselines, and model evaluation.

## Documentation

Start with the [Documentation Index](docs/README.md) to explore:

- [Learning paths](docs/learning-paths.md)
- [Workflow guides](docs/workflows/README.md)
- [Architecture overview](docs/architectures/README.md)
- [Common mistakes](docs/common-mistakes/README.md)
- [Glossary](docs/glossary/README.md)

Portuguese quick reference: [README.pt-BR.md](README.pt-BR.md)

## Philosophy

- **Zero generator dependencies**: Uses only the Python standard library.
- **Simple & Editable**: No heavy frameworks; the generated code is yours to change.
- **Profile-based**: Support for 'Safe' (3.12) or 'Modern' (3.14) Python environments.
- **Optional stack**: Easily add PyTorch (CPU/CUDA) or standard ML libs (pandas, scikit-learn).
- **Clean organization**: Dedicated `features.py` and JSON-based configuration.
