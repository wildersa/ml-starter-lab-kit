# Avaliação e Monitoramento

Esta página explica como medir se o seu modelo está funcionando e como garantir que ele continue útil após ser implantado.

## 1. Avaliação vs. Monitoramento

Iniciantes frequentemente confundem esses dois conceitos, mas eles ocorrem em estágios diferentes do ciclo de vida de ML.

- **Avaliação** (Offline): Ocorre **antes** do modelo ir para produção. Você usa dados históricos (conjunto de teste) para ver como o modelo *teria* se comportado.
- **Monitoramento** (Online): Ocorre **depois** que o modelo está em produção. Você acompanha como ele *está* se comportando com dados reais e ao vivo.

**Exemplo**:
Imagine um modelo que prevê se uma transação bancária é fraudulenta.
- **Avaliação**: Você testa o modelo nos dados do mês passado e vê que ele capturou 90% das fraudes conhecidas.
- **Monitoramento**: Hoje, você percebe que o modelo está sinalizando apenas 50% das transações como fraude em comparação com ontem. Algo pode estar errado com os dados em tempo real.

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

**Exemplo Prático**:
Um modelo prevê falha em motores.
- **Técnica**: 95% de Recall (ele captura 95% das falhas).
- **Negócio**: R$ 10.000 economizados por mês em reparos de emergência evitados.

## 4. Thresholds (Limiares): Decidindo quando agir

A maioria dos modelos fornece uma **probabilidade** (ex: "85% de chance de ser spam") em vez de um simples Sim/Não. Um **threshold** é o ponto de corte que você escolhe para tomar uma ação.

- **Threshold Alto (0.9)**: Você só sinaliza como spam se tiver muita certeza. Você perde alguns spams (Menor Recall), mas nunca bloqueia um e-mail real (Maior Precisão).
- **Threshold Baixo (0.1)**: Você sinaliza quase tudo. Você captura todos os spams (Maior Recall), mas muitos e-mails reais são bloqueados incorretamente (Menor Precisão).

## 5. Overfitting e Underfitting

Esses termos descrevem quão bem o modelo aprendeu o "ruído" vs. o "padrão".

- **Underfitting**: O modelo é simples demais. Ele tem um desempenho ruim tanto nos dados de treino quanto nos de teste. *Exemplo: Tentar prever preços de casas usando apenas a cor da porta da frente.*
- **Overfitting**: O modelo é complexo demais e "memorizou" os dados de treino. Ele parece perfeito durante o treino, mas falha em novos dados. *Exemplo: Um aluno que memoriza as respostas de um simulado específico, mas reprova na prova real porque as perguntas mudaram ligeiramente.*

## 6. Drift (Deriva) e Retreinamento

O desempenho de um modelo geralmente piora com o tempo porque o mundo muda. Isso é chamado de **Drift**.

- **Data Drift**: Os dados de entrada mudam. *Exemplo: Seu modelo foi treinado com dados de usuários de iPhone, mas agora a maioria dos seus usuários está no Android.*
- **Concept Drift**: A relação entre a entrada e a saída muda. *Exemplo: Antes de uma pandemia, as pessoas compravam seguro viagem; depois que ela começa, o comportamento de compra muda completamente.*
- **Performance Drift**: A acurácia do modelo começa a cair no mundo real.

**Gatilho de Retreinamento**: Você deve retreinar seu modelo quando detectar um drift significativo ou quando o desempenho cair abaixo de um limite predefinido.

## 7. Mapeamento de Métricas por Tipo de Problema

| Família | Tarefa | Métricas Comuns |
|---|---|---|
| **Classificação** | Prever uma categoria (Spam/Não Spam) | Acurácia, Precisão, Recall, F1-Score, AUC-ROC |
| **Regressão** | Prever um número (Preço, Temperatura) | MAE, RMSE, R-squared |
| **Séries Temporais** | Prever valores ao longo do tempo | MAE, MAPE, WAPE |
| **Clustering** | Agrupar itens semelhantes | Silhouette Score, Inércia |
| **Visão Computacional** | Encontrar objetos em imagens | mAP (Mean Average Precision), IoU (Intersection over Union) |
| **Bandits** | Tomada de decisão sequencial | Recompensa Acumulada, Regret |
