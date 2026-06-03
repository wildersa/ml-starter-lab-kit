# ML Starter Lab Kit

Interactive starter kit for small Machine Learning projects, with no extra dependencies in the generator.

The goal is simple: create a clean project structure and provide short, practical explanations for common ML workflows without going deep into theory.

## Usage

```bash
python create_ml_starter.py
```

Recommended layout:

```text
workspace/
├── ml-starter-lab-kit/      # starter tool
└── my-ml-project/           # generated project
```

See [starter and generated project layout](docs/usage/project-layout.md).

## Available project types

```text
1. generic       - generic ML project structure
2. supervised    - classification/regression
3. unsupervised  - PCA/K-Means/clustering
4. timeseries    - time series/LSTM
5. datathon      - expanded structure for Datathon/Fase 5
```

## Documentation

Start with the documentation hub:

- [Documentation index](docs/README.md)
- [Learning paths](docs/learning-paths.md)
- [Architecture overview](docs/architectures/README.md)
- [Workflow guides](docs/workflows/README.md)
- [Model overview](docs/models/README.md)
- [Metrics overview](docs/metrics/README.md)
- [Checklists](docs/checklists/README.md)
- [Common mistakes](docs/common-mistakes/README.md)
- [Glossary](docs/glossary/README.md)

Portuguese quick reference: [README.pt-BR.md](README.pt-BR.md)

## Philosophy

- No heavy framework by default.
- No extra dependencies in the generator.
- No unnecessary libraries added to the generated project.
- Simple and editable structure.
- Dedicated `features.py` for calculated features.
- JSON-based configuration.
