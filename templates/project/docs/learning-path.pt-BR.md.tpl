# Trilhas de Aprendizado: {{PROJECT_NAME}}

Este guia ajuda você a entender o fluxo de trabalho para este projeto de **{{TASK}}**.

## 1. O que significa "{{TASK}}"?

{% if TASK == "supervised" %}
O aprendizado supervisionado consiste em treinar um modelo usando exemplos onde a resposta (alvo/target) já é conhecida. O modelo aprende a mapear entradas (features) para a saída.
{% else %}
{% if TASK == "unsupervised" %}
O aprendizado não supervisionado encontra padrões ou estruturas ocultas nos dados sem rótulos pré-definidos. É frequentemente usado para agrupar itens semelhantes ou reduzir complexidade.
{% else %}
{% if TASK == "timeseries" %}
A análise de séries temporais lida com pontos de dados coletados em intervalos de tempo sucessivos. O objetivo costuma ser prever valores futuros com base no comportamento passado.
{% else %}
{% if TASK == "vision" %}
Tarefas de Visão Computacional envolvem ensinar computadores a "enxergar" e interpretar informações visuais, como classificar imagens ou detectar objetos.
{% else %}
{% if TASK == "bandit" %}
Multi-Armed Bandit (MAB) é uma forma de aprendizado por reforço onde o sistema toma decisões sequenciais (escolhendo "braços") para maximizar uma recompensa, equilibrando exploração e aproveitamento.
{% else %}
Uma estrutura genérica de ML fornece uma organização padrão para dados, features e modelagem, aplicável a diversos fluxos de experimentação customizados.
{% endif %}
{% endif %}
{% endif %}
{% endif %}
{% endif %}

## 2. Entendendo seus dados

Neste contexto:
- **Linhas**: {% if TASK == "bandit" %}Eventos de decisão individuais ou interações.{% else %}Observações ou amostras individuais.{% endif %}
- **Features**: As entradas usadas pelo modelo para entender os dados.
- **{{TARGET_COLUMN}}**: {% if TASK == "supervised" %}A coluna alvo que você deseja prever.{% else %}{% if TASK == "timeseries" %}O valor a ser previsto ao longo do tempo.{% else %}{% if TASK == "bandit" %}A recompensa observada após tomar uma ação.{% else %}{% if TASK == "unsupervised" %}Não há um alvo fixo; analisamos todas as features juntas.{% else %}A principal coluna de interesse para sua tarefa.{% endif %}{% endif %}{% endif %}{% endif %}
{% if TASK == "timeseries" %}
- **Índice de Tempo**: A coluna que define a ordem cronológica dos eventos.
{% endif %}

## 3. O papel do Primeiro Baseline

O primeiro baseline **não** é o seu modelo final. Seu propósito é:
- Estabelecer um "piso de desempenho" (o resultado mínimo que qualquer modelo real deve superar).
- Verificar se o pipeline de dados (carregamento, features, treino) está funcionando.
- Fornecer um ponto de referência para futuras melhorias.

{% if TASK == "supervised" %}
Baselines comuns: Prever o valor médio (Regressão) ou a classe mais frequente (Classificação).
{% else %}
{% if TASK == "bandit" %}
Baselines comuns: Escolher ações aleatoriamente ou sempre escolher a ação com melhor desempenho histórico.
{% endif %}
{% endif %}

## 4. Métricas: O que elas provam (e o que não provam)

Métricas úteis para esta tarefa incluem:
- {% if TASK == "supervised" %}**Acurácia/F1** (Classificação) ou **MAE/RMSE** (Regressão).{% else %}{% if TASK == "timeseries" %}**MAPE/WAPE** para precisão de previsão.{% else %}{% if TASK == "bandit" %}**Recompensa Acumulada** e **Regret**.{% else %}Indicadores de desempenho específicos da tarefa.{% endif %}{% endif %}{% endif %}

**Importante**: Uma boa pontuação métrica não prova que seu modelo é "inteligente" ou "justo". Prova apenas que o modelo encontrou um padrão matemático no conjunto de dados fornecido. Sempre verifique possíveis vieses.

## 5. Erros comuns para verificar

Antes de gastar tempo otimizando:
- **Vazamento de Alvo (Target Leakage)**: Você está usando features que não estariam disponíveis no momento da predição?
- **Dados Desbalanceados**: Uma classe ou cenário é muito mais frequente que os outros?
- **Qualidade dos Dados**: Existem valores ausentes ou outliers que não deveriam estar lá?
{% if TASK == "timeseries" %}
- **Vazamento Cronológico**: Você acidentalmente usou dados do "futuro" para prever o "passado"?
{% endif %}

## 6. O que vem a seguir?

Assim que o baseline estiver rodando:
1. **Engenharia de Features**: Crie entradas mais significativas a partir dos seus dados brutos.
2. **Análise de Erro**: Observe onde o modelo falha. Existe um padrão nos erros?
3. **Seleção de Modelo**: Tente algoritmos diferentes (Lineares, Árvores, etc.).
4. **Ajuste de Hiperparâmetros**: Otimize as configurações do modelo escolhido.
