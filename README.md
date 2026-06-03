# ML Starter Lab Kit

Interactive starter kit for small Machine Learning projects, with no extra dependencies in the generator.

The goal is simple: create a clean project structure and provide short, practical explanations for common ML workflows.

## Usage

```bash
python create_ml_starter.py
```

## Available project types

```text
1. generic       - generic ML project structure
2. supervised    - classification/regression
3. unsupervised  - PCA/K-Means/clustering
4. timeseries    - time series/LSTM
5. datathon      - expanded structure for Datathon/Fase 5
```

## Learning notes

Start here:

- [Model overview](docs/models/README.md)
- [Initial ML checklist](docs/models/checklist.md)
- [Feature engineering](docs/models/feature-engineering.md)
- [Supervised learning](docs/models/supervised.md)
- [Unsupervised learning](docs/models/unsupervised.md)
- [Time series and LSTM](docs/models/time-series.md)
- [Reinforcement Learning](docs/models/reinforcement-learning.md)
- [Multi-Armed Bandits](docs/models/bandits.md)

Portuguese quick reference: [README.pt-BR.md](README.pt-BR.md)

## Philosophy

- No heavy framework by default.
- No extra dependencies in the generator.
- No unnecessary libraries added to the generated project.
- Simple and editable structure.
- Dedicated `features.py` for calculated features.
- JSON-based configuration.
