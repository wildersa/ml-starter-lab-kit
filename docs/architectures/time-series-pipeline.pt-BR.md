# Pipeline de série temporal

Use quando a ordem dos eventos importa.

Exemplos:

- previsão de vendas;
- previsão de demanda;
- previsão de tráfego;
- detecção de anomalia temporal.

## Fluxo simplificado

```mermaid
flowchart LR
    A[Dados históricos] --> B[Validação temporal]
    B --> C[Features temporais]
    C --> D[Split cronológico]
    D --> E[Baseline ingênuo]
    D --> F[Treino do modelo]
    E --> G[Avaliação da previsão]
    F --> G
    G --> H[Artefato de previsão]
```

## Notas

- Não use split aleatório por padrão.
- Lags e médias móveis devem evitar vazamento do futuro.
- Compare com baselines simples antes de LSTM.

Veja:

- [séries temporais e LSTM](../models/time-series.pt-BR.md)
- [métricas de séries temporais](../metrics/time-series.pt-BR.md)
