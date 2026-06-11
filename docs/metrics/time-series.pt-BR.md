# Métricas de Séries Temporais

A avaliação de séries temporais exige um foco especial na ordem temporal dos dados. Você deve avaliar como o modelo se comporta em dados "futuros" em relação ao que ele viu durante o treinamento.

## Métricas Recomendadas

As séries temporais geralmente usam as mesmas métricas da regressão (MAE, RMSE, MAPE), mas com uma estratégia de avaliação diferente.

- **MAE**: Melhor para precisão geral nas mesmas unidades.
- **RMSE**: Melhor quando grandes erros de previsão são catastróficos.
- **sMAPE (MAPE Simétrico)**: Uma variação do MAPE que é mais robusta quando os valores reais são pequenos ou zero.

## Estratégia de Avaliação: Backtesting

- **O que responde**: Se eu tivesse usado este modelo no passado, qual teria sido o seu desempenho?
- **Quando usar**: Sempre para séries temporais. Em vez de divisões aleatórias, use uma **Janela Deslizante (Sliding Window)** ou **Janela em Expansão (Expanding Window)**.
- **Armadilha comum**: Avaliar em linhas aleatórias (shuffling) causa "Vazamento Temporal" (Temporal Leakage), onde o modelo vê o futuro para prever o passado, levando a um desempenho irrealista.

## Horizonte de Previsão e Janela

- **Horizonte (Horizon)**: Quão longe no futuro você está prevendo? (ex: prever os próximos 7 dias). As métricas geralmente pioram à medida que o horizonte aumenta.
- **Janela (Window)**: A quantidade de dados passados usados para fazer uma previsão (ex: usar os últimos 30 dias para prever o próximo dia).

---

### Próximos Passos

Sempre verifique o [Checklist Antes da Avaliação](../checklists/before-evaluation.pt-BR.md) para garantir que sua divisão temporal esteja correta e que você não esteja "vazando" informações do futuro para o passado.
- Veja o conceito de [Avaliação e Monitoramento](../concepts/evaluation-and-monitoring.pt-BR.md) para o ciclo completo.
