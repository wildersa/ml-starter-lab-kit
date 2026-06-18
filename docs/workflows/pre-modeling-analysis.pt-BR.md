# Análise Pré-Modelagem

Antes de treinar modelos complexos, é essencial entender seus dados. A análise pré-modelagem é um fluxo de diagnóstico que ajuda a identificar bugs, sinais e riscos antecipadamente.

Este guia organiza essas análises em um fluxo lógico de aprendizado para ajudar você a decidir se um conjunto de dados está pronto para a modelagem de baseline.

## Fluxo de Aprendizado

1.  **Entender o Dataset**: Tenha uma visão de alto nível do que você tem.
2.  **Entender Distribuições**: Observe colunas individuais isoladamente.
3.  **Entender Relacionamentos de Features**: Veja como as colunas interagem entre si.
4.  **Proteger a Validação**: Garanta que sua estratégia de avaliação seja robusta contra vazamento (leakage).
5.  **Medir Sinal Preditivo Inicial**: Verifique se as features realmente se relacionam com o alvo (target).
6.  **Inspecionar Riscos por Segmento**: Procure por desequilíbrios ou vieses em grupos específicos.
7.  **Decisão**: Determine se a qualidade dos dados e o sinal são suficientes para prosseguir.

---

## Famílias de Análise

### 1. Profiling de Dados e Resumo Estatístico
Esta é a "visão panorâmica" dos seus dados. Inclui verificar o número de registros, o número de features e estatísticas básicas (média, mediana, desvio padrão, mín/máx).
- **Objetivo**: Detectar problemas óbvios de escala ou erros de entrada de dados.

### 2. Integridade Estrutural
Verifique o "débito técnico" nos dados:
- **Tipos de Dados**: Números estão armazenados como strings? Datas são reconhecidas corretamente?
- **Valores Ausentes**: Quanta informação falta? A ausência é aleatória?
- **Cardinalidade**: Features categóricas têm muitos valores únicos (ex: um ID único por linha)?
- **Duplicados**: Existem linhas redundantes que podem inflar suas métricas de desempenho?

### 3. Análise de Distribuição
Use histogramas e gráficos de densidade para ver como os valores estão espalhados.
- **Objetivo**: Identificar outliers, distribuições enviesadas ou lacunas inesperadas nos dados.
- **Aplicação**: Crucial para aprendizado supervisionado e clustering.

### 4. Verificação Visual de Relacionamentos
Use gráficos de dispersão (scatter plots) ou box plots para visualizar a relação entre duas variáveis.
- **Objetivo**: Identificar padrões não lineares ou clusters que estatísticas de resumo podem ignorar.

### 5. Correlação e Redundância
Meça o quanto as features se movem juntas (ex: usando correlação de Pearson ou Spearman).
- **Multicolinearidade**: Alta correlação entre entradas pode tornar alguns modelos instáveis ou suas explicações difíceis de confiar.
- **Redundância**: Se duas features são quase idênticas, você pode precisar de apenas uma.

### 6. Vazamento (Leakage) e Disponibilidade
Esta é a verificação mais crítica para o aprendizado supervisionado.
- **Vazamento de Alvo (Target Leakage)**: Uma feature contém informações do futuro? Se uma feature "prevê" o alvo perfeitamente, provavelmente é um bug.
- **Disponibilidade**: Esta feature estará realmente disponível no momento exato em que o modelo precisar fazer uma previsão em produção?

### 7. Screening Preditivo Univariado
Teste cada feature individualmente para ver quão bem ela prevê o alvo (ex: usando um modelo simples de proxy ou ganho de informação).
- **Objetivo**: Identificar os candidatos mais promissores e possíveis vazamentos precocemente.

### 8. Baseline Rápida / Modelo de Sondagem (Probe)
Treine um modelo muito simples (como uma árvore rasa ou modelo linear) em um subconjunto de features.
- **Objetivo**: Definir um "piso" de desempenho. Se um modelo simples funciona bem, o problema pode não precisar de uma solução complexa.

### 9. Verificações por Segmento
Analise o desempenho e a distribuição dos dados em diferentes grupos (ex: por região, categoria ou demografia).
- **Desequilíbrio de Classes**: Uma categoria é muito mais rara que as outras?
- **Viés**: Existem grupos onde a qualidade dos dados é menor ou o sinal está ausente?

### 10. Consistência Temporal
Para séries temporais ou dados ordenados temporalmente, verifique como as distribuições mudam ao longo do tempo.
- **Objetivo**: Garantir que sua divisão de validação (ex: "passado vs futuro") corresponda ao caso de uso real.

---

## Aplicação Específica por Problema

| Família de Análise | Tabular Supervisionado | Séries Temporais | Clustering | Visão / Texto | Bandit / RL |
|---|---|---|---|---|---|
| Integridade Estrutural | Essencial | Essencial | Essencial | Relevante | Essencial |
| Distribuições | Essencial | Essencial | Essencial | Apenas Metadados | Essencial |
| Vazamento de Alvo | Crítico | Crítico | N/A | Relevante | Crítico |
| Checagens Temporais | Relevante | Crítico | Relevante | Relevante | Essencial |
| Checagens por Segmento | Essencial | Essencial | Essencial | Relevante | Essencial |

## Saiba Mais

- [scikit-learn: Common pitfalls in the interpretation of coefficients](https://scikit-learn.org/stable/auto_examples/inspection/plot_linear_model_coefficient_interpretation.html)
- [scikit-learn: Visualizing data](https://scikit-learn.org/stable/visualizations.html)

## Limitações

- **Análise não é Treinamento**: Essas verificações encontram problemas; elas não os corrigem. Você ainda precisa realizar o pré-processamento e a engenharia de features adequados.
- **Sinais Falsos**: Alta correlação não implica causalidade. Uma "feature forte" na análise pode falhar se o processo subjacente mudar.
- **Custo da Análise**: Evite a "paralisia por análise". O objetivo é chegar a uma baseline confiável rapidamente, não encontrar todas as correlações possíveis.
