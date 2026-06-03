# Ciclo básico de MLOps

Use esta visão quando o modelo precisa ser treinado, avaliado, aprovado e reutilizado.

## Fluxo simplificado

```mermaid
flowchart LR
    A[Versão dos dados] --> B[Rodada de treino]
    B --> C[Métricas]
    C --> D[Relatório de avaliação]
    D --> E[Gate de aprovação]
    E --> F[Artefato do modelo]
    F --> G[Serviço/demo]
    G --> H[Monitoramento]
    H --> I[Gatilho de retreino]
    I --> B
```

## Notas

- Rastreie dados, código, parâmetros, métricas e artefatos.
- Defina o que é bom o suficiente antes de promover um modelo.
- Tenha plano de rollback.
- Documente limitações.

Este starter kit não força uma stack completa de MLOps. Ele só oferece uma estrutura simples para evoluir.
