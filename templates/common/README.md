# Common Generated Modules

The generator can evolve to create optional support modules.

Suggested modules:

| Module | Purpose | Dependency policy |
|---|---|---|
| `eda.py` | dataset summary helpers | standard library first |
| `preprocessing.py` | missing values, encoding, scaling, type conversion | standard library first |
| `visualization.py` | chart placeholders/helpers | add matplotlib only if needed |
| `metrics.py` | simple metric wrappers and references | standard library first |
| `optimization.py` | simple grid/random search structure | no optimization library by default |
| `notebook_factory.py` | create starter notebooks | standard library |

The rule is simple: generate structure first, add libraries only when the project actually needs them.

## Why `preprocessing.py` instead of `scaler.py`?

Scaling is not needed by every model, and it is only one preprocessing step.

A broader `preprocessing.py` module can hold scaling, encoding, missing-value handling, and type conversion.

## Why `optimization.py`?

Hyperparameters exist in most ML projects, but they change by model family.

A small `optimization.py` module can provide structure for manual search, grid search, or random search without forcing a heavy optimization framework.
