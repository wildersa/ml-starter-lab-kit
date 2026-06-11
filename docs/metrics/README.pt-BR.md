# Visão Geral de Métricas

As métricas dizem se o modelo é útil para o problema.

Não escolha uma métrica apenas porque ela é popular. Escolha-a porque ela corresponde à decisão que você precisa tomar.

## Mapa rápido

| Problema | Métricas Principais |
|---|---|
| **[Classificação](classification.pt-BR.md)** | Matriz de Confusão, Acurácia, Precisão, Recall, F1, AUC, Thresholds |
| **[Regressão](regression.pt-BR.md)** | MAE, RMSE, MAPE, R² |
| **[Séries Temporais](time-series.pt-BR.md)** | MAE, RMSE, MAPE, Backtesting, Avaliação por Horizonte |
| **[Agrupamento (Clustering)](clustering.pt-BR.md)** | Inércia, Silhouette Score, Interpretação Qualitativa |
| **[Visão Computacional](vision.pt-BR.md)** | mAP, IoU, Dice Score, Métricas de Classificação de Imagem |
| **[Bandits](bandits.pt-BR.md)** | Recompensa, Recompensa Acumulada, Regret, Lift, Drift de Usuário |

## Princípios Fundamentais

Para um mergulho profundo nos conceitos fundamentais de como medir o sucesso de ML, consulte o guia de **[Avaliação e Monitoramento](../concepts/evaluation-and-monitoring.md)**.

### Guias relacionados

- [Erro de métrica (Metric mismatch)](../common-mistakes/metric-mismatch.md)
- [Medição de features](../workflows/feature-measurement.md)
- [Checklist antes da avaliação](../checklists/before-evaluation.md)

### Regra prática

Uma boa métrica deve responder:
> **"O modelo melhorou a decisão com a qual eu me importo?"**
