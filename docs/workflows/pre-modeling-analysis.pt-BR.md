# Análise Pré-Modelagem

Antes de treinar modelos complexos, é essencial entender seus dados. A análise pré-modelagem é um fluxo de diagnóstico que ajuda a identificar bugs, sinais e riscos antecipadamente.

Este guia organiza essas análises em um fluxo lógico de aprendizado para ajudar você a decidir se um conjunto de dados está pronto para a modelagem de baseline.

## Fluxo de Aprendizado

1. **Entender o Dataset**: Tenha uma visão de alto nível do que você tem.
2. **Entender Distribuições**: Observe colunas individuais isoladamente.
3. **Entender Relacionamentos de Features**: Veja como as colunas interagem entre si.
4. **Proteger a Validação**: Garanta que sua estratégia de avaliação seja robusta contra vazamento (leakage).
5. **Medir Sinal Preditivo Inicial**: Verifique se as features realmente se relacionam com o alvo (target).
6. **Inspecionar Riscos por Segmento**: Procure por desequilíbrios ou vieses em grupos específicos.
7. **Decisão**: Determine se a qualidade dos dados e o sinal são suficientes para prosseguir.

---

## Primeira Decisão: Você tem um Alvo (Target)?

A maioria das análises pré-modelagem começa com uma pergunta:

```text
Eu tenho uma resposta histórica/gabarito para cada linha?
```

Se sim, o problema é geralmente **supervisionado**. Você pode perguntar se as features ajudam a prever esse alvo.

Se não, o problema é **não supervisionado**. Você não pode medir o poder preditivo contra um alvo, então a análise muda: você procura por estrutura, grupos, redundância, anomalias ou representações úteis.

```text
Tem um alvo?
|
|-- Sim -> pré-análise supervisionada
|          features + alvo -> modelo rápido -> métricas + importância de features
|
`-- Não -> pré-análise não supervisionada
           apenas features -> estrutura, clusters, anomalias, variância, visualização
