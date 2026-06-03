# Notebooks

Use notebooks for exploration, not as the only production code.

## Good notebook use

- EDA;
- quick charts;
- first baseline;
- explaining results;
- documenting decisions.

## Move reusable logic to Python modules

If a cell becomes important, move it to:

```text
src/<package>/data.py
src/<package>/features.py
src/<package>/train.py
src/<package>/evaluate.py
```

## Practical rule

Notebook explains the journey. Python modules keep the reusable logic.
