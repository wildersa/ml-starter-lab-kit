# Métricas de séries temporais

A previsão de séries temporais requer métricas especiais porque os dados têm uma ordem temporal. Você não pode simplesmente embaralhar suas linhas.

Para um mergulho profundo em como medir o desempenho do modelo e como isso se relaciona com o valor de negócio, consulte o guia de [Avaliação e Monitoramento](../concepts/evaluation-and-monitoring.pt-BR.md).

## Backtesting (Avaliação Walk-forward)

- **O que responde:** Como meu modelo teria se comportado se eu o tivesse usado no passado para prever o futuro?
- **Quando usar:** Sempre para séries temporais. Em vez de uma divisão aleatória, você treina no "Passado" e testa no "Futuro".
- **Quando evitar:** Nunca. A validação cruzada tradicional (escolhendo linhas aleatoriamente) vazará informações do futuro para o passado.
- **Armadilha comum:** Usar validação cruzada K-fold aleatória. Esta é a principal causa de "falso" alto desempenho em séries temporais.
- **Exemplo:** Treinar com dados de Janeiro a Outubro para prever Novembro, depois de Janeiro a Novembro para prever Dezembro.

## Avaliação por Horizonte (Horizon) e Janela (Window)

- **O que responde:** A precisão do modelo muda à medida que tentamos prever mais longe no futuro (Curto prazo vs. Longo prazo)?
- **Quando usar:** Quando seu negócio precisa planejar vários passos à frente (ex: estoque para os próximos 7 dias).
- **Quando evitar:** Quando você só se importa com o passo imediatamente seguinte.
- **Armadilha comum:** Relatar um único número de erro para uma previsão de 30 dias. Geralmente, o dia 1 é muito mais preciso que o dia 30.
- **Exemplo:** Medir o MAE especificamente para "1 dia à frente", "7 dias à frente" e "30 dias à frente".

## MAE e RMSE (Contexto de séries temporais)

- **O que responde:** O mesmo que na regressão, mas analisado ao longo do tempo.
- **Quando usar:** Para entender a escala absoluta do erro em sua previsão.
- **Armadilha comum:** Não verificar se o erro é "viesado" (ex: o modelo sempre subestima as vendas durante os fins de semana).

## MAPE e sMAPE

- **O que responde:** Erro percentual, permitindo a comparação entre produtos com diferentes volumes de vendas.
- **Quando usar:** Quando você precisa comparar a qualidade da previsão de um item de alto volume vs um item de baixo volume.
- **Quando evitar:** **Limitação:** Como na regressão, evite quando os valores podem ser zero. O **sMAPE** (MAPE Simétrico) lida um pouco melhor com zeros, mas é mais difícil de interpretar.
- **Armadilha comum:** Confiar no MAPE para demanda "intermitente" (itens que vendem zero na maioria dos dias).
- **Exemplo:** Um erro de 10% em um produto que vende 1000 unidades é a mesma "pontuação" que um erro de 10% em um que vende 10 unidades.
