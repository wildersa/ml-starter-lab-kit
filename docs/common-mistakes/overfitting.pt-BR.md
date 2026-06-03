# Overfitting

Overfitting acontece quando o modelo memoriza os dados de treino em vez de aprender um padrão útil.

## Sinais

- score ótimo no treino;
- score fraco em validação/teste;
- performance instável entre splits;
- modelo depende de features ruidosas.

## Correções práticas

- simplifique o modelo;
- use dados de validação;
- reduza features ruidosas;
- use regularização quando aplicável;
- colete mais dados quando possível.
