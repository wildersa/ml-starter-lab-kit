# Modelos supervisionados

Use aprendizado supervisionado quando você tem exemplos com respostas conhecidas.

```text
features -> target
```

Exemplos:

- prever se um cliente vai converter;
- prever preço de casa;
- classificar fraude;
- prever churn.

## Tipos principais

| Tipo | Target | Métrica exemplo |
|---|---|---|
| Classificação | categoria/classe | accuracy, F1, AUC |
| Regressão | número | MAE, RMSE, R² |

## Fluxo típico

```text
dados -> EDA -> split -> pré-processamento -> baseline -> modelo -> avaliação
```

## Modelos comuns

- Regressão Logística
- Árvore de Decisão
- Random Forest
- XGBoost/LightGBM/CatBoost
- Redes neurais, quando justificar

## Conselho prático

Comece com um baseline simples antes de usar um modelo forte.

Para dados tabulares, modelos baseados em árvores costumam ser uma ótima primeira opção séria.

## Erros comuns

- Usar dados do futuro como features.
- Avaliar só nos dados de treino.
- Ignorar desbalanceamento de classes.
- Usar accuracy quando F1/AUC faria mais sentido.
