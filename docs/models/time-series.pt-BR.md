# Séries temporais e LSTM

Use métodos de série temporal quando a ordem dos eventos importa.

Exemplos:

- prever vendas;
- prever demanda;
- estimar tráfego futuro;
- detectar padrões temporais.

## Regra importante

Não use split aleatório por padrão.

Em série temporal, treine no passado e teste no futuro.

```text
dados passados -> treino
dados futuros -> teste
```

## Features comuns

- valores defasados, ou lags;
- média móvel;
- desvio padrão móvel;
- dia da semana;
- mês;
- feriados/eventos;
- indicadores de tendência.

## LSTM em uma frase

LSTM é uma arquitetura de rede neural feita para aprender padrões em sequências.

## Quando LSTM pode fazer sentido

- Você tem dados temporais suficientes.
- Padrões sequenciais são importantes.
- Baselines simples não são suficientes.

## Comece mais simples antes

Antes de LSTM, teste:

- baseline do último valor;
- média móvel;
- regressão linear com lags;
- modelo de árvore com features temporais.

## Erros comuns

- Split aleatório.
- Vazamento em features móveis.
- Não comparar com baseline simples.
- Usar LSTM com poucos dados.
