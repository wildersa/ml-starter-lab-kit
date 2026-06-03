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

## Medindo se uma feature ajudou

Não mantenha uma feature só porque ela parece inteligente.

Meça.

Checagens úteis:

- compare baseline sem a feature vs. baseline com a feature;
- use o mesmo split e a mesma métrica;
- inspecione melhoria por segmento, não só score global;
- verifique se a feature aumenta risco de vazamento;
- veja se a feature é estável entre treino, validação e teste;
- remova features que adicionam complexidade sem ganho mensurável.

Uma tabela simples de impacto pode ser assim:

| Feature | Métrica antes | Métrica depois | Delta | Manter? | Nota |
|---|---:|---:|---:|---|---|
| `media_compra_cliente_30d` | 0.712 | 0.728 | +0.016 | sim | ganho estável |
| `duracao_campanha` | 0.712 | 0.801 | +0.089 | não | risco de vazamento |

Veja [medição de features](../workflows/feature-measurement.pt-BR.md).

## Regra prática

Antes de criar uma feature, pergunte:

```text
Eu saberia esse valor no momento da previsão?
```

Se a resposta for não, provavelmente existe vazamento de informação.

Depois pergunte:

```text
Essa feature melhora a métrica nos dados de validação?
```

Se a resposta for não, remova ou documente por que ela fica.
