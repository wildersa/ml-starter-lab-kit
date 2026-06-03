# Visão geral de métricas

Métricas mostram se o modelo é útil para o problema.

Não escolha uma métrica só porque ela é popular. Escolha porque ela combina com a decisão.

## Mapa rápido

| Problema | Comece com |
|---|---|
| Classificação | [Accuracy, F1, AUC](classification.pt-BR.md) |
| Regressão | [MAE, RMSE, R²](regression.pt-BR.md) |
| Clusterização | [Silhouette, inércia](clustering.pt-BR.md) |
| Série temporal | [MAE, RMSE, MAPE](time-series.pt-BR.md) |
| Bandits | [Reward, regret](bandits.pt-BR.md) |
| Visão | [F1, mAP, IoU, Dice](vision.pt-BR.md) |

## Guias relacionados

- [Métrica incompatível](../common-mistakes/metric-mismatch.pt-BR.md)
- [Medição de features](../workflows/feature-measurement.pt-BR.md)
- [Checklist antes da avaliação](../checklists/before-evaluation.pt-BR.md)

## Regra prática

Uma boa métrica deve responder:

```text
O modelo melhorou a decisão que importa?
```
