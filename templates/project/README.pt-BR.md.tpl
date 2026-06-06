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

## Fluxo sugerido

```text
1. Coloque o dataset em data/raw/
2. Ajuste configs/config.json
3. Realize a EDA no notebook
4. Edite src/{{PACKAGE_NAME}}/features.py
5. Treine o modelo
6. Avalie os resultados
7. Documente limitações e próximos passos
```

## Comandos sugeridos

```bash
python -m {{PACKAGE_NAME}}.data
{{ADVISOR_COMMAND}}
python -m {{PACKAGE_NAME}}.train
python -m {{PACKAGE_NAME}}.evaluate
```
