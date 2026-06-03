# ML Starter Lab Kit

Gerador interativo para criar uma estrutura inicial de projeto de Machine Learning sem adicionar dependências extras no gerador.

A ideia é simples: montar uma estrutura limpa de projeto e oferecer explicações curtas sobre fluxos comuns de ML sem aprofundar demais na teoria.

## Uso

```bash
python create_ml_starter.py
```

Layout recomendado:

```text
workspace/
├── ml-starter-lab-kit/      # ferramenta starter
└── meu-projeto-ml/          # projeto gerado
```

Veja [layout do starter e do projeto gerado](docs/usage/project-layout.pt-BR.md).
Veja também um [exemplo de projeto gerado](examples/generated-project-sample/).

## Tipos disponíveis

```text
1. generic       - estrutura genérica de ML
2. supervised    - classificação/regressão
3. unsupervised  - PCA/K-Means/clustering
4. timeseries    - séries temporais/LSTM
5. datathon      - estrutura expandida para Datathon/Fase 5
```

## Documentação

Comece pelo índice de documentação:

- [Índice da documentação](docs/README.pt-BR.md)
- [Trilhas de aprendizado](docs/learning-paths.pt-BR.md)
- [Visão geral de arquiteturas](docs/architectures/README.pt-BR.md)
- [Guias de workflow](docs/workflows/README.pt-BR.md)
- [Visão geral dos modelos](docs/models/README.pt-BR.md)
- [Visão geral de métricas](docs/metrics/README.pt-BR.md)
- [Checklists](docs/checklists/README.pt-BR.md)
- [Erros comuns](docs/common-mistakes/README.pt-BR.md)
- [Glossário](docs/glossary/README.pt-BR.md)
- [Changelog](CHANGELOG.md)

## Filosofia

- Suporte a perfis de ambiente (Safe/Modern).
- Requisitos opcionais para ML e PyTorch (CPU/CUDA).
- Sem framework pesado por padrão.
- Sem dependências extras no gerador.
- Sem adicionar libs desnecessárias ao projeto gerado.
- Estrutura simples e editável.
- `features.py` separado para features calculadas.
- Configuração em JSON.
