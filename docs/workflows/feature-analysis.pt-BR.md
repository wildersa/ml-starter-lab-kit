# Análise de Features Assistida por Modelo

A análise de features é uma etapa de diagnóstico onde você usa modelos simples para entender a relação entre suas colunas de entrada e o alvo (target). Ela ocorre após o EDA e antes do ajuste final do modelo.

## Engenharia vs. Análise vs. Seleção

| Termo | Objetivo |
|---|---|
| **Engenharia de Features** | Criar novas colunas (ex: razões, agregações, codificações). |
| **Análise de Features** | Estudar quanto sinal cada feature fornece a um modelo. |
| **Seleção de Features** | Escolher o melhor subconjunto de features para reduzir ruído ou custo. |

## 1. Triagem Preditiva Univariada (Univariate Screening)

Esta técnica envolve treinar um modelo "proxy" muito pequeno (como uma Árvore de Decisão rasa ou Regressão Logística) usando apenas **uma feature por vez**.

- **Por que:** Estima se uma feature tem sinal por conta própria.
- **Interpretação:** Se uma única feature gera uma métrica alta (ex: AUC alto ou MAE baixo), ela é um preditor forte.
- **Aviso:** Se uma feature mostra resultados quase perfeitos sozinha, isso geralmente indica **vazamento de alvo (target leakage)** (informações do futuro que não estarão disponíveis no momento da predição).

## 2. Importância Baseada no Modelo

Depois de ter um modelo de linha de base (baseline) treinado com muitas features, você pode extrair pontuações de "importância" (como a importância de Gini em Random Forests).

- **Por que:** Mostra em quais features o modelo mais confiou durante o treinamento.
- **Limitação:** Alta importância nem sempre significa que a feature é "boa"; apenas significa que o modelo a usou. Se a feature estiver vazada, ela terá alta importância, mas falhará em produção.

## 3. Importância por Permutação (Permutation Importance)

Este método mede quanto a métrica de validação cai quando você embaralha aleatoriamente os valores de uma única feature.

- **Por que:** Calcula o impacto real da feature no desempenho do modelo em dados não vistos.
- **Benefício:** É mais robusto do que a importância bruta de treinamento porque utiliza o conjunto de validação.

## Princípios Chave de Diagnóstico

### Estas são ferramentas, não "A Verdade"
A análise de features ajuda a encontrar bugs e sinais, mas não prova que uma feature é essencial globalmente. Ela apenas mostra como a feature se comporta com um modelo e conjunto de dados específicos.

### Interações Importam
Uma feature pode ter um "sinal baixo" na triagem univariada, mas tornar-se extremamente poderosa quando combinada com outra feature (interação). Não descarte features baseando-se apenas em resultados univariados.

### Detecção de Vazamento (Leakage)
Se uma feature que deveria ser "fraca" (como um ID aleatório ou um CEP) mostrar alto poder preditivo, investigue imediatamente. Você pode estar diante de um bug de vazamento.

### Consistência de Divisão e Métrica
Sua análise de features deve usar a mesma **estratégia de divisão** (ex: divisão temporal para séries temporais) e **métrica** (ex: F1-score para classes desbalanceadas) que sua avaliação final. Usar configurações diferentes levará a conclusões enganosas.
