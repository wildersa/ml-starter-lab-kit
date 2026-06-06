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

Se o suporte a ML ou Torch foi selecionado (e os arquivos foram gerados), instale também:

```bash
# ML Básico (se requirements-ml.txt existir)
pip install -r requirements-ml.txt

# PyTorch (se requirements-torch-*.txt existir)
pip install -r requirements-torch-*.txt
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
python -m {{PACKAGE_NAME}}.guide
```
O guia verifica se o CSV existe e se a coluna alvo foi identificada corretamente.

### 4. Execute o Dataset Advisor
Se ativado, o Advisor realiza uma análise heurística mais profunda dos seus dados para sugerir estratégias de modelagem:
```bash
{{ADVISOR_COMMAND}}
```
Ele cria o relatório `reports/dataset-advice.md` e um ponto de partida em `src/{{PACKAGE_NAME}}/suggested_pipeline.py`.

Nota: O **Guia do Projeto** é uma verificação de prontidão/validação, enquanto o **Dataset Advisor** fornece sugestões de modelagem explicáveis.

### 5. Engenharia de Features
Edite `src/{{PACKAGE_NAME}}/features.py` para adicionar features calculadas.

### 6. Treinamento e Baselines
O arquivo `src/{{PACKAGE_NAME}}/train.py` gerado é um **baseline simples**, não um modelo final. Ele estabelece um desempenho mínimo a ser superado.

## Fluxo sugerido

1. Coloque o dataset em `data/raw/`
2. Ajuste `configs/config.json`
3. Execute `python -m {{PACKAGE_NAME}}.guide` para validar a prontidão
4. Realize a EDA no notebook
5. Edite `src/{{PACKAGE_NAME}}/features.py`
6. Treine o modelo (baseline)
7. Avalie os resultados
8. Documente limitações e próximos passos

## Comandos sugeridos

```bash
# Validar prontidão
python -m {{PACKAGE_NAME}}.guide

# Processar dados
python -m {{PACKAGE_NAME}}.data

# (Opcional) Obter sugestões de modelagem
{{ADVISOR_COMMAND}}

# Treinar baseline
python -m {{PACKAGE_NAME}}.train

# Avaliar
python -m {{PACKAGE_NAME}}.evaluate
```
