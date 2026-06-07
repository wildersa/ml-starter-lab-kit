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

## Caminho de Aprendizado Pretendido
1. Explore o arquivo `data/raw/demo_dataset.csv`.
2. Execute `python -m {{PACKAGE_NAME}}.guide` para validar a configuração.
3. Use os notebooks fornecidos para realizar a Análise Exploratória de Dados (EDA).
4. Execute o script de treinamento para ver um modelo baseline em ação.
