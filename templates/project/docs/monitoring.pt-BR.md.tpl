# Monitoramento e Drift

Esta página explica como garantir que seu modelo continue útil após ser implantado.

## 1. Monitoramento (Online)

O monitoramento ocorre **depois** que o modelo está em produção. Você acompanha como ele *está* se comportando com dados reais e ao vivo.

**Exemplo**:
Imagine um modelo que prevê se uma transação bancária é fraudulenta. Hoje, você percebe que o modelo está sinalizando apenas 50% das transações como fraude em comparação com ontem. Algo pode estar errado com os dados em tempo real.

## 2. Drift (Deriva) e Retreinamento

O desempenho de um modelo geralmente piora com o tempo porque o mundo muda. Isso é chamado de **Drift**.

- **Data Drift**: Os dados de entrada mudam. *Exemplo: Seu modelo foi treinado com dados de usuários de iPhone, mas agora a maioria dos seus usuários está no Android.*
- **Concept Drift**: A relação entre a entrada e a saída muda. *Exemplo: Antes de uma pandemia, as pessoas compravam seguro viagem; depois que ela começa, o comportamento de compra muda completamente.*
- **Performance Drift**: A acurácia do modelo começa a cair no mundo real.

**Gatilho de Retreinamento**: Você deve retreinar seu modelo quando detectar um drift significativo ou quando o desempenho cair abaixo de um limite predefinido.
