# Guia de Avaliação — {{PROJECT_NAME}}

Este guia explica como medir os resultados do seu projeto de `{{TASK}}`.

## Fluxo de Avaliação

Para confiar no seu modelo, você deve seguir este fluxo padrão:

1.  **Divisão do Dataset**: Divida seus dados em conjuntos de Treino e Teste. Nunca avalie no mesmo dado usado para treinar.
2.  **Alvo (Target)**: O valor real que você deseja prever (ground truth).
3.  **Predição**: O valor produzido pelo seu modelo.
4.  **Baseline**: Uma regra simples (como "sempre prever a média") para comparação. Se seu modelo não for melhor que o baseline, ele não está pronto.
5.  **Métrica**: Uma fórmula matemática que resume o quão perto as predições estão dos alvos.
6.  **Interpretação**: Entender o que a métrica significa para o seu negócio ou problema.
7.  **Próximo Experimento**: Usar os resultados para decidir como melhorar (ex: adicionar features ou mudar o modelo).

{% if TASK == "supervised" %}
{% if DEMO_SUBTYPE == "classification" %}
## Avaliação de Classificação

Como você está prevendo categorias, foque nestes conceitos:

### Matriz de Confusão
A base da classificação. Ela mostra:
- **Verdadeiros Positivos (VP)**: Positivo previsto corretamente.
- **Verdadeiros Negativos (VN)**: Negativo previsto corretamente.
- **Falsos Positivos (FP)**: Positivo previsto incorretamente (Alarme Falso).
- **Falsos Negativos (FN)**: Negativo previsto incorretamente (Oportunidade Perdida).

### Métricas Chave
- **Precisão**: De todos os positivos previstos, quantos estavam certos? Use quando o **Falso Positivo** for caro.
- **Recall**: De todos os positivos reais, quantos encontramos? Use quando o **Falso Negativo** for caro.
- **F1-Score**: O equilíbrio entre Precisão e Recall.

### Limiares (Thresholds) e Custos
A maioria dos modelos gera uma probabilidade (0.0 a 1.0). Por padrão, usamos **0.5** como limiar.
- Se um **Falso Positivo** for muito caro (ex: bloquear um bom cliente), aumente o limiar (ex: para 0.8).
- Se um **Falso Negativo** for muito caro (ex: perder um diagnóstico), diminua o limiar (ex: para 0.2).
{% else %}
## Avaliação de Regressão

Como você está prevendo números, foque nestas métricas:

- **MAE (Erro Médio Absoluto)**: O erro médio nas mesmas unidades do seu alvo. Muito fácil de interpretar.
- **RMSE (Raiz do Erro Quadrático Médio)**: Similar ao MAE, mas penaliza erros grandes com mais força.
- **MAPE (Erro Médio Percentual Absoluto)**: Mostra o erro como uma porcentagem (ex: "o modelo erra 10% em média").

**Evite Acurácia**: Não use "acurácia" para regressão. Uma predição de 95 quando o alvo é 100 está "errada" em termos de acurácia, mas "perto" em termos de regressão.
{% endif %}
{% endif %}

{% if TASK == "timeseries" %}
## Avaliação de Séries Temporais

Avaliar séries temporais requer cuidado especial porque a ordem importa.

- **Backtesting**: Em vez de uma divisão aleatória, use um ponto de corte no tempo. Treine no passado, teste no "futuro".
- **Horizonte de Previsão**: Meça como o desempenho cai à medida que você tenta prever mais longe no futuro.
- **Métricas**: Use MAE, RMSE ou MAPE, similar à regressão, mas calcule-as por passo de tempo.
{% endif %}

{% if TASK == "unsupervised" %}
## Avaliação Não Supervisionada

Como não há um "alvo", medimos o quão bem o modelo encontra padrões.

- **Agrupamento (ex: K-Means)**: Use o **Silhouette Score** para ver quão bem separados estão seus grupos.
- **Consistência Interna**: Os itens no mesmo grupo realmente parecem similares para um especialista humano?
- **Estabilidade**: Se você rodar o modelo novamente com dados ligeiramente diferentes, os grupos permanecem os mesmos?
{% endif %}

{% if TASK == "vision" %}
## Avaliação de Visão Computacional

- **Classificação de Imagem**: Usa as mesmas métricas de Classificação (Precisão, Recall, F1).
- **Detecção de Objetos**: Usa **mAP (mean Average Precision)**, que considera o quão bem a "caixa" sobrepõe o objeto.
{% endif %}

{% if TASK == "bandit" or GENERATE_BANDIT == "true" %}
## Avaliação de Multi-Armed Bandit

Bandits aprendem enquanto executam, então medimos a "eficiência do aprendizado":

- **Recompensa Acumulada**: A soma total de recompensas obtidas ao longo do tempo.
- **Regret (Arrependimento)**: A diferença entre a recompensa que você *poderia* ter obtido com o melhor braço e o que você realmente obteve. Quanto menor, melhor.
- **Seleção de Braços**: Estamos convergindo para a melhor opção ao longo de muitas rodadas?
{% endif %}

{% if TASK == "generic" %}
## Avaliação Genérica

Defina seus critérios de sucesso com base no seu objetivo específico.
1. Identifique seu alvo.
2. Escolha uma métrica que penalize o comportamento "errado" para o seu caso de uso.
3. Compare com um baseline de "senso comum".
{% endif %}

## Referências
Para mais detalhes sobre métricas específicas, visite a [Documentação de Métricas](../../docs/metrics/README.pt-BR.md).
