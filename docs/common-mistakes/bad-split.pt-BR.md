# Split ruim

Um split ruim torna a avaliação não confiável.

## Casos comuns

- split aleatório em série temporal;
- mesmo usuário aparece em treino e teste quando a separação por usuário importa;
- pré-processamento aprende com todos os dados antes do split;
- duplicados aparecem em treino e teste.

## Regra prática

Faça o split de um jeito que simule o cenário real de previsão.
