# Multi-Armed Bandit Lab — referência inicial

Este documento define a base teórica inicial para uma futura seção **Bandit Lab / MAB Lab** no `ml-starter-lab-kit`.

O objetivo é manter o escopo simples o suficiente para ser didático, mas completo o suficiente para não descaracterizar o problema de **Multi-Armed Bandit (MAB)**.

## 1. O que é Multi-Armed Bandit

Multi-Armed Bandit é um problema de decisão sequencial sob incerteza.

A ideia clássica é: existe um conjunto de opções, chamadas de **arms** ou **ações**. A cada rodada, o agente escolhe uma dessas ações, observa uma recompensa daquela ação e usa esse feedback para decidir melhor nas próximas rodadas.

Diferente de aprendizado supervisionado, o agente não recebe um dataset fixo com target conhecido para todos os exemplos. Ele aprende enquanto decide.

Comparação simplificada:

```txt
Aprendizado supervisionado:
dataset fixo -> target conhecido -> treino -> avaliação

Multi-Armed Bandit:
escolha uma ação -> observe reward parcial -> atualize a política -> escolha de novo
```

Essa diferença é central. O MAB não deve ser tratado como apenas mais um algoritmo dentro de `train.py`. Ele representa outro tipo de problema: **tomada de decisão sequencial com feedback parcial**.

## 2. Conceitos principais

### Arm / ação

Um **arm** é uma opção que o agente pode escolher.

Exemplos:

- versão A, B ou C de uma oferta;
- mensagem de marketing diferente;
- botão/CTA diferente;
- estratégia de recomendação diferente;
- produto/oferta diferente em uma simulação.

No primeiro Bandit Lab do projeto, os arms podem ser sintéticos e configuráveis.

### Reward

O **reward** é a recompensa observada após escolher um arm.

No caso mais simples, o reward pode ser binário:

```txt
1 = sucesso
0 = falha
```

Exemplos:

- clicou ou não clicou;
- converteu ou não converteu;
- aceitou ou não aceitou uma oferta;
- obteve ou não obteve resultado positivo.

Para o primeiro lab, a recomendação é usar um **Bernoulli Bandit**, onde cada arm tem uma probabilidade real, escondida, de gerar reward `1`.

### Política

A **política** define como o agente escolhe o próximo arm.

Exemplos de políticas:

- Random Policy;
- Epsilon-Greedy;
- UCB;
- Thompson Sampling.

### Exploração vs exploração

O dilema central do MAB é equilibrar:

- **exploration**: testar arms pouco conhecidos para aprender mais;
- **exploitation**: usar o arm que parece melhor até agora.

Se o agente explora demais, perde recompensa usando opções ruins por muito tempo.

Se explora de menos, pode escolher cedo uma opção aparentemente boa e nunca descobrir que outra era melhor.

### Regret

**Regret** mede quanto o agente deixou de ganhar por não escolher sempre o melhor arm.

Em uma simulação, como sabemos qual arm é realmente melhor, podemos calcular:

```txt
regret acumulado = reward esperado do melhor arm em T rodadas - reward obtido pela política
```

O regret é uma métrica essencial porque mostra o custo de aprender durante a tomada de decisão.

## 3. Por que começar com Bernoulli Bandit

Para o primeiro lab, o melhor cenário é um **stochastic Bernoulli multi-armed bandit**.

Motivos:

- é simples de explicar;
- permite reward binário `0/1`;
- permite configurar arms com probabilidades reais escondidas;
- encaixa naturalmente em UCB e Thompson Sampling;
- permite calcular total reward, arm counts, best arm selection rate e regret;
- não exige dataset real do usuário;
- preserva o ciclo real de MAB: ação, feedback parcial, atualização, próxima ação.

Exemplo de ambiente:

```json
{
  "n_rounds": 1000,
  "arms": [
    {"name": "A", "true_reward_probability": 0.03},
    {"name": "B", "true_reward_probability": 0.05},
    {"name": "C", "true_reward_probability": 0.08}
  ],
  "seed": 42
}
```

