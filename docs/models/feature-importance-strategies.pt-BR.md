# Matriz de Estratégia de Importância de Variáveis

A importância de uma variável (feature importance) não é uma "verdade" única. A relevância de uma coluna depende da arquitetura do modelo, da métrica escolhida, de como os dados foram divididos e de quais informações estão disponíveis no momento da predição.

Este guia fornece uma matriz de estratégia para ajudar você a escolher a técnica de análise correta para o seu problema.

## Matriz de Estratégia

| Tipo de Problema | Família do Modelo | Técnica de Análise | Métricas Primárias | Estratégia de Divisão |
|---|---|---|---|---|
| **Classificação** | Árvore/Boosting | Gini, Permutação | F1-Score, AUC | Aleatória Estratificada |
| **Classificação** | Linear/Kernel | Coeficientes, Vetores de Suporte | Acurácia, Log Loss | Aleatória Estratificada |
| **Regressão** | Árvore/Boosting | Redução de Variância, Permutação | MAE, RMSE | Aleatória |
| **Regressão** | Linear/Kernel | Coeficientes, Pesos Duais | R-quadrado, MAE | Aleatória |
| **Séries Temporais** | Linear/Árvore/Deep | Importância por Permutação | MAE, RMSE, WAPE | Temporal (Janela) |
| **Agrupamento** | Distância/Kernel | Análise de Centroides, Silhueta | Score de Silhueta | Nenhuma (Dados Totais) |
| **Decisão Adaptativa (Bandit)** | Linear/Probabilístico | Análise de Pesos, Propensão | Recompensa, Regret, Lift | Divisão por Política de Log |
| **Visão** | Neural/Deep | Mapas de Saliência, Ativação | Acurácia, mAP | Aleatória/Estratificada |

## Quando Usar Cada Técnica

### 1. Importância Específica do Modelo
- **Modelos Lineares**: Use coeficientes. As variáveis devem estar na mesma escala (ex: via técnicas de escala padrão) para que a magnitude seja comparável.
- **Modelos de Árvore**: Use medidas de importância nativas baseadas em impureza ou ganho (gain). São rápidas, mas podem ser tendenciosas para variáveis categóricas de alta cardinalidade.
- **Modelos de Kernel**: A análise depende da influência dos vetores de suporte ou pesos no espaço dual. A importância é frequentemente mais difícil de interpretar diretamente em comparação com coeficientes lineares.
- **Modelos Probabilísticos**: Use pesos posteriores (posterior weights) ou o impacto da variável na distribuição de probabilidade.

### 2. Agnóstico ao Modelo (Importância por Permutação)
Esta técnica embaralha uma única variável e mede a queda no score do modelo.
- **Ideal para**: Comparar famílias de modelos diferentes sob o mesmo critério.
- **Benefício**: Pode refletir como o modelo utiliza as interações entre variáveis para realizar predições.
- **Aviso**: Se as variáveis forem altamente correlacionadas (colinearidade), a importância por permutação pode ser enganosa, pois o modelo pode usar uma variável correlacionada como substituta, resultando em uma importância relatada menor para ambas.
- **Requisito**: Exige um conjunto de validação separado para evitar medir o quanto o modelo "decorou" (overfit) uma variável.

### 3. Seleção Preditiva Univariada
Mede a relação entre uma variável e o alvo de forma independente (ex: correlação ou informação mútua).
- **Útil quando**: Você tem milhares de variáveis e precisa remover ruído antes do treino.
- **Enganoso quando**: Variáveis só agregam valor quando combinadas com outras (interações).

## Desafios de Domínio

### Séries Temporais
**Nunca use divisões aleatórias.** Se você usar uma divisão aleatória para calcular a importância, o modelo pode sofrer "vazamento" (leakage) de informações do futuro para prever o passado, fazendo uma variável parecer mais importante do que realmente é em produção. Sempre use uma divisão temporal (treino no passado, teste no "futuro").

### Agrupamento (Clustering) e Visão
Estes domínios **não** mapeiam o poder preditivo coluna por coluna de forma direta.
- **Agrupamento**: As variáveis definem o espaço. A análise geralmente envolve verificar como as distribuições diferem entre grupos, em vez de "prever" um rótulo.
- **Visão**: A importância é espacial (quais pixels importam) em vez de tabular. A importância global é frequentemente substituída por mapas de calor ou mapas de saliência.

### Bandits Contextuais e Labs Adaptativos
Analisar logs de bandits exige cuidado porque os dados são "viesados" pela política que os coletou.
- **Propensão**: Você deve considerar a probabilidade de uma ação ter sido escolhida (propensity score).
- **Recompensa vs. Ação**: A importância da variável pode descrever o que gera a *recompensa* ou o que gera a *seleção da ação*. São perguntas diferentes.
- **Política de Log**: Sempre avalie a importância em relação a um baseline ou política de coleta.

## Limitações e Avisos

- **Correlação não é Causalidade**: Alta importância significa que o modelo *usou* a variável para reduzir o erro; não prova que a variável *causou* o resultado no mundo real.
- **Colinearidade**: Se duas variáveis são altamente correlacionadas, o modelo pode dividir a "importância" entre elas, fazendo ambas parecerem menos significativas do que realmente são.
- **Dependência da Métrica**: Uma variável pode ser vital para otimizar o RMSE, mas irrelevante para o MAE.

*Fonte: Estratégia baseada em práticas comuns para inspeção de modelos.*
