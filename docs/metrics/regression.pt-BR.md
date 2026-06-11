# Métricas de regressão

Use métricas de regressão quando o modelo prevê um número contínuo (ex: preço, temperatura ou distância).

Para um mergulho profundo em como medir o desempenho do modelo e como isso se relaciona com o valor de negócio, consulte o guia de [Avaliação e Monitoramento](../concepts/evaluation-and-monitoring.md).

## MAE (Erro Médio Absoluto)

- **O que responde:** Em média, quão longe as previsões estão dos valores reais?
- **Quando usar:** Quando você quer uma métrica de erro que esteja na mesma unidade do seu alvo e seja fácil de explicar para pessoas não técnicas.
- **Quando evitar:** Quando erros grandes (outliers) são muito mais "dolorosos" do que erros pequenos.
- **Armadilha comum:** Comparar o MAE entre diferentes conjuntos de dados com escalas diferentes.
- **Exemplo:** Se você prevê preços de casas e seu MAE é R$ 10.000, suas previsões erram por R$ 10.000 em média.

## RMSE (Raiz do Erro Quadrático Médio)

- **O que responde:** Qual é a magnitude média do erro, com uma penalidade maior para grandes erros?
- **Quando usar:** Quando erros grandes são particularmente indesejáveis (ex: atrasar 10 dias em uma entrega é muito pior do que atrasar 1 dia 10 vezes).
- **Quando evitar:** Quando seus dados têm muitos outliers que estão corretos, mas que dominarão a métrica.
- **Armadilha comum:** Esperar que o RMSE seja tão fácil de interpretar quanto o MAE. Ele é sempre maior ou igual ao MAE.
- **Exemplo:** Um erro de R$ 50.000 na previsão de uma casa de R$ 200.000 aumentará o RMSE significativamente mais do que aumentaria o MAE.

## MAPE (Erro Médio Percentual Absoluto)

- **O que responde:** Qual é o erro percentual médio em relação aos valores reais?
- **Quando usar:** Quando você precisa comunicar o erro para pessoas que não conhecem a escala dos dados (ex: "O modelo acerta 95% em média").
- **Quando evitar:** **Limitação Crucial:** Quando os valores reais são zero ou muito próximos de zero, pois a divisão levará a valores indefinidos ou extremos.
- **Armadilha comum:** Usar MAPE em dados que podem ser zero (como milímetros de chuva ou vendas diárias de uma loja pequena).
- **Exemplo:** Prever 110 para um valor real de 100 resulta em um MAPE de 10%.

## R² (R-Quadrado)

- **O que responde:** Quanto da variância no alvo é explicada pelo modelo?
- **Quando usar:** Para ter uma noção de quanto seu modelo é melhor do que apenas prever o valor médio.
- **Quando evitar:** Quando você se importa com o erro absoluto em vez da explicação relativa da variância.
- **Armadilha comum:** Um R² alto não significa que o modelo é "bom" se os dados subjacentes forem muito ruidosos ou se o modelo estiver com overfitting.
- **Exemplo:** Um R² de 0,8 significa que seu modelo explica 80% do movimento nos dados.
