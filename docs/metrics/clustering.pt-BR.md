# Métricas de agrupamento (Clustering)

O agrupamento é não supervisionado, o que significa que não há uma "resposta certa" para comparar. A avaliação consiste em encontrar padrões que façam sentido para o negócio.

Para um mergulho profundo em como medir o desempenho do modelo e como isso se relaciona com o valor de negócio, consulte o guia de [Avaliação e Monitoramento](../concepts/evaluation-and-monitoring.md).

## Inércia (Soma dos Quadrados Dentro do Cluster)

- **O que responde:** Quão compactos estão os clusters?
- **Quando usar:** No K-Means, para ajudar a escolher o número de clusters (o "Método do Cotovelo" ou Elbow Method).
- **Quando evitar:** Quando seus clusters têm formas irregulares (não esféricas).
- **Armadilha comum:** Assumir que uma inércia menor sempre significa melhores clusters. Um modelo com tantos clusters quanto pontos de dados tem inércia zero, mas é inútil.
- **Exemplo:** Na segmentação de clientes, observando como a inércia cai à medida que você passa de 2 para 5 clusters.

## Silhouette Score (Coeficiente de Silhueta)

- **O que responde:** Quão bem separados estão os clusters? (Os pontos estão muito mais próximos do seu próprio cluster do que dos outros?)
- **Quando usar:** Para avaliar a qualidade de um agrupamento sem conhecer a verdade absoluta. Varia de -1 a 1.
- **Quando evitar:** Em conjuntos de dados muito grandes, pois o cálculo pode ser computacionalmente caro.
- **Armadilha comum:** Confiar apenas na pontuação média. Você também deve olhar para o gráfico de silhueta de cada cluster para garantir que todos estejam "saudáveis".
- **Exemplo:** Uma pontuação de 0,6 sugere uma estrutura forte, enquanto 0,2 sugere sobreposição significativa.

## Interpretação Qualitativa de Clusters

- **O que responde:** Esses grupos realmente significam algo para o negócio?
- **Quando usar:** Sempre. Após o agrupamento, você deve "perfilar" os clusters analisando as médias de suas características.
- **Quando evitar:** Nunca.
- **Armadilha comum:** Dar um nome a um cluster (ex: "Clientes VIP") sem verificar se eles realmente gastam significativamente mais do que a média.
- **Exemplo:** Descobrir que o "Cluster 1" representa usuários que visitam apenas nos fins de semana e compram itens de luxo.
