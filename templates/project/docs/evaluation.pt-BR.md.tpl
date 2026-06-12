# Conceitos de Avaliação

Esta página explica como medir se o seu modelo está funcionando e como garantir que ele seja útil.

## 1. Avaliação (Offline)

A avaliação ocorre **antes** do modelo ir para produção. Você usa dados históricos (conjunto de teste) para ver como o modelo *teria* se comportado.

**Exemplo**:
Imagine um modelo que prevê se uma transação bancária é fraudulenta. Você testa o modelo nos dados do mês passado e vê que ele capturou 90% das fraudes conhecidas.

## 2. O Baseline: Seu Piso de Desempenho

Um **baseline** (linha de base) é a maneira mais simples possível de resolver o problema sem um modelo complexo. Você deve superar o baseline para que seu modelo seja considerado útil.

- **Exemplos**:
    - Prever o valor médio (Regressão).
    - Prever a classe mais frequente (Classificação).
    - Prever que o tempo de amanhã será exatamente igual ao de hoje (Séries Temporais).

**Por que isso importa**: Se sua Rede Neural complexa tem 70% de acurácia, mas uma regra simples "sempre prever Sim" tem 75% de acurácia, seu modelo é pior do que não fazer nada.

## 3. Métricas Técnicas vs. de Negócio

Modelos são treinados com matemática, mas são usados para negócios.

- **Métrica Técnica**: Mede o erro matemático (ex: Erro Quadrático Médio, F1-Score).
- **Métrica de Negócio**: Mede o impacto no mundo real (ex: Dinheiro economizado, redução de cancelamentos, aumento de cliques).

## 4. Thresholds (Limiares): Decidindo quando agir

A maioria dos modelos fornece uma **probabilidade** (ex: "85% de chance de ser spam") em vez de um simples Sim/Não. Um **threshold** é o ponto de corte que você escolhe para tomar uma ação.

- **Threshold Alto (0.9)**: Você só sinaliza como spam se tiver muita certeza. Você perde alguns spams (Menor Recall), mas nunca bloqueia um e-mail real (Maior Precisão).
- **Threshold Baixo (0.1)**: Você sinaliza quase tudo. Você captura todos os spams (Menor Recall), mas muitos e-mails reais são bloqueados incorretamente (Menor Precisão).

## 5. Overfitting e Underfitting

Esses termos descrevem quão bem o modelo aprendeu o "ruído" vs. o "padrão".

- **Underfitting**: O modelo é simples demais. Ele tem um desempenho ruim tanto nos dados de treino quanto nos de teste.
- **Overfitting**: O modelo é complexo demais e "memorizou" os dados de treino. Ele parece perfeito durante o treino, mas falha em novos dados.

## 6. Mapeamento de Métricas por Tipo de Problema

| Família | Tarefa | Métricas Comuns |
|---|---|---|
| **Classificação** | Prever uma categoria | Acurácia, Precisão, Recall, F1-Score, AUC-ROC |
| **Regressão** | Prever um número | MAE, RMSE, R-squared |
| **Séries Temporais** | Prever valores ao longo do tempo | MAE, MAPE, WAPE |
| **Clustering** | Agrupar itens semelhantes | Silhouette Score, Inércia |
| **Visão Computacional** | Encontrar objetos em imagens | mAP, IoU |
| **Bandits** | Tomada de decisão sequencial | Recompensa Acumulada, Regret |
