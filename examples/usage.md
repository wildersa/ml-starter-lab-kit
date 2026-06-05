# Usage examples

## Interactive mode

```bash
python create_ml_starter.py
```

## Phase 3

Choose:

```text
task: supervised
package: tech_challenge_phase3
target: your_target_column
```

Then, if needed, add to your project:

```text
pandas
scikit-learn
xgboost
```

## Phase 4

Choose:

```text
task: timeseries
package: tech_challenge_phase4
```

Then add Keras/TensorFlow only if you are going to use LSTM.

## Phase 5 / Datathon

Choose:

```text
task: supervised (or other real ML type)
preset: datathon
package: datathon_offerexp
```

It also creates:

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
