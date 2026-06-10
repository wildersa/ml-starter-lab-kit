# Métricas de Regressão

Use métricas de regressão quando seu modelo prevê um número contínuo (ex: preços de casas, temperatura ou volume de vendas).

## MAE (Erro Médio Absoluto)

- **O que responde**: Em média, quão distantes estão as previsões, na mesma unidade do alvo?
- **Quando usar**: Quando você quer uma métrica de erro fácil de explicar para partes interessadas não técnicas. Trata todos os erros com o mesmo peso.
- **Quando evitar**: Quando você deseja penalizar especificamente grandes outliers.
- **Exemplo**: Um MAE de 5,0 na previsão de preços de casas (em milhares) significa que o modelo erra por R$ 5.000 em média.

## RMSE (Raiz do Erro Quadrático Médio)

- **O que responde**: Qual é a magnitude do erro, com uma penalidade maior para grandes erros?
- **Quando usar**: Quando grandes erros são muito mais caros do que pequenos erros.
- **Armadilha comum**: O RMSE é sensível a outliers. Um único erro enorme pode inflar significativamente o RMSE.
- **Exemplo**: Se a maioria dos erros for pequena, mas um for muito grande, o RMSE será muito superior ao MAE.

## R² (Coeficiente de Determinação)

- **O que responde**: Quanto da variância nos dados é explicada pelo modelo?
- **Quando usar**: Para entender o quanto seu modelo é melhor do que apenas prever o valor médio.
- **Quando evitar**: Sozinho. Um R² alto não significa que o modelo é "bom" se ele for tendencioso ou se os dados tiverem padrões específicos que o modelo ignora.
- **Exemplo**: Um R² de 0,80 significa que 80% da variação no alvo é explicada por suas variáveis (features).

## MAPE (Erro Percentual Absoluto Médio)

- **O que responde**: Qual é o erro percentual médio?
- **Quando usar**: Quando você precisa comunicar o erro em termos relativos (ex: "estamos errando em 10%").
- **Quando evitar**: Quando os valores reais podem ser zero ou muito próximos de zero (pois leva a divisão por zero ou valores extremos).
- **Armadilha comum**: O MAPE é assimétrico; ele penaliza menos as superestimativas do que as subestimativas.
- **Exemplo**: Um MAPE de 0,10 significa que suas previsões estão, em média, a 10% de distância do valor real.

---

### Dica Prática

Sempre verifique o [Checklist Antes da Avaliação](../checklists/before-evaluation.pt-BR.md) para garantir que suas métricas sejam confiáveis e correspondam aos seus objetivos de negócio.
