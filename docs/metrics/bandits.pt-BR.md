# Métricas de Bandit

Os Multi-Armed Bandits (MAB) avaliam o equilíbrio entre **Exploração** (testar opções para aprender) e **Explotação/Aproveitamento** (usar a melhor opção conhecida para maximizar recompensa).

## Recompensa (Reward)

- **O que responde**: Qual é o resultado imediato de uma ação?
- **Quando usar**: Para definir o sucesso (ex: clique, compra, usuário satisfeito).
- **Exemplo**: Uma recompensa de 1 para um clique e 0 para nenhum clique.

## Recompensa Acumulada (Cumulative Reward)

- **O que responde**: Quanto valor total a política gerou ao longo do tempo?
- **Quando usar**: Para comparar o desempenho geral de diferentes estratégias.
- **Exemplo**: A Estratégia A obteve 1500 cliques totais, enquanto a Estratégia B obteve 1200.

## Regret (Arrependimento)

- **O que responde**: Quanta recompensa eu perdi por não escolher o melhor braço (arm) possível todas as vezes?
- **Quando usar**: Para entender o custo do aprendizado. Um regret menor significa que a política encontrou a melhor opção rapidamente.
- **Armadilha comum**: O regret zero é impossível durante o aprendizado, mas uma boa política mostra uma curva de regret acumulado que se estabiliza (platô).

## Lift vs. Baseline

- **O que responde**: O quanto o bandit é melhor do que uma escolha aleatória ou uma regra de negócio estática?
- **Quando usar**: Para justificar o uso de um sistema de bandit em vez de uma abordagem mais simples.
- **Exemplo**: A política de Thompson Sampling alcançou um lift de 15% na conversão em comparação com o baseline aleatório.

## Distribuição de Braços (Arm Distribution)

- **O que responde**: Quais opções (braços) o modelo está escolhendo mais?
- **Quando usar**: Para detectar se o modelo está preso em uma opção ou se está explorando de forma justa.

## Custo de Exploração e Drift de Comportamento

- **Custo de Exploração**: A perda temporária de recompensa incorrida ao testar opções incertas.
- **Drift de Comportamento do Usuário**: Bandits são sensíveis a mudanças nas preferências do usuário ao longo do tempo. Se sua taxa de recompensa cair repentinamente, seus usuários podem ter mudado de comportamento, exigindo que o modelo "reaprenda".

---

### Próximos Passos

Sempre verifique o [Checklist Antes da Avaliação](../checklists/before-evaluation.pt-BR.md) e monitore o desempenho do bandit ao longo do tempo, pois seu ambiente é dinâmico.
- Veja o conceito de [Avaliação e Monitoramento](../concepts/evaluation-and-monitoring.pt-BR.md) para o ciclo completo.
