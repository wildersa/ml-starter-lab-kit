# Hiperparâmetros

Hiperparâmetros são configurações escolhidas antes ou ao redor do treino.

Eles não são aprendidos diretamente dos dados como os pesos do modelo.

## Hiperparâmetros são iguais para todo modelo?

Não.

Cada família de modelo tem seus próprios hiperparâmetros.

## Categorias comuns

| Categoria | Exemplos |
|---|---|
| Hiperparâmetros do modelo | `max_depth`, `n_estimators`, `n_clusters`, `n_components` |
| Hiperparâmetros de treino | `learning_rate`, `epochs`, `batch_size` |
| Hiperparâmetros de pré-processamento | tipo de scaler, estratégia de preenchimento, estratégia de encoding |
| Hiperparâmetros de busca | tamanho do grid, número de tentativas, semente aleatória |

## Exemplos por família de modelo

| Modelo/família | Hiperparâmetros comuns |
|---|---|
| XGBoost | `max_depth`, `learning_rate`, `n_estimators`, `subsample` |
| K-Means | `n_clusters`, `init`, `max_iter`, `random_state` |
| PCA | `n_components`, opção de whitening |
| LSTM | número de units, camadas, dropout, tamanho da sequência, epochs, batch size |
| Random Forest | `n_estimators`, `max_depth`, `min_samples_leaf` |
| Bandits | taxa de exploração, priors, parâmetro de confiança |

## Conselho prático

Comece com poucos hiperparâmetros importantes.

Não tente tunar tudo de uma vez.

Veja também: [otimização de hiperparâmetros](hyperparameter-optimization.pt-BR.md).
