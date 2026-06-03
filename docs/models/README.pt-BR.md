# Visão geral dos modelos

Esta pasta traz notas curtas e práticas sobre famílias comuns de modelos de Machine Learning.

Não é um guia teórico profundo. Use para entender por onde começar e o que cada fluxo normalmente precisa.

## Comece pela pergunta

Antes de escolher o modelo, pergunte:

1. O que quero prever, agrupar, ranquear ou otimizar?
2. Tenho uma coluna alvo?
3. A ordem temporal importa?
4. Minhas decisões afetam dados futuros?
5. Qual métrica prova que o modelo ajudou?

## Famílias de modelos

| Família | Use quando | Comece aqui |
|---|---|---|
| Supervisionado | Você tem dados de entrada e respostas conhecidas | [Modelos supervisionados](supervised.pt-BR.md) |
| Não supervisionado | Você não tem target e quer descobrir estrutura | [Modelos não supervisionados](unsupervised.pt-BR.md) |
| Séries temporais | A ordem dos eventos importa | [Séries temporais e LSTM](time-series.pt-BR.md) |
| Modelos de imagem | A entrada é imagem ou frame visual | [Modelos de imagem / Visão Computacional](vision.pt-BR.md) |
| Reinforcement Learning | Um agente aprende por ações e recompensas | [Reinforcement Learning](reinforcement-learning.pt-BR.md) |
| Bandits | Você escolhe opções e aprende com feedback | [Multi-Armed Bandits](bandits.pt-BR.md) |

## Tópicos compartilhados

- [Feature engineering](feature-engineering.pt-BR.md)
- [Medição de features](../workflows/feature-measurement.pt-BR.md)
- [Visão geral de métricas](../metrics/README.pt-BR.md)
- [Erros comuns](../common-mistakes/README.pt-BR.md)

## Esqueleto comum

A maioria dos projetos começa parecido:

```text
problema -> dados -> EDA -> limpeza -> features -> baseline -> modelo -> avaliação
```

O starter kit cria o esqueleto. O tipo de problema define os detalhes.
