# ML Starter Lab Kit

**Scaffold interativo para pequenos projetos de Machine Learning.**

O ML Starter Lab Kit é um **gerador de projetos** que ajuda você a iniciar experimentos de ML com uma estrutura de pastas profissional, código base e orientações didáticas.

- **O que é**: Uma ferramenta para criar um espaço de trabalho limpo e organizado para seu código de ML.
- **O que não é**: Não é uma plataforma de AutoML ou uma biblioteca de treinamento. Não treina modelos automaticamente; ele fornece o "esqueleto" e as melhores práticas para que você possa focar na parte de Machine Learning.

## Início rápido (Quick start)

1. **Clone** este repositório:

   ```bash
   git clone https://github.com/wildersa/ml-starter-lab-kit.git
   cd ml-starter-lab-kit
   ```

2. **Gere** seu projeto:

   ```bash
   python create_ml_starter.py
   ```

3. **Acesse** a pasta do projeto gerado (ela é criada ao lado desta ferramenta):

   ```bash
   cd ../nome-do-seu-projeto
   ```

4. **Inicialize**: Crie um ambiente virtual e instale os requisitos:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

5. **Comece**: Coloque seus dados em `data/raw/` e siga o `README.md` gerado.

Layout recomendado:

```text
workspace/
├── ml-starter-lab-kit/      # esta ferramenta
└── meu-projeto-ml/          # seu projeto gerado
```

Veja [layout do starter e do projeto gerado](docs/usage/project-layout.pt-BR.md) e um [exemplo de projeto gerado](examples/generated-project-sample/).

## Tipos de projeto disponíveis

- **generic**: Estrutura padrão de projeto de ML.
- **supervised**: Para tarefas de classificação e regressão.
- **unsupervised**: Para agrupamento (clustering) e redução de dimensionalidade.
- **timeseries**: Para previsão e análise de séries temporais.
- **vision**: Para classificação e detecção de imagens.
- **bandit**: Para Multi-Armed Bandits e decisões adaptativas (exploração-explotação).

## Funcionalidades Principais

- **Synthetic Data Lab**: Gere conjuntos de dados determinísticos (Classificação, Regressão, MAB, etc.) para testar pipelines ou estudar o comportamento de ML sem dados reais.
- **Workspace Interativo**: Um ambiente visual guiado (usando Streamlit) para EDA, treino de baselines e avaliação de modelos.

## Documentação

Comece pelo [Índice da Documentação](docs/README.pt-BR.md) para explorar:

- [Trilhas de aprendizado](docs/learning-paths.pt-BR.md)
- [Guias de workflow](docs/workflows/README.pt-BR.md)
- [Visão geral de arquiteturas](docs/architectures/README.pt-BR.md)
- [Erros comuns](docs/common-mistakes/README.pt-BR.md)
- [Glossário](docs/glossary/README.pt-BR.md)

## Filosofia

- **Zero dependências no gerador**: Usa apenas a biblioteca padrão do Python.
- **Simples e Editável**: Sem frameworks pesados; o código gerado é seu para alterar.
- **Baseado em perfis**: Suporte para ambientes Python 'Safe' (3.12) ou 'Modern' (3.14).
- **Stack opcional**: Adicione facilmente PyTorch (CPU/CUDA) ou libs padrão de ML (pandas, scikit-learn).
- **Organização limpa**: `features.py` dedicado e configuração baseada em JSON.
