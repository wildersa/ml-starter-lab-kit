# Feature Engineering

Feature engineering, ou engenharia de features, é criar colunas úteis para o modelo.

Uma feature é boa quando traz uma informação disponível no momento da previsão.

## Tipos comuns de features

| Tipo | Exemplo | Útil para |
|---|---|---|
| Razão | `preco / quantidade` | modelos tabulares |
| Diferença | `receita - custo` | métricas de negócio |
| Partes de data | dia, mês, dia da semana | sazonalidade |
| Lag | valor de 1 ou 7 períodos atrás | séries temporais |
| Média móvel | média dos últimos 7 dias | tendência/suavização |
| Agregação por grupo | média por cliente | resumo de comportamento |

## Cuidado com vazamento de dados

Não crie features usando informação do futuro.

Exemplo ruim:

```text
usar compras depois da campanha para prever conversão da campanha
```

Exemplo melhor:

```text
usar compras antes da campanha para prever conversão da campanha
```

## Regra prática

Antes de criar uma feature, pergunte:

```text
Eu saberia esse valor no momento da previsão?
```

Se a resposta for não, provavelmente existe vazamento de informação.
