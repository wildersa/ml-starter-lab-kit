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

## Famílias comuns

| Família | Use quando | Exemplos |
|---|---|---|
| Supervisionado | Você tem dados de entrada e respostas conhecidas | XGBoost, Random Forest, Regressão Logística |
| Não supervisionado | Você não tem target e quer descobrir estrutura | K-Means, PCA, clustering |
| Séries temporais | A ordem dos eventos importa | ARIMA, Prophet, LSTM, features temporais |
| Reinforcement Learning | Um agente aprende por ações e recompensas | Q-learning, policy gradients |
| Bandits | Você escolhe opções e aprende com feedback | Thompson Sampling, UCB, LinUCB |

## Esqueleto comum

A maioria dos projetos começa parecido:

```text
problema -> dados -> EDA -> limpeza -> features -> baseline -> modelo -> avaliação
```

O starter kit cria o esqueleto. O tipo de problema define os detalhes.
