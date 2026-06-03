# Basic MLOps Lifecycle

Use this view when the model needs to be trained, evaluated, approved, and reused.

## Simplified flow

```mermaid
flowchart LR
    A[Data version] --> B[Training run]
    B --> C[Metrics]
    C --> D[Evaluation report]
    D --> E[Approval gate]
    E --> F[Model artifact]
    F --> G[Serving/demo]
    G --> H[Monitoring]
    H --> I[Retraining trigger]
    I --> B
```

## Notes

- Keep track of data, code, parameters, metrics, and artifacts.
- Define what is good enough before promoting a model.
- Have a rollback plan.
- Document limitations.

This starter kit does not enforce a full MLOps stack. It only gives a simple structure to grow from.
