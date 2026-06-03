# Reinforcement Learning

Reinforcement Learning, ou RL, é usado quando um agente aprende interagindo com um ambiente.

O agente toma ações, recebe recompensas e tenta melhorar decisões futuras.

## Ideia básica

```text
estado -> ação -> recompensa -> novo estado
```

## Use RL quando

- decisões afetam situações futuras;
- o feedback vem como recompensa;
- exploração faz parte do problema;
- existe simulador ou ambiente seguro.

## Exemplos

- jogos;
- controle de robôs;
- simulação de preço dinâmico;
- alocação de recursos;
- sistemas de decisão sequencial.

## Conceitos importantes

| Conceito | Significado |
|---|---|
| Agente | quem toma a decisão |
| Ambiente | mundo onde as ações acontecem |
| Estado | situação atual |
| Ação | escolha do agente |
| Recompensa | sinal de feedback |
| Política | regra usada para escolher ações |

## Aviso prático

RL costuma ser mais difícil que aprendizado supervisionado.

Se o problema puder ser resolvido com [modelo supervisionado](supervised.pt-BR.md), regra simples ou [bandit](bandits.pt-BR.md), comece por aí.
