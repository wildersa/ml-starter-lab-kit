# Pré-processamento

Pré-processamento prepara os dados brutos antes da engenharia de features e do treino.

Não é a mesma coisa que feature engineering. Pré-processamento normalmente corrige os dados. Feature engineering cria novos sinais úteis.

## Etapas comuns de pré-processamento

| Etapa | Objetivo |
|---|---|
| Conversão de tipos | converter datas, números, booleanos |
| Valores ausentes | preencher, sinalizar ou remover nulos |
| Encoding | converter categorias para representação numérica |
| Scaling | colocar valores numéricos em escalas comparáveis |
| Deduplicação | remover linhas repetidas quando fizer sentido |
| Remoção de vazamento | remover colunas indisponíveis no momento da previsão |

## Todo modelo precisa de scaling?

Não.

Scaling é importante para modelos que dependem de distância, variância, gradientes ou otimização numérica.

## Scaling costuma importar para

- K-Means;
- PCA;
- KNN;
- SVM;
- Regressão Logística com regularização;
- Regressão Linear com regularização;
- Redes neurais;
- LSTM;
- DBSCAN;
- normalização de pixels em imagem.

## Scaling costuma importar pouco para

- Decision Trees;
- Random Forest;
- XGBoost;
- LightGBM;
- CatBoost;
- baselines simples baseados em regra.

## Regra prática

Não crie um `scaler.py` para tudo. Um nome melhor de módulo é:

```text
preprocessing.py
```

Porque scaling é só uma parte do pré-processamento.
