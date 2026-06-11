# Evaluation and Monitoring

Evaluation and Monitoring are two sides of the same coin: one happens before the model is used (offline), and the other happens while the model is in use (online).

## Evaluation (Offline)

Evaluation happens during the development phase. It answers: "Is this model good enough to be deployed?"

- **Goal**: Compare different models or versions.
- **Data**: Static datasets (validation and test sets).
- **Key Check**: Ensure there is no [Data Leakage](../common-mistakes/data-leakage.md).

## Monitoring (Online)

Monitoring happens after the model is deployed. It answers: "Is the model still performing as expected in the real world?"

- **Goal**: Detect when the model starts to fail.
- **Data**: Real-time production data.
- **Common Issues**:
    - **Drift**: When the relationship between inputs and outputs changes over time.
    - **Latency**: How long the model takes to return a prediction.
    - **Data Integrity**: When the production data format differs from training data.

---

### Practical Rule

Never trust a model based only on its training metrics. Always use a proper [Evaluation Strategy](../metrics/README.md) and keep an eye on its [Monitoring](../architectures/layers.md).
