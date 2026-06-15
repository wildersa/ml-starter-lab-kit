# Fluxos de Machine Learning

Esta pasta explica etapas comuns de projetos de Machine Learning de forma curta e prática.

Use como referência rápida, não como guia teórico profundo.

## Guias de workflow

| Guia | Use para |
|---|---|
| [Dados Sintéticos](synthetic-data.pt-BR.md) | gerar dados para testes e estudo |
| [EDA](eda.pt-BR.md) | primeiro olhar sobre o dataset |
| [Pré-processamento](preprocessing.pt-BR.md) | nulos, encoding, scaling, conversão de tipos |
| [Feature engineering](../models/feature-engineering.pt-BR.md) | criar colunas úteis de entrada |
| [Medição de features](feature-measurement.pt-BR.md) | verificar se uma feature realmente ajudou |
| [Hiperparâmetros](hyperparameters.pt-BR.md) | entender configurações de modelo/treino |
| [Otimização de hiperparâmetros](hyperparameter-optimization.pt-BR.md) | ajustar parâmetros sem complicar demais |
| [Fine-tuning](fine-tuning.pt-BR.md) | adaptar modelos pré-treinados |
| [Notebooks](notebooks.pt-BR.md) | usar notebooks sem transformar tudo em notebook |

## Seções relacionadas

- [Arquiteturas](../architectures/README.pt-BR.md)
- [Métricas](../metrics/README.pt-BR.md)
- [Checklists](../checklists/README.pt-BR.md)
- [Erros comuns](../common-mistakes/README.pt-BR.md)

## Regra prática

A maioria dos projetos compartilha o mesmo esqueleto, mas cada família de modelo muda os detalhes.

```text
dados -> pré-processamento -> features -> baseline -> treino -> avaliação
```
