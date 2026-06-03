# ML Starter Lab Kit

Gerador interativo para criar uma estrutura inicial de projeto de Machine Learning sem adicionar dependências extras no gerador.

A ideia é simples: montar uma estrutura limpa de projeto e oferecer explicações curtas sobre os fluxos mais comuns de ML.

## Uso

```bash
python create_ml_starter.py
```

## Tipos disponíveis

```text
1. generic       - estrutura genérica de ML
2. supervised    - classificação/regressão
3. unsupervised  - PCA/K-Means/clustering
4. timeseries    - séries temporais/LSTM
5. datathon      - estrutura expandida para Datathon/Fase 5
```

## Notas didáticas

Comece por aqui:

- [Visão geral dos modelos](docs/models/README.pt-BR.md)
- [Visão geral de arquiteturas](docs/architectures/README.pt-BR.md)
- [Visão geral de métricas](docs/metrics/README.pt-BR.md)
- [Checklist inicial de ML](docs/models/checklist.pt-BR.md)
- [Feature engineering](docs/models/feature-engineering.pt-BR.md)
- [Modelos supervisionados](docs/models/supervised.pt-BR.md)
- [Modelos não supervisionados](docs/models/unsupervised.pt-BR.md)
- [Séries temporais e LSTM](docs/models/time-series.pt-BR.md)
- [Modelos de imagem / Visão Computacional](docs/models/vision.pt-BR.md)
- [Reinforcement Learning](docs/models/reinforcement-learning.pt-BR.md)
- [Multi-Armed Bandits](docs/models/bandits.pt-BR.md)

## Filosofia

- Sem framework pesado por padrão.
- Sem dependências extras no gerador.
- Sem adicionar libs desnecessárias ao projeto gerado.
- Estrutura simples e editável.
- `features.py` separado para features calculadas.
- Configuração em JSON.
