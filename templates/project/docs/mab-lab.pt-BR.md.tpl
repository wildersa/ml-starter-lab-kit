# Multi-Armed Bandit Lab — Referência

O Multi-Armed Bandit (MAB) é um problema de tomada de decisão sequencial sob incerteza.

## 1. O que é Multi-Armed Bandit

A ideia clássica é: existe um conjunto de opções, chamadas de **arms** (braços) ou **ações**. A cada rodada, o agente escolhe uma dessas ações, observa uma recompensa (reward) dessa ação e usa esse feedback para tomar decisões melhores nas rodadas futuras.

Diferente do aprendizado supervisionado, o agente não recebe um dataset fixo com um alvo conhecido para todos os exemplos. Ele aprende enquanto decide.

Comparação simplificada:

```txt
Aprendizado Supervisionado:
dataset fixo -> alvo conhecido -> treinamento -> avaliação

Multi-Armed Bandit:
escolha uma ação -> observe recompensa parcial -> atualize a política -> escolha de novo
```

Essa diferença é central. O MAB representa outro tipo de problema: **tomada de decisão sequencial com feedback parcial**.

## 2. Conceitos Principais

### Arm / Ação
Um **arm** é uma opção que o agente pode escolher.
Exemplos: versões diferentes de uma oferta, mensagens de marketing distintas ou recomendações de produtos variadas.

### Reward (Recompensa)
O **reward** é o feedback observado após a escolha de um arm. No caso mais simples, é binário: 1 para sucesso, 0 para falha.

### Política
A **política** define como o agente escolhe o próximo arm.
Exemplos: Random, Epsilon-Greedy, UCB, Thompson Sampling.

### Exploração vs. Explotação (Exploration vs. Exploitation)
O dilema central do MAB é equilibrar:
- **Exploração**: testar arms menos conhecidos para aprender mais.
- **Explotação**: usar o arm que parece melhor até agora.

### Regret (Arrependimento)
O **Regret** mede o quanto o agente deixou de ganhar por não escolher sempre o melhor arm. Em uma simulação, calculamos como a diferença entre a melhor recompensa possível e a recompensa obtida pela política.

## 3. Políticas Recomendadas

### Epsilon-Greedy
Mistura exploração aleatória com explotação. Com probabilidade `epsilon`, ele explora; caso contrário, escolhe o melhor arm conhecido.

### UCB1 (Upper Confidence Bound)
Escolhe arms de forma otimista, adicionando um bônus de incerteza à média observada. Arms menos testados recebem um bônus maior.

### Thompson Sampling
Uma abordagem Bayesiana que mantém uma distribuição de probabilidade para cada arm e extrai amostras dela para tomar decisões. Ele lida com a exploração naturalmente através da incerteza.
