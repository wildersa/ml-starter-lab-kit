# Avaliação e Monitoramento

Avaliação e Monitoramento são dois lados da mesma moeda: um acontece antes do modelo ser usado (offline) e o outro acontece enquanto o modelo está em uso (online).

## Avaliação (Offline)

A avaliação ocorre durante a fase de desenvolvimento. Ela responde: "Este modelo é bom o suficiente para ser implantado?"

- **Objetivo**: Comparar diferentes modelos ou versões.
- **Dados**: Conjuntos de dados estáticos (conjuntos de validação e teste).
- **Verificação Principal**: Garantir que não haja [Vazamento de Dados (Data Leakage)](../common-mistakes/data-leakage.pt-BR.md).

## Monitoramento (Online)

O monitoramento acontece após o modelo ser implantado. Ele responde: "O modelo ainda está funcionando conforme o esperado no mundo real?"

- **Objetivo**: Detectar quando o modelo começa a falhar.
- **Dados**: Dados de produção em tempo real.
- **Problemas Comuns**:
    - **Drift**: Quando a relação entre entradas e saídas muda ao longo do tempo.
    - **Latência**: Quanto tempo o modelo leva para retornar uma previsão.
    - **Integridade dos Dados**: Quando o formato dos dados de produção difere dos dados de treinamento.

---

### Regra Prática

Nunca confie em um modelo baseado apenas em suas métricas de treinamento. Sempre use uma [Estratégia de Avaliação](../metrics/README.pt-BR.md) adequada e fique de olho no seu [Monitoramento](../architectures/layers.pt-BR.md).
