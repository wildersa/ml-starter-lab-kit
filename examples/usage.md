# Exemplos de uso

## Modo interativo

```bash
python create_ml_starter.py
```

## Fase 3

Escolha:

```text
task: supervised
package: tech_challenge_fase3
target: sua_coluna_target
```

Depois, se precisar, adicione no seu projeto:

```text
pandas
scikit-learn
xgboost
```

## Fase 4

Escolha:

```text
task: timeseries
package: tech_challenge_fase4
```

Depois adicione Keras/TensorFlow somente se for usar LSTM.

## Fase 5 / Datathon

Escolha:

```text
task: supervised (ou outro tipo real de ML)
preset: datathon
package: datathon_offerexp
```

Ele cria também:

```text
docs/architecture-azure.md
docs/model-card.md
docs/system-card.md
docs/lgpd-plan.md
docs/algorithmic-strategy.md
data/synthetic_enrichment/
data/golden_set/
infra/azure/
```