O usuário não deve olhar essas probabilidades durante a simulação. Elas representam o ambiente real escondido.

## 4. Políticas recomendadas para o primeiro lab

### 4.1 Random Policy

A Random Policy escolhe arms aleatoriamente.

Ela não aprende de verdade, mas serve como baseline mínimo.

Uso no lab:

- mostrar o comportamento de uma política sem aprendizado;
- comparar reward/regret contra políticas adaptativas.

### 4.2 Epsilon-Greedy

Epsilon-Greedy mistura exploração aleatória com exploração do melhor arm observado até agora.

Com probabilidade `epsilon`, escolhe qualquer arm aleatoriamente.

Com probabilidade `1 - epsilon`, escolhe o arm com maior média observada.

Exemplo:

```txt
epsilon = 0.1
10% das rodadas -> explora aleatoriamente
90% das rodadas -> escolhe o melhor arm conhecido
```

Uso no lab:

- baseline simples de política adaptativa;
- bom para explicar o trade-off exploration/exploitation.

Limitação:

- explora de forma fixa, mesmo quando já tem bastante evidência;
- não diferencia muito bem arms incertos de arms ruins.

### 4.3 UCB / UCB1

UCB significa **Upper Confidence Bound**.

A ideia é escolher de forma otimista: cada arm recebe uma pontuação composta por:

```txt
média observada + bônus de incerteza
```

Uma forma comum do UCB1 é:

```txt
ucb_i(t) = mean_i + sqrt(2 * ln(t) / n_i)
```

Onde:

- `mean_i` é a média de rewards observada do arm `i`;
- `t` é a rodada atual;
- `n_i` é o número de vezes que o arm `i` foi escolhido.

Interpretação:

- arms com média alta são favorecidos;
- arms pouco testados recebem bônus maior;
- conforme um arm é testado mais vezes, o bônus diminui;
- com o tempo, a política tende a concentrar escolhas nos arms melhores.

No lab, UCB deve:

1. escolher cada arm pelo menos uma vez;
2. calcular média e contagem por arm;
3. calcular o bônus de incerteza;
4. escolher o arm com maior `mean + bonus`;
5. atualizar estatísticas após observar o reward.

### 4.4 Thompson Sampling

Thompson Sampling é uma política bayesiana.

Em vez de usar uma média fixa ou um bônus explícito, ela mantém uma crença probabilística sobre cada arm.

No caso Bernoulli, cada arm pode ter uma distribuição Beta:

```txt
Beta(alpha, beta)
```

Interpretação:

- `alpha` aumenta quando o arm gera sucesso (`reward = 1`);
- `beta` aumenta quando o arm gera falha (`reward = 0`);
- no começo, todos podem iniciar com `Beta(1, 1)`;
- a cada rodada, a política sorteia uma amostra da distribuição de cada arm;
- escolhe o arm com maior amostra sorteada.

Ciclo:

```txt
para cada rodada:
  para cada arm:
    sorteie uma probabilidade da posterior Beta(alpha, beta)
  escolha o arm com maior valor sorteado
  observe reward
  atualize alpha/beta do arm escolhido
```

Por que isso funciona bem didaticamente:

- arms com bons resultados tendem a sortear valores maiores;
- arms incertos ainda têm chance de serem explorados;
- a exploração surge naturalmente da incerteza da distribuição.

## 5. Métricas obrigatórias do Bandit Lab

O lab deve gerar métricas suficientes para comparar políticas.

Mínimo recomendado:

```txt
- total_reward
- cumulative_regret
- best_arm_selection_rate
- arm_counts
- average_reward
- history por rodada
```

### total_reward

Soma de todos os rewards obtidos pela política.

### cumulative_regret

Diferença acumulada entre o reward esperado do melhor arm e o resultado da política.

### best_arm_selection_rate

Percentual de rodadas em que a política escolheu o arm realmente ótimo.

### arm_counts

Quantidade de vezes que cada arm foi escolhido.

Ajuda a enxergar se a política:

