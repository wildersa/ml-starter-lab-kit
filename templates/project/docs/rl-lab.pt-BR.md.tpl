# 🤖 Guia do Laboratório de Aprendizado por Reforço (RL) e Extensão

Bem-vindo ao **Laboratório de Aprendizado por Reforço (RL)**. Esta base fornece um loop de interação explícito e passo a passo e um workspace visual para conceitos de RL sem esconder o funcionamento interno dos algoritmos em uma chamada opaca.

---

## 🎯 Arquitetura e Contratos Base

A fundação de RL é construída sobre abstrações Python em `src/{{PACKAGE_NAME}}/rl.py`:

### 1. Estruturas `AgentTransition` vs. `StepRecord`
Para prevenir o vazamento do estado oculto em ambientes parcialmente observáveis (POMDPs), o loop de interação separa estritamente os dados do agente dos dados de depuração:

```python
@dataclass
class AgentTransition:
    """Dados visíveis apenas para o agente (apenas feedback observável)."""
    observation_before: Any    # Observação do agente o
    action: Any                # Ação a
    reward: float              # Recompensa r
    observation_after: Any     # Próxima observação o'
    terminated: bool           # Status de término
    truncated: bool            # Status de truncamento
    info: dict                 # Informações de diagnóstico

@dataclass
class StepRecord:
    """Registro mais completo de UI e histórico unindo estado real e AgentTransition."""
    episode: int
    step: int
    state_before: Any          # Estado interno real do mundo s
    state_after: Any           # Próximo estado interno real do mundo s'
    transition: AgentTransition
    update_info: dict          # Diagnóstico de atualização do agente
```

### 2. Contrato `BaseEnvironment`
Implemente esta interface para novos ambientes (MDP ou POMDP):
```python
class BaseEnvironment:
    def reset(self, seed: Optional[int] = None) -> tuple[Any, dict]:
        """Reinicia o ambiente. Retorna (observação, info)."""
        ...

    def step(self, action: Any) -> tuple[Any, float, bool, bool, dict]:
        """Executa uma ação. Retorna (observação, recompensa, terminated, truncated, info)."""
        ...

    def available_actions(self, observation: Optional[Any] = None) -> list[Any]:
        """Retorna ações válidas para a observação atual ou fornecida."""
        ...

    def get_state(self) -> Any:
        """Retorna o estado interno real (para ensino, depuração e análise de POMDPs)."""
        ...

    def render_ascii(self) -> str:
        """Representação ASCII opcional."""
        ...
```

### 3. Contrato `BaseAgent`
Implemente esta interface para algoritmos de aprendizado ou planejamento:
```python
class BaseAgent:
    def select_action(self, observation: Any, available_actions: list[Any]) -> Any:
        """Seleciona uma ação dada a observação atual."""
        ...

    def update(self, transition: AgentTransition, available_next_actions: Optional[list[Any]] = None) -> dict:
        """Atualiza os parâmetros do agente usando a transição observável. Retorna um dicionário de diagnóstico."""
        ...

    def get_policy(self, observation: Any, available_actions: Optional[list[Any]] = None) -> dict[Any, float]:
        """Retorna a distribuição de probabilidade das ações P(a|s)."""
        ...

    def get_q_values(self, observation: Any) -> dict[Any, float]:
        """Retorna os valores Q(s, a) para a observação."""
        ...

    def set_q_value(self, observation: Any, action: Any, value: float) -> None:
        """Permite edições manuais de valores Q no modo assistido."""
        ...
```

### 4. Coordenador `RLRunner`
Coordena passos, contadores de episódios, retorno acumulado $G_t$ (soma não descontada das recompensas do episódio $\sum r_t$) e histórico de transições:
```python
runner = RLRunner(env, agent)
record = runner.step(action=chosen_action)  # Passo manual
# ou
record = runner.step()                      # Ação automática via política do agente
```

---

## 🕹️ Modo de Treinamento Assistido

No **RL Workspace Visual** (`python -m {{PACKAGE_NAME}}.lab rl-workspace`), você pode executar o treinamento no **Modo Assistido**:

1. **[ RESET EPISODE ]**: Re-inicializa o estado do ambiente e do agente.
2. **[ STEP ]**: Executa exatamente uma transição.
3. **[ AUTO ]**: Executa passos automaticamente com intervalo configurável.
4. **[ PAUSE ]**: Pausa a execução automática para inspeção detalhada.

### Capacidades do Modo Assistido:
- **Separação Estado vs. Observação**: Inspecione o estado real $s$ ao lado do que o agente observou $o$.
- **Seleção Manual de Ação**: Escolha ações específicas para testar cenários e cenários contrafactuais.
- **Diagnósticos de Atualização**: Veja cálculos numéricos exatos (erro TD $\delta$, alvo de Bellman $r + \gamma \max Q$, Q antigo vs Q novo).
- **Substituição Interativa de Valores Q**: Edite valores Q e veja a política gulosa e a seleção de ações mudarem instantaneamente.
- **Inspetor de Histórico de Transição**: Navegue por qualquer passo anterior para inspecionar entradas e saídas exatas.

---

## 🔌 Como Plug-in de Exercícios MDP Futuros

Para implementar um exercício **Processo de Decisão de Markov Completamente Observável (MDP)** personalizado (ex: Gridworld, Gestão de Estoque):

1. **Definir Ambiente**:
   Crie uma subclasse de `BaseEnvironment`. Em MDPs completamente observáveis, `get_state()` e `get_observation()` retornam o mesmo valor.
2. **Definir Agente**:
   Implemente um algoritmo tabular (ex: Q-Learning, SARSA, Monte Carlo) criando uma subclasse de `BaseAgent`.
3. **Plug-in no Workspace**:
   Passe suas instâncias para `RLRunner(env, agent)` em `src/{{PACKAGE_NAME}}/rl_workspace.py`.

---

## 🐯 Como Plug-in de Exercícios POMDP Futuros

Para implementar um exercício **Processo de Decisão de Markov Parcialmente Observável (POMDP)** personalizado (ex: Problema do Tigre):

1. **Definir Ambiente com Separação Estado/Observação**:
   - `get_state()` retorna o estado real $s$ (ex: `posicao_tigre = "ESQUERDA"`).
   - `get_observation()` retorna a observação com ruído $o$ (ex: `rugido = "ESQUERDA"` com probabilidade 85%).
2. **Definir Agente de Crença**:
   Implemente um agente que mantém o estado de crença $b(s)$ atualizado via regra de Bayes em `update(transition: AgentTransition)`. O `AgentTransition` isola o agente do estado interno.
3. **Visualizar no Workspace**:
   O painel de transição destacará a distinção entre `Estado Anterior` e `Observação Anterior`.

---

## 📚 Referências
- Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press.
- Kaelbling, L. P., Littman, M. L., & Cassandra, A. R. (1998). Planning and acting in partially observable stochastic domains. *Artificial Intelligence*, 101(1-2), 99-134.
