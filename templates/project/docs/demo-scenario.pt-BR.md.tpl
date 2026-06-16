# Cenário de Demonstração: {{PROJECT_NAME}}

> **Importante**: Este conjunto de dados é **sintético** e destinado apenas para **aprendizado**. Ele não representa dados do mundo real e não deve ser usado para tirar conclusões comerciais ou científicas válidas.

{% if DEMO_SUBTYPE == "classification" %}
## Cenário: Campanha Bancária (Classificação)
Esta demonstração simula uma campanha de marketing onde o objetivo é prever se um cliente assinará um depósito a prazo.

### Dicionário de Dados
| Coluna | Tipo | Descrição | Papel |
|---|---|---|---|
| id | Numérico | Identificador único do cliente | ID |
| age | Numérico | Idade do cliente | Feature |
| job | Categórico | Tipo de trabalho | Feature |
| balance | Numérico | Saldo anual médio | Feature |
| subscribed | Categórico | O cliente assinou? (yes/no) | **Alvo (Target)** |
{% endif %}

{% if DEMO_SUBTYPE == "regression" %}
## Cenário: Preços de Casas (Regressão)
Esta demonstração simula um conjunto de dados imobiliários onde o objetivo é prever o preço de venda de uma casa com base em suas características.

### Dicionário de Dados
| Coluna | Tipo | Descrição | Papel |
|---|---|---|---|
| id | Numérico | Identificador único da casa | ID |
| sqft | Numérico | Metragem quadrada da casa | Feature |
| bedrooms | Numérico | Número de quartos | Feature |
| age | Numérico | Idade da casa em anos | Feature |
| price | Numérico | Preço de venda | **Alvo (Target)** |
{% endif %}

{% if DEMO_SUBTYPE == "unsupervised" %}
## Cenário: Segmentação de Clientes (Não Supervisionado)
Esta demonstração simula dados de clientes para agrupamento (clustering). O objetivo é descobrir padrões ou segmentos entre os clientes sem um alvo predefinido.

### Dicionário de Dados
| Coluna | Tipo | Descrição | Papel |
|---|---|---|---|
| customer_id | Numérico | Identificador único do cliente | ID |
| age | Numérico | Idade do cliente | Feature |
| annual_income | Numérico | Renda anual | Feature |
| spend_score | Numérico | Pontuação atribuída pela loja com base no comportamento do cliente | Feature |

**Nota**: Como uma tarefa não supervisionada, não há coluna alvo. O objetivo é encontrar agrupamentos.
{% endif %}

{% if DEMO_SUBTYPE == "timeseries" %}
## Cenário: Vendas Diárias (Séries Temporais)
Esta demonstração simula dados de vendas diárias. O objetivo é entender padrões temporais e prever vendas futuras.

### Dicionário de Dados
| Coluna | Tipo | Descrição | Papel |
|---|---|---|---|
| date | Data | O dia do registro | Índice Temporal |
| sales | Numérico | Unidades vendidas | **Alvo (Target)** |
| on_promotion | Categórico | Houve promoção naquele dia? | Feature |

**Nota**: Esta é uma tarefa de previsão onde a relação entre data e valor é fundamental.
{% endif %}

{% if DEMO_SUBTYPE == "vision" %}
## Cenário: Metadados de Imagem (Visão)
Esta demonstração simula um arquivo de metadados para uma tarefa de classificação de imagem.

> **Nota**: Esta demonstração inclui apenas os metadados em CSV. **Não** inclui arquivos de imagem reais.

### Dicionário de Dados
| Coluna | Tipo | Descrição | Papel |
|---|---|---|---|
| image_path | Texto | Caminho para o arquivo de imagem | Referência |
| label | Categórico | Categoria da imagem (cat, dog, bird) | **Alvo (Target)** |
| width | Numérico | Largura da imagem | Metadados |
| height | Numérico | Altura da imagem | Metadados |
{% endif %}

{% if DEMO_SUBTYPE == "bandit" %}
## Cenário: Campanha Bancária (Multi-Armed Bandit)
Esta demonstração simula uma campanha de marketing usando um Multi-Armed Bandit para decidir qual oferta mostrar a cada cliente.

### Dicionário de Dados
| Coluna | Tipo | Descrição | Papel |
|---|---|---|---|
| event_id | Texto | Identificador único do evento | ID |
| timestamp | DateTime | Quando a decisão foi tomada | Contexto |
| customer_id | Texto | Identificador único do cliente | Contexto |
| age | Numérico | Idade do cliente | Contexto |
| balance | Numérico | Saldo anual médio | Contexto |
| job | Categórico | Tipo de trabalho | Contexto |
| segment | Categórico | Segmento de valor do cliente | Contexto |
| channel_preference | Categórico | Canal de comunicação preferencial | Contexto |
| previous_contacts | Numérico | Número de contatos anteriores | Contexto |
| arm_name | Categórico | A oferta selecionada pela política de comportamento | **Braço/Ação (Arm/Action)** |
| action_probability | Numérico | Probabilidade de selecionar este braço sob a política de comportamento | Propensão |
| policy_name | Texto | Nome da política que tomou a decisão (deterministic uniform logging) | Metadados |
| reward | Numérico | Resultado binário (1 para sucesso, 0 para nenhum) | **Alvo (Target)** |
| conversion | Numérico | O mesmo que a recompensa, usado para relatórios de negócios | Resultado |
| revenue | Numérico | Valor financeiro gerado pela conversão | Resultado |
| delay_days | Numérico | Dias até que a recompensa fosse observada | Atraso |

### Relação Contexto-Ação-Recompensa
Neste cenário, diferentes clientes respondem melhor a diferentes ofertas (braços):
* **Investment Advisor Call**: Melhor para clientes com saldo alto.
* **Term Deposit Email**: Melhor para clientes mais jovens (<30).
* **Credit Card Push**: Melhor para clientes de valor médio abaixo de 40 anos.
* **Term Deposit Phone**: Melhor para clientes aposentados.
{% endif %}

## Caminho de Aprendizado Pretendido
1. Explore o arquivo `data/raw/demo_dataset.csv`.
2. Execute `python -m {{PACKAGE_NAME}}.guide` para validar a configuração.
3. Use os notebooks fornecidos para realizar a Análise Exploratória de Dados (EDA).
4. Execute o script de treinamento para ver um modelo baseline em ação.