- explorou demais;
- concentrou cedo demais;
- convergiu para o melhor arm;
- ficou presa em um arm ruim.

### history por rodada

O histórico por rodada é importante para visualização e aprendizado.

Campos recomendados:

```txt
round
policy
selected_arm
reward
cumulative_reward
cumulative_regret
arm_estimates
```

## 6. Artefatos propostos

O Bandit Lab deve gerar artefatos próprios, separados de `train.py` e `evaluate.py`.

```txt
configs/bandit_config.json
configs/bandit_results.json
reports/bandit-results.md
reports/bandit-history.csv
```

### configs/bandit_config.json

Configuração do ambiente e das políticas.

### configs/bandit_results.json

Resumo estruturado para consumo por testes, workspace ou futuras visualizações.

### reports/bandit-results.md

Relatório didático para o usuário.

Deve explicar:

- o cenário simulado;
- arms existentes;
- melhor arm real;
- políticas comparadas;
- resultados;
- interpretação de reward e regret;
- diferença entre UCB e Thompson Sampling.

### reports/bandit-history.csv

Histórico por rodada, útil para gráficos.

## 7. Como encaixar no projeto

O Bandit Lab deve ser uma seção avançada do Guided Learning, não uma alteração do treino supervisionado.

Comando sugerido:

```bash
python -m <package>.lab bandit
```

Estrutura sugerida no workspace:

```txt
Learning Workspace
├── Dataset Overview
├── Guided EDA
├── Learning Notes
├── Model Suggestions
├── Baseline Lab
├── Bandit Lab
└── Train & Evaluate
```

Não usar:

```bash
python -m <package>.lab train-bandit
```

Motivo: no MAB, o aprendizado acontece durante a sequência de decisões, não em uma etapa de treino supervisionado convencional.

## 8. Escopo do primeiro Bandit Lab

O primeiro escopo deve ser simples, mas completo:

```txt
- simulação sintética estacionária;
- rewards Bernoulli;
- arms configuráveis;
- Random Policy;
- Epsilon-Greedy;
- UCB1;
- Thompson Sampling;
- comparação por reward e regret;
- relatório Markdown;
- JSON estruturado;
- histórico CSV;
- seção no Streamlit Guided Learning.
```

Fora do primeiro escopo:

```txt
- contextual bandits;
- non-stationary bandits;
- delayed rewards;
- offline policy evaluation;
- dataset real com logs históricos;
- integração com train/evaluate;
- uso de LLM;
- dependências pesadas.
```

Esses temas são importantes, mas devem vir depois que o usuário entender o MAB básico.

## 9. Critério de qualidade para implementação

A implementação não deve apenas imprimir uma tabela final.

Ela precisa preservar o ciclo real de MAB:

```txt
1. inicializar ambiente
2. inicializar política
3. escolher arm
4. observar reward somente do arm escolhido
5. atualizar estado da política
6. registrar histórico
7. repetir por T rodadas
8. comparar políticas
9. calcular regret
10. gerar relatório
```

Se faltar feedback parcial, atualização por rodada ou regret, o lab fica descaracterizado.

## 10. Referências

- Slivkins, Aleksandrs. **Introduction to Multi-Armed Bandits**. arXiv:1904.07272, 2019. https://arxiv.org/abs/1904.07272
- Bubeck, Sébastien; Cesa-Bianchi, Nicolò. **Regret Analysis of Stochastic and Nonstochastic Multi-armed Bandit Problems**. arXiv:1204.5721, 2012. https://arxiv.org/abs/1204.5721
- Agrawal, Shipra; Goyal, Navin. **Analysis of Thompson Sampling for the Multi-armed Bandit Problem**. arXiv:1111.1797, 2011. https://arxiv.org/abs/1111.1797
- Auer, Peter; Cesa-Bianchi, Nicolò; Fischer, Paul. **Finite-time Analysis of the Multiarmed Bandit Problem**. Machine Learning, 2002.
- Sutton, Richard S.; Barto, Andrew G. **Reinforcement Learning: An Introduction**. MIT Press, 2nd edition, 2018.
