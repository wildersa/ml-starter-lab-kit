# Arquiteturas de ML

Esta pasta mostra arquiteturas simplificadas de Machine Learning.

O objetivo não é ser completo. Use estes diagramas como ponto de partida para entender como projetos de ML costumam ser organizados.

## Arquitetura vs camadas do modelo

Em ML, a palavra camada pode significar duas coisas diferentes:

1. **Camadas de pipeline**: dados, validação, features, treino, avaliação, serviço e monitoramento.
2. **Camadas de rede neural**: Dense, Conv2D, LSTM, blocos de atenção etc.

A maioria dos projetos de ML pode ter camadas de pipeline. Só projetos com redes neurais têm camadas de rede neural.

## Guias de arquitetura

| Guia | Use para |
|---|---|
| [Camadas de pipeline ML](layers.pt-BR.md) | entender camadas comuns de projetos ML |
| [Treino tabular básico](basic-tabular-training.pt-BR.md) | projetos tabulares supervisionados |
| [Pipeline não supervisionado](unsupervised-pipeline.pt-BR.md) | projetos com PCA/K-Means/clusterização |
| [Pipeline de série temporal](time-series-pipeline.pt-BR.md) | previsão e projetos temporais |
| [Pipeline de treino com imagem](image-training-pipeline.pt-BR.md) | modelos de imagem e fine-tuning |
| [Pipeline de decisão com bandit](bandit-decision-pipeline.pt-BR.md) | sistemas de decisão adaptativa |
| [Ciclo básico de MLOps](mlops-lifecycle.pt-BR.md) | treino, aprovação, serviço, monitoramento |

## Seções relacionadas

- [Workflows](../workflows/README.pt-BR.md)
- [Visão geral dos modelos](../models/README.pt-BR.md)
- [Visão geral de métricas](../metrics/README.pt-BR.md)
