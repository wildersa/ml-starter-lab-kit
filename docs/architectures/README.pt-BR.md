# Arquiteturas de ML

Esta pasta mostra arquiteturas simplificadas de Machine Learning.

O objetivo não é ser completo. Use estes diagramas como ponto de partida para entender como projetos de ML costumam ser organizados.

## Arquitetura vs camadas do modelo

Em ML, a palavra camada pode significar duas coisas diferentes:

1. **Camadas de pipeline**: dados, validação, features, treino, avaliação, serviço e monitoramento.
2. **Camadas de rede neural**: Dense, Conv2D, LSTM, blocos de atenção etc.

A maioria dos projetos de ML pode ter camadas de pipeline. Só projetos com redes neurais têm camadas de rede neural.

## Comece por aqui

- [Camadas de pipeline ML](layers.pt-BR.md)
- [Treino tabular básico](basic-tabular-training.pt-BR.md)
- [Pipeline não supervisionado](unsupervised-pipeline.pt-BR.md)
- [Pipeline de série temporal](time-series-pipeline.pt-BR.md)
- [Pipeline de treino com imagem](image-training-pipeline.pt-BR.md)
- [Pipeline de decisão com bandit](bandit-decision-pipeline.pt-BR.md)
- [Ciclo básico de MLOps](mlops-lifecycle.pt-BR.md)
