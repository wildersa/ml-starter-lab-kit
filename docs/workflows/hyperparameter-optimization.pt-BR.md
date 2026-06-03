# Otimização de hiperparâmetros

Hiperparâmetros são configurações escolhidas antes do treino.

Exemplos:

- profundidade de árvore;
- learning rate;
- número de estimadores;
- regularização;
- batch size;
- número de épocas.

## Comece simples

1. Treine um baseline.
2. Altere um ou dois parâmetros importantes.
3. Compare com o mesmo método de validação.
4. Anote os resultados.

## Abordagens comuns

| Abordagem | Use quando |
|---|---|
| Busca manual | aprendizado ou projetos pequenos |
| Grid search | poucos parâmetros e espaço pequeno |
| Random search | espaço maior |
| Otimização bayesiana | tuning mais avançado |

## Aviso prático

Não faça tuning no conjunto final de teste. Use validação ou cross-validation.
