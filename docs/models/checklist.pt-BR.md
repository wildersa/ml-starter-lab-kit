# Checklist inicial de ML

Use este checklist antes de treinar qualquer coisa.

## 1. Defina o problema

- Classificação: prever uma classe.
- Regressão: prever um número.
- Clusterização: encontrar grupos.
- Série temporal: prever valores futuros.
- Bandit/RL: escolher ações e aprender com recompensas.

## 2. Entenda os dados

Verifique:

- quantidade de linhas e colunas;
- valores ausentes;
- linhas duplicadas;
- distribuição do target;
- colunas de data;
- colunas categóricas;
- possível vazamento de dados.

## 3. Crie um baseline

Baseline é uma referência simples.

Exemplos:

- classe majoritária;
- valor médio;
- último valor conhecido;
- política aleatória;
- regra fixa de negócio.

Um modelo complexo só faz sentido se superar o baseline.

## 4. Separe os dados corretamente

- Split aleatório serve para muitos problemas tabulares.
- Série temporal precisa de split cronológico.
- Dados por usuário/evento podem precisar de split agrupado.

## 5. Avalie com a métrica certa

Exemplos:

- Accuracy: classificação simples.
- F1: classificação desbalanceada.
- AUC: qualidade de ranking/probabilidade.
- MAE/RMSE: regressão.
- MAPE: erro de previsão, quando fizer sentido.
- Regret/reward: bandits.

## 6. Documente limitações

Sempre escreva para que o modelo não deve ser usado.
