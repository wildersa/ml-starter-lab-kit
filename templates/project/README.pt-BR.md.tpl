# {{PROJECT_NAME}}

Este é um projeto de Machine Learning gerado, não a própria ferramenta de starter.

## Tipo de projeto

`{{TASK}}`

## Estrutura

```text
configs/             configurações JSON
data/raw/            dados originais
data/processed/      dados processados
notebooks/           exploração e análise
src/{{PACKAGE_NAME}}/ código principal
models/              modelos treinados
reports/             métricas, figuras e relatórios
tests/               testes mínimos
```

## Ambiente e Requisitos

Este projeto usa arquivos de requisitos para gerenciar o ambiente local.

```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente (Linux/macOS)
source .venv/bin/activate

# Ativar ambiente (Windows)
.venv\\Scripts\\activate

# Instalar dependências básicas e o próprio pacote em modo editável
pip install -r requirements.txt

# Para desenvolvimento e testes
pip install -r requirements-dev.txt

# Para notebooks
pip install -r requirements-notebook.txt
```

Se o suporte a ML, Torch ou MLflow foi selecionado (e os arquivos foram gerados), instale também:

```bash
# ML Básico (se requirements-ml.txt existir)
pip install -r requirements-ml.txt

# PyTorch (se requirements-torch-*.txt existir)
pip install -r requirements-torch-*.txt

# MLflow Tracking (se requirements-mlflow.txt existir)
pip install -r requirements-mlflow.txt
```

> **Nota sobre CUDA**: As instalações do CUDA podem exigir o índice de wheel do PyTorch correto e compatibilidade com o driver local.
> Verifique em: [pytorch.org](https://pytorch.org/get-started/locally/)

### Validação do ambiente

```bash
# Validar se o pacote está instalado corretamente
python -c "import {{PACKAGE_NAME}}; print('Pacote {{PACKAGE_NAME}} pronto')"

# Validar PyTorch e CUDA (se instalado)
python -c "import torch; print(f'Torch {torch.__version__} disponível. CUDA: {torch.cuda.is_available()}')"
```

## Primeiros Passos

### 1. Prepare seus dados
Coloque seu dataset em `data/raw/dataset.csv` (ou no caminho que você configurou).
{% if INCLUDE_DEMO == "true" %}
**Dataset de Demonstração**: Este projeto inclui um conjunto de dados sintéticos para aprendizado.
Consulte `docs/demo-scenario.md` para ver o cenário e o dicionário de dados.
{% endif %}

**Conceitos de Aprendizado Supervisionado:**
- **Alvo (Target)**: A coluna que você deseja prever. A maioria dos projetos tem **um** alvo principal.
- **Features**: As colunas usadas para fazer a previsão. Você pode ter **muitas** colunas de features. As colunas existentes no CSV já são candidatas a features.

Exemplo de `dataset.csv`:
```csv
feature_1,feature_2,feature_3,target_column
1.2,0,red,0
2.1,1,blue,1
```

### 2. Configure o projeto
Revise e edite `configs/config.json`:
- `data.raw_path`: O caminho dos seus dados de entrada.
- `data.processed_path`: Onde os dados limpos serão salvos.
- `target.column`: O nome da sua coluna alvo.

### 3. Execute o Guia do Projeto
Valide se seu dataset e configuração estão prontos para o pipeline:
```bash
python -m {{PACKAGE_NAME}}.lab check
```
O guia verifica se o CSV existe e se a coluna alvo foi identificada corretamente.

{% if LEARNING_ENABLED == "true" %}
## Workspace de Aprendizado Interativo (Recomendado)

Este projeto inclui um workspace visual para guiar você pelo processo de ML.

```bash
python -m {{PACKAGE_NAME}}.lab workspace
```

**IMPORTANTE**: Você deve executar a etapa de **Análise Exploratória de Dados (EDA)** antes que o workspace possa mostrar sugestões de modelos, baselines ou notas de aprendizado.

### Fluxo Visual
1. **Check**: Valida se os dados estão prontos.
2. **Explore (EDA)**: Gera o resumo do dataset.
3. **Workspace**: Abre o app Streamlit para insights interativos.
{% else %}
{% if GENERATE_ADVISOR == "true" %}
### 4. Execute o Dataset Advisor
Se ativado, o Advisor realiza uma análise heurística mais profunda dos seus dados para sugerir estratégias de modelagem:
```bash
python -m {{PACKAGE_NAME}}.lab advisor
```
Ele cria o relatório `reports/dataset-advice.md` e um ponto de partida em `src/{{PACKAGE_NAME}}/suggested_pipeline.py`.

Nota: O **Guia do Projeto** é uma verificação de prontidão/validação, enquanto o **Dataset Advisor** fornece sugestões de modelagem explicáveis.
{% endif %}

### 5. Engenharia de Features
Edite `src/{{PACKAGE_NAME}}/features.py` para adicionar features calculadas.

### 6. Treinamento e Baselines
O arquivo `src/{{PACKAGE_NAME}}/train.py` gerado é um **baseline simples**, não um modelo final. Ele estabelece um desempenho mínimo a ser superado.
{% endif %}

## Fluxo sugerido

1. Coloque o dataset em `data/raw/`
2. Ajuste `configs/config.json`
3. Execute `python -m {{PACKAGE_NAME}}.lab check` para validar a prontidão
4. Realize a EDA no notebook{% if GENERATE_EDA == "true" %} (ou execute `python -m {{PACKAGE_NAME}}.lab eda`{% if LEARNING_ENABLED == "true" %} ou use o workspace{% endif %}){% endif %}
5. Edite `src/{{PACKAGE_NAME}}/features.py`
6. Treine o modelo (baseline)
7. Avalie os resultados
8. Documente limitações e próximos passos

## Comandos sugeridos

{% if LEARNING_ENABLED == "true" %}
**Workspace Visual:**
```bash
python -m {{PACKAGE_NAME}}.lab workspace
```

**Alternativas CLI:**
{% endif %}
```bash
# Validar prontidão
python -m {{PACKAGE_NAME}}.lab check

{% if GENERATE_EDA == "true" %}
# Executar EDA (Gera artefatos necessários para Advisor/Baseline/Notas)
python -m {{PACKAGE_NAME}}.lab eda
{% endif %}

{% if GENERATE_ADVISOR == "true" %}
# (Opcional) Obter sugestões de modelagem
python -m {{PACKAGE_NAME}}.lab advisor
{% endif %}

{% if GENERATE_LEARNING == "true" %}
# (Opcional) Gerar notas de aprendizado
python -m {{PACKAGE_NAME}}.lab learn
{% endif %}

{% if GENERATE_BASELINE == "true" %}
# (Opcional) Executar baseline lab educacional
python -m {{PACKAGE_NAME}}.lab baseline
{% endif %}

{% if GENERATE_BANDIT == "true" %}
# (Opcional) Executar o Bandit Lab educacional (Multi-Armed Bandit)
python -m {{PACKAGE_NAME}}.lab bandit
{% endif %}

# Treinar baseline
python -m {{PACKAGE_NAME}}.lab train

# Avaliar
python -m {{PACKAGE_NAME}}.lab evaluate

# Executar todos os passos
python -m {{PACKAGE_NAME}}.lab all
```
{% if ENABLE_MLFLOW == "true" %}
## Rastreamento de Experimentos (MLflow)

Você pode visualizar suas execuções iniciando o servidor local:

```bash
mlflow server --port 5000
```

Em seguida, abra seu navegador em [http://localhost:5000](http://localhost:5000).
{% endif %}
