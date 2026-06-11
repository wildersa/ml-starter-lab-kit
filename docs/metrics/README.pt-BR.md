# Visão Geral de Métricas

As métricas dizem se o modelo é útil para o problema.

Não escolha uma métrica apenas porque ela é popular. Escolha-a porque ela corresponde à **decisão** que você precisa tomar e ao **custo de estar errado**.

## Mapa rápido

| Problema | Métricas Recomendadas |
|---|---|
| Classificação | [Acurácia, Precisão, Recall, F1, AUC](classification.pt-BR.md) |
| Regressão | [MAE, RMSE, R², MAPE](regression.pt-BR.md) |
| Agrupamento | [Silhueta, Inércia, Interpretação](clustering.pt-BR.md) |
| Séries Temporais | [MAE, RMSE, sMAPE, Backtesting](time-series.pt-BR.md) |
| Bandits | [Recompensa, Regret, Lift, Exploração](bandits.pt-BR.md) |
| Visão | [mAP, IoU, Dice, F1](vision.pt-BR.md) |

## Guias relacionados

- [Métrica incompatível (Metric mismatch)](../common-mistakes/metric-mismatch.pt-BR.md)
- [Medição de impacto de features](../workflows/feature-measurement.pt-BR.md)
- [Checklist antes da avaliação](../checklists/before-evaluation.pt-BR.md)

## Regra prática

Uma boa métrica deve responder:

> "O modelo melhorou a decisão com a qual eu me preocupo?"

Se sua métrica melhora, mas o resultado do seu negócio não, você está medindo a coisa errada.
- Veja o conceito de [Avaliação e Monitoramento](../concepts/evaluation-and-monitoring.pt-BR.md) para o ciclo completo.
