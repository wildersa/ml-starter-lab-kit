# Bem-vindo ao {{PROJECT_NAME}}!

Este guia ajudará você a navegar no seu novo projeto de Machine Learning.

## 1. Visão Geral do Projeto

- **Nome do Projeto**: {{PROJECT_NAME}}
- **Tarefa de ML**: {{TASK}}
- **Nome do Pacote**: `{{PACKAGE_NAME}}`
- **Versão do Python**: {{PYTHON_VERSION}}

## 2. Configuração Rápida do Ambiente

Abra seu terminal nesta pasta e execute:

```bash
# 1. Criar ambiente virtual
{% if PYTHON_VERSION == "3.12" %}
py -3.12 -m venv .venv           # Windows
python3.12 -m venv .venv         # POSIX
{% else %}
py -{{PYTHON_VERSION}} -m venv .venv
python{{PYTHON_VERSION}} -m venv .venv
{% endif %}

# 2. Ativar ambiente
.venv\Scripts\activate           # Windows
source .venv/bin/activate        # POSIX

# 3. Instalar dependências e o projeto
pip install -r requirements.txt
pip install -e .
```

## 3. Trilha de Aprendizado Recomendada

Siga estes passos em ordem para ter a melhor experiência:

### Passo 1: Validação de Prontidão (Check)
Valide se seu dataset e configuração estão prontos:
```bash
python -m {{PACKAGE_NAME}}.lab check
```

### Passo 2: Análise Exploratória de Dados (EDA) — **NÃO PULE**
Antes de treinar qualquer modelo, você deve entender seus dados.
- **Notebook (Recomendado para iniciantes)**: Abra `notebooks/01_eda.ipynb`
{% if GENERATE_EDA == "true" %}
- **Alternativa CLI**: `python -m {{PACKAGE_NAME}}.lab eda`
{% endif %}

> **Nota**: A EDA gera artefatos necessários para o Advisor e para o Workspace de Aprendizado.

{% if LEARNING_ENABLED == "true" %}
### Passo 3: Workspace de Aprendizado Interativo
Se você estiver no Modo Guiado, abra o workspace visual:
```bash
python -m {{PACKAGE_NAME}}.lab workspace
```
{% endif %}

### Passo 4: Sugestões de Modelagem e Baselines
{% if GENERATE_ADVISOR == "true" %}
- **Advisor**: `python -m {{PACKAGE_NAME}}.lab advisor` (Sugestões de modelagem)
{% endif %}
- **Treinar Baseline**: `python -m {{PACKAGE_NAME}}.lab train`
- **Avaliar**: `python -m {{PACKAGE_NAME}}.lab evaluate`

---

## 4. Estrutura do Projeto e Arquivos Chave

- `data/raw/`: Coloque seu dataset aqui (Padrão: `{{DATASET_PATH}}`).
- `configs/config.json`: Configuração principal do projeto (Coluna alvo, caminhos).
- `src/{{PACKAGE_NAME}}/features.py`: Defina sua lógica de engenharia de atributos aqui.
- `notebooks/01_eda.ipynb`: Seu ponto de partida para exploração de dados.

## 5. Notebooks vs. Pipeline Python

- **Use Notebooks (`notebooks/`)**: Para exploração, visualização e aprendizado iterativo.
- **Use Pipeline Python (`src/`)**: Para execução repetível, controle de versão e código pronto para produção.

{% if GENERATE_DOCS == "true" %}
## 6. Documentação

Consulte a pasta `docs/` para guias detalhados:
- [Trilha de Aprendizado](docs/learning-path.pt-BR.md)
- [Dicionário de Dados](docs/data-dictionary.md)
- [Guia de Avaliação](docs/evaluation.pt-BR.md)
{% if INCLUDE_DEMO == "true" %}
- [Cenário de Demonstração](docs/demo-scenario.md)
{% endif %}
{% if GENERATE_BANDIT == "true" %}
- [Guia do Bandit Lab](docs/mab-lab.pt-BR.md)
{% endif %}
{% if GENERATE_SYNTHETIC == "true" %}
- [Guia de Dados Sintéticos](docs/synthetic-data-lab.pt-BR.md)
{% endif %}
{% if GENERATE_MONITOR == "true" %}
- [Guia de Monitoramento](docs/monitoring.pt-BR.md)
{% endif %}
{% endif %}
