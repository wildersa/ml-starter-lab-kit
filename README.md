# ML Starter Kit Builder

Gerador interativo para criar uma estrutura inicial de projeto de Machine Learning.

O gerador usa apenas biblioteca padrão do Python.  
Não depende de Cookiecutter, Kedro, MLflow, DVC ou qualquer framework extra.

## Uso

```bash
python create_ml_starter.py
```

## Tipos disponíveis

```text
1. generic       - estrutura genérica de ML
2. supervised    - classificação/regressão
3. unsupervised  - PCA/K-Means/clustering
4. timeseries    - séries temporais/LSTM
5. datathon      - estrutura expandida para Fase 5/Datathon
```

## Filosofia

- Sem framework pesado.
- Sem dependências extras no gerador.
- Sem adicionar libs desnecessárias ao projeto.
- Estrutura simples e editável.
- `features.py` separado para features calculadas.
- Configuração em JSON.
