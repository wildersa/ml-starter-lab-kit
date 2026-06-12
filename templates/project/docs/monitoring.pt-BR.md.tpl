# Monitoramento e Drift

Esta página explica como garantir que seu modelo continue útil após ser implantado.

## 1. Monitoramento (Online)

O monitoramento ocorre **depois** que o modelo está em produção. Você acompanha como ele *está* se comportando com dados reais e ao vivo.

**Exemplo**:
Imagine um modelo que prevê se uma transação bancária é fraudulenta. Hoje, você percebe que o modelo está sinalizando apenas 50% das transações como fraude em comparação com ontem. Algo pode estar errado com os dados em tempo real.

## 2. Drift (Deriva) e Retreinamento

O desempenho de um modelo geralmente piora com o tempo porque o mundo muda. Isso é chamado de **Drift**.

- **Data Drift**: A distribuição dos dados de entrada muda. *Exemplo: Seu modelo foi treinado com dados de usuários de iPhone, mas agora a maioria dos seus usuários está no Android.*
- **Concept Drift**: A relação entre a entrada e a saída muda. *Exemplo: Antes de uma pandemia, as pessoas compravam seguro viagem; depois que ela começa, o comportamento de compra muda completamente.*
- **Performance Drift**: A acurácia do modelo começa a cair no mundo real em comparação com o que foi visto no treino.

**Gatilho de Retreinamento**: Você deve retreinar seu modelo quando detectar um drift significativo ou quando o desempenho cair abaixo de um limite predefinido.

## 3. Sinais Específicos por Tarefa

Diferentes tipos de tarefas de ML exigem a observação de sinais diferentes:

- **Classificação**: Observe mudanças na distribuição das classes previstas e nos scores de confiança. Você está subitamente prevendo muito mais de uma classe específica?
- **Regressão**: Observe o aumento no erro de previsão (ex: MAE, RMSE) e mudanças na faixa de valores previstos.
- **Séries Temporais**: Observe mudanças na sazonalidade, tendências ou outliers repentinos que o modelo não viu antes.
- **Clustering (Agrupamento)**: Observe a "compacidade" dos clusters. Novos pontos de dados estão caindo muito longe dos centros dos clusters existentes?
- **Visão Computacional**: Observe mudanças na qualidade da imagem, condições de iluminação ou novos tipos de objetos.
- **Bandit/Adaptativo**: Observe o "Regret" (Arrependimento) e a "Taxa de Seleção do Melhor Braço". Se uma estratégia anteriormente vencedora começar a falhar, o ambiente pode ter mudado.

## 4. Como detectar Drift?

Uma maneira simples de começar é comparar os **Dados de Treino** (seu baseline) com os **Dados de Operação** (novos dados).

1. **Verifique o Schema**: Uma nova categoria apareceu? Uma coluna está ausente ou cheia de nulos?
2. **Compare Distribuições**: Use histogramas ou estatísticas (Média, Desvio Padrão) para ver se os novos dados "se parecem" com os dados de treino.
3. **Monitore Previsões**: Se você ainda não tem os "rótulos reais" (labels), rastrear a distribuição de suas previsões é um ótimo proxy para detectar drift.