```

---

## Pré-Análise Supervisionada: Sinal Preditivo

Use isto quando o dataset tiver uma coluna de alvo.

Exemplos:

- `churn`: o cliente cancelou?
- `fraude`: a transação foi fraudulenta?
- `preco`: preço de venda observado.
- `tempo_entrega`: tempo de entrega observado.
- `conversao`: o usuário converteu?

Pergunta principal:

```text
Estas features ajudam a prever este alvo?
```

Um modelo de sondagem (probe) supervisionado rápido é útil aqui. Não é o modelo final. É um passo de diagnóstico.

Modelos de sondagem comuns:

- XGBoost
- LightGBM
- Random Forest
- Árvore de Decisão rasa
- Regressão Logística
- Regressão Linear
- Execução simples de AutoML

Isto pode revelar:

- se o dataset tem sinal preditivo;
- se a pontuação inicial é plausível;
- quais features parecem úteis;
- se uma feature pode estar vazando informação futura;
- se o problema parece simples, difícil, ruidoso ou mal formulado;
- se vale a pena avançar para o treinamento e avaliação adequados.

Fluxo típico:

```text
dataset com alvo
-> pré-processamento mínimo
-> modelo de sondagem supervisionado rápido
-> métricas iniciais
-> importância de features
-> revisão de vazamento e sanidade de features
-> decisão: continuar, corrigir dados ou reformular o problema
```

Para dados tabulares, o XGBoost ou outro modelo de boosting de árvore é frequentemente uma sondagem padrão forte porque pode capturar relacionamentos não lineares e interações de features com pouca engenharia manual. Ainda assim, é apenas uma baseline de diagnóstico, não uma prova de que o modelo final deve ser XGBoost.

---

## Pré-Análise Não Supervisionada: Estrutura Sem um Alvo

Use isto quando não houver uma coluna de alvo.

Neste caso, não pergunte:

```text
Qual feature prevê melhor o alvo?
```

Não há alvo. Pergunte, em vez disso:

```text
Existe uma estrutura útil nos dados?
```

Perguntas comuns:

- Existem grupos naturais?
- Existem registros incomuns?
- Algumas colunas são redundantes?
- Os dados podem ser simplificados em menos dimensões?
- Padrões tornam-se visíveis em 2D ou 3D?
- Quais features ajudam a separar perfis ou explicar a variância?

Ferramentas úteis:

| Objetivo | Ferramentas comuns |
|---|---|
| Encontrar grupos simples | K-Means |
| Encontrar grupos irregulares ou ruído | DBSCAN, HDBSCAN |
| Reduzir dimensionalidade | PCA |
| Visualizar estrutura | UMAP, t-SNE |
| Detectar anomalias | Isolation Forest, Local Outlier Factor, One-Class SVM |
| Avaliar separação de clusters | Silhouette Score, Davies-Bouldin, Calinski-Harabasz |
| Encontrar features redundantes | Correlação, VIF, verificações de colinearidade |

Fluxo típico:

```text
dataset sem alvo
-> EDA e limpeza de dados
-> codificação e escala quando necessário
-> PCA ou UMAP para exploração de estrutura
-> clustering ou detecção de anomalias
-> interpretação humana de grupos/padrões
-> decisão: segmentar, rotular, coletar alvo ou continuar a exploração
```

Limitação importante:

```text
O algoritmo pode produzir grupo 0, grupo 1 e grupo 2.
O analista dá a esses grupos um significado de negócio.
```

A análise não supervisionada é geralmente menos conclusiva do que a importância de features supervisionada porque não há uma resposta de verdade (ground-truth) para otimizar contra.

---

## Importância de Features Significa Coisas Diferentes

No aprendizado supervisionado:

```text
feature importante = ajuda a prever o alvo
```

No aprendizado não supervisionado:

```text
feature importante = ajuda a explicar a variância, separação, agrupamento ou comportamento de anomalia
```

Essa diferença importa. Um gráfico de importância de features supervisionado responde a uma pergunta mais direta porque está ancorado a um alvo conhecido.

Sem um alvo, a relevância da feature é mais exploratória e depende do objetivo da análise.

---

## Onde as Redes Neurais se Encaixam

Redes neurais não são um tipo de aprendizado separado. Elas são arquiteturas de modelo.

Uma rede neural pode ser usada para:

- classificação supervisionada;
- regressão supervisionada;
- previsão de séries temporais;
- tarefas de texto, imagem e áudio;
- embeddings;
- autoencoders;
- detecção de anomalias;
- aprendizado de representação auto-supervisionado.

Para dados tabulares regulares, as redes neurais geralmente não são a primeira ferramenta de pré-análise porque costumam ser mais pesadas, mais sensíveis ao pré-processamento, menos interpretáveis e exigem mais ajuste do que os modelos baseados em árvores.

Para dados não estruturados, as redes neurais são frequentemente centrais:

```text
texto/imagem/áudio
-> modelo neural pré-treinado
-> embedding
-> classificador, busca, clustering, detecção de anomalias ou modelo downstream
```

Regra prática:

```text
Pré-análise supervisionada tabular -> sondagem rápida de árvore/linear primeiro.
Pré-análise de texto/imagem/áudio -> embeddings ou modelos neurais pré-treinados podem ser a primeira representação útil.
```

---

## Famílias de Análise

### 1. Profiling de Dados e Resumo Estatístico

Esta é a "visão panorâmica" dos seus dados. Inclui verificar o número de registros, o número de features e estatísticas básicas como média, mediana, desvio padrão, mín e máx.

- **Objetivo**: Detectar problemas óbvios de escala ou erros de entrada de dados.

### 2. Integridade Estrutural

Verifique o "débito técnico" nos dados:

- **Tipos de Dados**: Números estão armazenados como strings? Datas são reconhecidas corretamente?
- **Valores Ausentes**: Quanta informação falta? A ausência é aleatória?
- **Cardinalidade**: Features categóricas têm muitos valores únicos, como um ID único por linha?
- **Duplicados**: Existem linhas redundantes que podem inflar suas métricas de desempenho?

### 3. Análise de Distribuição

Use histogramas e gráficos de densidade para ver como os valores estão espalhados.

- **Objetivo**: Identificar outliers, distribuições enviesadas ou lacunas inesperadas nos dados.
- **Aplicação**: Crucial para aprendizado supervisionado e clustering.

### 4. Verificação Visual de Relacionamentos

Use gráficos de dispersão (scatter plots) ou box plots para visualizar a relação entre duas variáveis.

- **Objetivo**: Identificar padrões não lineares ou clusters que estatísticas de resumo podem ignorar.

### 5. Correlação e Redundância

Meça o quanto as features se movem juntas, por exemplo, com correlação de Pearson ou Spearman.

- **Multicolinearidade**: Alta correlação entre entradas pode tornar alguns modelos instáveis ou suas explicações difíceis de confiar.
- **Redundância**: Se duas features são quase idênticas, você pode precisar de apenas uma.

### 6. Vazamento (Leakage) e Disponibilidade

Esta é a verificação mais crítica para o aprendizado supervisionado.

- **Vazamento de Alvo (Target Leakage)**: Uma feature contém informações do futuro? Se uma feature "prevê" o alvo perfeitamente, provavelmente é um bug.
- **Disponibilidade**: Esta feature estará realmente disponível no momento exato em que o modelo precisar fazer uma previsão em produção?

### 7. Screening Preditivo Univariado

Teste cada feature individualmente para ver quão bem ela prevê o alvo, por exemplo, usando um modelo simples de proxy ou ganho de informação.

- **Objetivo**: Identificar os candidatos mais promissores e possíveis vazamentos precocemente.

### 8. Baseline Rápida / Modelo de Sondagem (Probe)

Treine um modelo simples ou um modelo tabular rápido em um subconjunto controlado de features.

- **Objetivo**: Definir um piso de desempenho e medir o sinal preditivo inicial.
- **Exemplos**: árvore rasa, regressão linear/logística, Random Forest, XGBoost, LightGBM.
- **Atenção**: Uma pontuação rápida forte também pode indicar vazamento. Sempre inspecione a disponibilidade das features.

### 9. Verificações por Segmento

Analise o desempenho e a distribuição dos dados em diferentes grupos, como região, categoria, canal ou segmento de cliente.

- **Desequilíbrio de Classes**: Uma categoria é muito mais rara que as outras?
- **Viés**: Existem grupos onde a qualidade dos dados é menor ou o sinal está ausente?

### 10. Consistência Temporal

Para séries temporais ou dados ordenados temporalmente, verifique como as distribuições mudam ao longo do tempo.

- **Objetivo**: Garantir que sua divisão de validação, como "passado vs futuro", corresponda ao caso de uso real.

---

## Aplicação Específica por Problema

| Família de Análise | Tabular Supervisionado | Séries Temporais | Clustering | Visão / Texto | Bandit / RL |
|---|---|---|---|---|---|
| Integridade Estrutural | Essencial | Essencial | Essencial | Relevante | Essencial |
| Distribuições | Essencial | Essencial | Essencial | Apenas metadados | Essencial |
| Vazamento de Alvo | Crítico | Crítico | N/A | Relevante | Crítico |
| Checagens Temporais | Relevante | Crítico | Relevante | Relevante | Essencial |
| Checagens por Segmento | Essencial | Essencial | Essencial | Relevante | Essencial |
| Modelo Probe Rápido | Útil | Útil com divisão temporal | N/A | Útil após embeddings | Útil apenas offline |
| PCA / UMAP | Opcional | Opcional | Útil | Útil após embeddings | Opcional |
| Clustering | Opcional para segmentação | Opcional | Core | Útil após embeddings | Opcional |
| Detecção de Anomalias | Opcional | Útil | Útil | Útil | Útil para monitoramento |

---

## Mapa de Decisão Prático

```text
Eu tenho um dataset.
|
|-- Eu tenho um alvo?
|   |
|   |-- Sim
|   |   |-- O alvo é categórico? -> classificação supervisionada
|   |   |-- O alvo é numérico?   -> regressão supervisionada
|   |   `-- Pré-análise: modelo probe rápido, métricas, importância de features, checagem de vazamento
|   |
|   `-- Não
|       |-- Quero grupos?           -> clustering
|       |-- Quero compressão?       -> redução de dimensionalidade
|       |-- Quero pontos estranhos? -> detecção de anomalias
|       `-- Pré-análise: PCA/UMAP, clustering, detecção de anomalias, checagem de redundância
```

