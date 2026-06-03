# ML Pipeline Layers

A training project can be organized in layers even when the model itself is simple.

This is not the same as neural network layers.

## Common pipeline layers

```text
raw data
  -> data validation
  -> cleaning
  -> feature engineering
  -> split strategy
  -> baseline
  -> model training
  -> evaluation
  -> model registry / artifacts
  -> inference
  -> monitoring
```

## What each layer does

| Layer | Purpose |
|---|---|
| Raw data | original files, database extracts, API exports |
| Data validation | check schema, missing values, duplicates, suspicious columns |
| Cleaning | fix types, remove invalid rows, handle missing values |
| Feature engineering | create useful model inputs |
| Split strategy | separate train/validation/test without leakage |
| Baseline | simple reference to beat |
| Training | fit the model |
| Evaluation | compare metrics and inspect errors |
| Registry/artifacts | save model and metadata |
| Inference | use the trained model |
| Monitoring | watch quality, drift, latency, and cost |

## Practical rule

Use layers to keep the project understandable. Do not create layers just to look enterprise.
