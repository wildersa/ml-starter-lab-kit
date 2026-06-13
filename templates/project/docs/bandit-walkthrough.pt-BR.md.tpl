# Passo a Passo do Bandit — De Aprendizado Supervisionado para Decisões Adaptativas

Você tem um conjunto de dados e quer usá-lo para um experimento de Multi-Armed Bandit. Este guia ajudará você a mapear conceitos tradicionais de aprendizado supervisionado para o mundo das decisões adaptativas.

## 1. O Mapeamento Principal

No Aprendizado Supervisionado, você geralmente tem um conjunto de dados fixo onde cada linha é um exemplo independente. No Bandit Lab, tratamos cada decisão como um **evento** (ou impressão).

| Conceito Supervisionado | Conceito Bandit | Descrição |
| :--- | :--- | :--- |
| Features | **Contexto** | Informação disponível *antes* de tomar uma decisão (ex: perfil do usuário, dispositivo, horário). |
| - | **Braço (Arm) / Ação** | A decisão que você toma (ex: qual anúncio mostrar, qual preço definir). |
| Target (y) | **Recompensa (Reward)** | O resultado que você deseja maximizar, observado *após* tomar uma ação. |
| Modelo | **Política (Policy)** | A estratégia que escolhe o melhor braço baseado no conhecimento atual. |
| Avaliação (Conjunto de Teste) | **Simulação** | Reencenar eventos para ver como uma política teria performado comparada a uma linha de base (baseline). |

## 2. A Armadilha do "Target Supervisionado" ⚠️

**AVISO CRÍTICO:** Você não pode simplesmente usar o `y` (target) de um dataset supervisionado como sua recompensa de Bandit sem um mapeamento claro de "Ação".

No Aprendizado Supervisionado, o `y` é geralmente o que aconteceu independentemente do seu modelo. Em um experimento de Bandit, a **Recompensa** é o que acontece *porque* você escolheu um **Braço** específico.

Para rodar um Bandit Lab válido, você precisa de:
1. **Impressões/Eventos**: Um fluxo de oportunidades para fazer uma escolha.
2. **Ações**: Um conjunto finito de opções que você poderia ter escolhido.
3. **Recompensas**: Uma métrica (binária ou contínua) que mede o sucesso para uma ação específica.

## 3. Conceitos Detalhados do Bandit

### Contexto
Isso é tudo o que você sabe sobre a situação antes de escolher um braço.
*Exemplo*: O usuário é de "São Paulo", usando "Mobile", às "10:00 AM".

### Braço / Ação
Uma das escolhas discretas disponíveis para a política.
*Exemplo*: Mostrar "Cupom de Desconto A" vs "Cupom de Desconto B".

### Recompensa (Reward)
O feedback do ambiente.
*Exemplo*: O usuário clicou? (1 para Sim, 0 para Não).

### Política
O "cérebro" que decide qual braço puxar. Ele equilibra **Exploração** (tentar coisas novas) e **Explotação** (usar o que funciona).

### Baseline (Linha de Base)
Uma política simples usada para comparação, geralmente uma política **Aleatória** ou uma fixa como "Sempre escolher o Braço 1".

### Regret e Lift
* **Regret (Arrependimento)**: A diferença entre a melhor recompensa possível e o que sua política realmente obteve. Queremos minimizar isso.
* **Lift**: A melhoria percentual da sua política em relação à linha de base.

### Recompensa Atrasada (Delayed Reward)
Em muitos cenários do mundo real, a recompensa não é instantânea.
*Exemplo*: Você mostra um anúncio agora, mas a compra (recompensa) acontece 3 dias depois. Esse atraso torna o aprendizado mais difícil.

### Drift (Deriva)
Assim como no aprendizado supervisionado, o ambiente muda. O "Melhor Braço" hoje pode ser o "Pior Braço" no mês que vem devido a tendências sazonais ou mudanças no comportamento do usuário.

## 4. Como usar isso no Bandit Lab

Quando você executa `python -m {{PACKAGE_NAME}}.lab bandit`, o simulador usa sua configuração para testar diferentes políticas entre si. Ele calcula a **Recompensa Acumulada** e o **Regret** ao longo do tempo, ajudando você a ver qual política aprende mais rápido.