---

## Saiba Mais

- [scikit-learn: Common pitfalls in the interpretation of coefficients](https://scikit-learn.org/stable/auto_examples/inspection/plot_linear_model_coefficient_interpretation.html)
- [scikit-learn: Visualizing data](https://scikit-learn.org/stable/visualizations.html)
- [scikit-learn: Clustering](https://scikit-learn.org/stable/modules/clustering.html)
- [scikit-learn: Novelty and Outlier Detection](https://scikit-learn.org/stable/modules/outlier_detection.html)
- [Documentação do XGBoost](https://xgboost.readthedocs.io/)

## Limitações

- **Análise não é Treinamento**: Essas verificações encontram problemas; elas não os corrigem. Você ainda precisa realizar o pré-processamento, engenharia de features, treinamento e avaliação adequados.
- **Sinais Falsos**: Alta correlação ou alta importância de feature não implica causalidade. Uma "feature forte" na análise pode falhar se o processo subjacente mudar.
- **Ambiguidade Não Supervisionada**: Clusters e anomalias não são automaticamente significativos. Eles precisam de interpretação humana e validação.
- **Custo de Rede Neural**: Abordagens neurais podem ser poderosas, especialmente para dados não estruturados, mas podem ser excessivas para diagnósticos tabulares iniciais.
- **Custo da Análise**: Evite a paralisia por análise. O objetivo é chegar a uma baseline confiável rapidamente, não encontrar todas as correlações possíveis.
