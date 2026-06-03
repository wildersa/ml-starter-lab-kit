# Notebooks

Use notebooks para exploração, não como único código do projeto.

## Bons usos de notebook

- EDA;
- gráficos rápidos;
- primeiro baseline;
- explicar resultados;
- documentar decisões.

## Mova lógica reutilizável para módulos Python

Se uma célula ficou importante, mova para:

```text
src/<package>/data.py
src/<package>/features.py
src/<package>/train.py
src/<package>/evaluate.py
```

## Regra prática

Notebook explica a jornada. Módulos Python guardam a lógica reutilizável.
