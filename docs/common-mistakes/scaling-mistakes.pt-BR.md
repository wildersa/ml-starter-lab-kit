# Erros de scaling

Scaling é útil, mas nem sempre necessário.

## Erros comuns

- escalar usando todos os dados antes do split;
- esquecer scaling em K-Means ou PCA;
- assumir que XGBoost precisa de scaling por padrão;
- escalar IDs ou códigos categóricos como se fossem valores numéricos reais.

## Regra prática

Use scaling quando o modelo depende de distância, variância, gradientes ou otimização numérica.

Não escale no automático.
