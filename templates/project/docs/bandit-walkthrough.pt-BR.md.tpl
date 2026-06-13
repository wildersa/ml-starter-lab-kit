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

## 5. Exemplo guiado — Dataset de marketing para Bandit Lab

Imagine que você tem um **Dataset de Marketing Bancário** usado para Aprendizado Supervisionado.

**Colunas Originais Supervisionadas:**
* `age` (idade), `job` (profissão), `balance` (saldo), `housing` (moradia), `loan` (empréstimo), `campaign` (Features)
* `y` (Alvo: assinou o produto? sim/não)

Para transformar isso em um **Bandit Lab**, você precisa fazer a ponte:

### Passo 1: Defina o Contexto
Todas as features do dataset original tornam-se o seu **Contexto**.
* `age`, `job`, `balance`, etc.

### Passo 2: Defina os Braços / Ações
Você precisa decidir o que está testando.
* **Braço A**: Enviar um SMS genérico.
* **Braço B**: Ligar para o cliente com uma oferta personalizada.
* **Braço C**: Enviar um e-mail com um cupom de desconto.

### Passo 3: Defina a Recompensa (Reward)
Aqui é onde mora a armadilha do "Target Supervisionado". O `y` original (assinou) é o resultado de uma ação de marketing *anterior*. Em um Bandit Lab, queremos saber se o usuário assinou **por causa** do Braço que escolhemos (A, B ou C).

* **Recompensa Imediata**: O usuário clicou no link do SMS? (Binário: 1/0)
* **Recompensa Atrasada**: O usuário assinou o contrato dentro de 7 dias?

### Passo 4: Compare com o Baseline
Como saber se sua política é boa?
* **Baseline Aleatório**: Escolhe aleatoriamente A, B ou C para cada cliente.
* **Baseline Fixo**: Sempre envia SMS (Braço A) para todos.

### Passo 5: A Tabela de Simulação
Durante a simulação, o Bandit Lab gera um histórico parecido com este:

| impression_id | context_age | context_balance | arm_chosen | reward | reward_delay_days |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 101 | 35 | 2000 | Braço B | 1 | 2 |
| 102 | 42 | 500 | Braço A | 0 | - |
| 103 | 28 | 1200 | Braço C | 1 | 0 |

**Conclusão**: No Bandit Lab, o **target original** (`y`) não é suficiente. Você deve modelar a interação (Ação -> Recompensa) para realmente otimizar suas decisões de negócio.
