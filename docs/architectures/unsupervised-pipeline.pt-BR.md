# Pipeline não supervisionado

Use quando não existe coluna target.

Exemplos:

- segmentação de clientes;
- clusterização exploratória;
- redução de dimensionalidade;
- descoberta de anomalias.

## Fluxo simplificado

```mermaid
flowchart LR
    A[Dados brutos] --> B[EDA]
    B --> C[Limpeza]
    C --> D[Escala]
    D --> E[PCA opcional]
    E --> F[Clusterização]
    F --> G[Interpretação dos clusters]
    G --> H[Relatório]
```

## Notas

- Escala costuma ser importante.
- PCA pode ajudar em visualização e redução de ruído.
- Clusters exigem interpretação.
- Um cluster não é automaticamente um segmento de negócio.

Veja:

- [modelos não supervisionados](../models/unsupervised.pt-BR.md)
- [métricas de clusterização](../metrics/clustering.pt-BR.md)
