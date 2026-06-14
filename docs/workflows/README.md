# ML Workflows

This folder explains common Machine Learning workflow steps in a short and practical way.

Use it as a quick reference, not as a deep theory guide.

## Workflow guides

| Guide | Use for |
|---|---|
| [Synthetic Data](synthetic-data.md) | generating data for testing and study |
| [EDA](eda.md) | first look at the dataset |
| [Preprocessing](preprocessing.md) | missing values, encoding, scaling, type conversion |
| [Feature engineering](../models/feature-engineering.md) | creating useful input columns |
| [Feature measurement](feature-measurement.md) | checking if a feature actually helped |
| [Hyperparameters](hyperparameters.md) | understanding model/training settings |
| [Hyperparameter optimization](hyperparameter-optimization.md) | tuning without overcomplicating |
| [Fine-tuning](fine-tuning.md) | adapting pretrained models |
| [Notebooks](notebooks.md) | using notebooks without making them the whole project |

## Related sections

- [Architectures](../architectures/README.md)
- [Metrics](../metrics/README.md)
- [Checklists](../checklists/README.md)
- [Common mistakes](../common-mistakes/README.md)

## Practical rule

Most projects share the same skeleton, but each model family changes the details.

```text
data -> preprocessing -> features -> baseline -> training -> evaluation
```
