# sample_ml_project

This is a generated Machine Learning project, not the starter tool itself.
Este é um projeto de Machine Learning gerado, não a própria ferramenta starter.

## Tipo de projeto

`supervised`

## Estrutura

```text
configs/             configurações em JSON
data/raw/            dados originais
data/processed/      dados tratados
notebooks/           exploração e análise
src/sample_ml_project/ código principal
models/              modelos treinados
reports/             métricas, figuras e relatórios
tests/               testes mínimos
```

## Ambiente e Requisitos

Este projeto utiliza arquivos de requisitos para gerenciar o ambiente local.

```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente (Linux/macOS)
source .venv/bin/activate

# Ativar ambiente (Windows)
.venv\Scripts\activate

# Instalar dependências básicas e o próprio pacote em modo editável
pip install -r requirements.txt

# Para desenvolvimento e testes
pip install -r requirements-dev.txt

# Para notebooks
pip install -r requirements-notebook.txt
```

Se o suporte a ML ou Torch foi selecionado (e os arquivos foram gerados), instale também:

```bash
# ML básico (se requirements-ml.txt existir)
pip install -r requirements-ml.txt

# PyTorch (se requirements-torch-*.txt existir)
pip install -r requirements-torch-*.txt
```

> **Nota sobre CUDA**: Instalações CUDA podem exigir o index de wheel correto do PyTorch e compatibilidade de driver local.
> Verifique em: [pytorch.org](https://pytorch.org/get-started/locally/)

### Validação de ambiente

```bash
# Validar se o pacote está instalado corretamente
python -c "import sample_ml_project; print('Pacote sample_ml_project pronto')"

# Validar PyTorch e CUDA (se instalado)
python -c "import torch; print(f'Torch {torch.__version__} disponível. CUDA: {torch.cuda.is_available()}')"
```

## Fluxo sugerido

```text
1. Coloque o dataset em data/raw/
2. Ajuste configs/config.json
3. Faça a EDA no notebook
4. Edite src/sample_ml_project/features.py
5. Treine o modelo
6. Avalie os resultados
7. Documente limitações e próximos passos
```

## Comandos sugeridos

```bash
python -m src.sample_ml_project.data
python -m src.sample_ml_project.train
python -m src.sample_ml_project.evaluate
```
