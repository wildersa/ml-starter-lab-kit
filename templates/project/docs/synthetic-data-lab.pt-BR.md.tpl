# Synthetic Data Lab (Laboratório de Dados Sintéticos)

Este laboratório fornece um mecanismo configurável para gerar conjuntos de dados sintéticos determinísticos para vários cenários de Machine Learning.

## Por que usar Dados Sintéticos?

Dados sintéticos são uma ferramenta excelente para:
- **Cenários educacionais**: Aprender como diferentes algoritmos respondem a padrões de dados controlados.
- **Testes de unidade**: Garantir que seu pipeline lide corretamente com formatos ou distribuições de dados específicos.
- **Prototipagem**: Construir a estrutura do seu projeto antes que os dados reais estejam disponíveis.

**Importante**: Dados sintéticos são para estudo e teste. Eles não provam o desempenho no mundo real.

## Como usar

1.  Revise e edite `configs/synthetic_data.json` para escolher um cenário e ajustar seus parâmetros.
2.  Execute o comando de geração:
    ```bash
    python -m {{PACKAGE_NAME}}.lab synthetic
    ```
3.  Os artefatos gerados serão armazenados em `data/synthetic/`.
4.  Um resumo da geração está disponível em `reports/synthetic-data-summary.md`.

## Cenários Disponíveis

### 1. Classificação (Classification)
Gera um dataset com features tabulares e um alvo (target) binário.
- **Configurável**: Número de amostras, features, features informativas e desbalanceamento de classes.

### 2. Regressão (Regression)
Gera um dataset com features tabulares e um alvo numérico.
- **Configurável**: Nível de ruído e número de features.

### 3. Agrupamento (Clustering)
Gera segmentos não rotulados estilo "perfil de cliente".
- **Configurável**: Número de clusters (centros) e features.

### 4. Séries Temporais (Time Series)
Gera um dataset indexado por data com tendência, sazonalidade e ruído.
- **Configurável**: Inclinação da tendência, período sazonal e flags opcionais de promoção/evento.

### 5. Multi-Armed Bandit (Simples)
Gera um histórico de interações Bernoulli.
- **Estrutura**: `round`, `arm`, `reward`.
- Adequado para experimentação básica de MAB.

### 6. Multi-Armed Bandit (Eventos Contextuais)
Gera eventos com contexto (features), ações (braços) e recompensas.
- **Estrutura**: Colunas de contexto, coluna de ação, coluna de recompensa.
- **Avançado**: Suporta `delay_steps` opcionais para simular recompensas atrasadas.

## Reprodutibilidade

O Synthetic Data Lab é **determinístico**. Desde que você use a mesma semente (`seed`) na configuração, os dados gerados serão idênticos em diferentes execuções.

## Relação com Tipos de Aprendizado

- **Aprendizado Supervisionado**: Use Classificação ou Regressão para testar loops de treino e avaliação.
- **Aprendizado Não Supervisionado**: Use Agrupamento para testar segmentação e redução de dimensionalidade.
- **Séries Temporais**: Use o cenário de Time Series para testar modelos de previsão como ARIMA, Prophet ou LSTMs.
- **Decisões Adaptativas (Bandits)**: Eventos sintéticos permitem simular ambientes onde as decisões impactam interações futuras, ao contrário de datasets supervisionados estáticos.

## Saiba mais

- **Fonte Prática**: scikit-learn [Dataset Generation Documentation](https://scikit-learn.org/stable/datasets/sample_generators.html).
- **Avaliação**: scikit-learn [Model Evaluation Guide](https://scikit-learn.org/stable/modules/model_evaluation.html).

**Limitação**: Dados sintéticos são úteis para testes de pipeline e fins educacionais, mas não capturam a complexidade e o ruído de ambientes de produção reais. Sempre valide seus modelos com dados reais antes do deploy.
