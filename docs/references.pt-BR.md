# Mapa de Teoria e Referências

Este documento fornece uma lista selecionada de fontes confiáveis para ajudar você a verificar conceitos e se aprofundar na teoria de machine learning usada neste projeto.

## Machine Learning Fundamental

### [Guia do Usuário scikit-learn](https://scikit-learn.org/stable/user_guide.html)
- **O que suporta**: Workflows gerais de machine learning, pré-processamento e seleção de modelos.
- **Onde se aplica**: Em todo o projeto, especificamente durante a preparação de dados e treinamento.
- **Nota para iniciantes**: Esta é a documentação padrão da indústria para ML em Python. É densa, mas inclui excelentes explicações narrativas junto com o código.
- **Limitação**: Focada em machine learning tradicional; não cobre deep learning ou cenários complexos de bandits em profundidade.

### [Avaliação de Modelos scikit-learn](https://scikit-learn.org/stable/modules/model_evaluation.html)
- **O que suporta**: Definições e a matemática por trás de métricas como Acurácia, Precisão, Recall e RMSE.
- **Onde se aplica**: Durante a fase de avaliação (`lab evaluate`) e ao interpretar resultados.
- **Nota para iniciantes**: Essencial para entender o *porquê* de escolher uma métrica em vez de outra.
- **Limitação**: Foca em como calcular as métricas, não necessariamente em como lidar com custos de erros específicos do negócio.

### [Datasets Gerados scikit-learn](https://scikit-learn.org/stable/datasets/sample_generators.html)
- **O que suporta**: A lógica por trás da geração de dados sintéticos.
- **Onde se aplica**: No Synthetic Data Lab e comandos `lab synthetic`.
- **Nota para iniciantes**: Útil se você quiser entender como dados "falsos" ainda podem ter propriedades matemáticas realistas.
- **Limitação**: Cobre distribuições padrão, mas não explica como simular regras de negócio complexas e específicas de um domínio.

## Multi-Armed Bandits (MAB)

### [Introduction to Multi-Armed Bandits (Slivkins)](https://arxiv.org/abs/1904.07272)
- **O que suporta**: As bases matemáticas de algoritmos de bandit como UCB e Thompson Sampling.
- **Onde se aplica**: No Multi-Armed Bandit Lab e `bandit_lab.py`.
- **Nota para iniciantes**: Este é um texto acadêmico rigoroso. Comece pela introdução e pelos primeiros capítulos para pegar a intuição antes de mergulhar nas provas.
- **Limitação**: Alta carga matemática; pode ser intimidador para iniciantes sem base em cálculo ou estatística.

### [Reinforcement Learning: An Introduction (Sutton & Barto)](http://incompleteideas.net/book/the-book-2nd.html)
- **O que suporta**: Contexto opcional sobre o campo mais amplo de Aprendizado por Reforço, do qual MAB faz parte.
- **Onde se aplica**: Contexto teórico para tomada de decisão sob incerteza.
- **Nota para iniciantes**: Um clássico, considerado a "bíblia" de RL. O Capítulo 2 é dedicado inteiramente a Multi-Armed Bandits e é altamente recomendado.
- **Limitação**: Cobre um escopo muito mais amplo do que este projeto exige; a maior parte do livro trata de tomada de decisão sequencial (MDPs) em vez das decisões de "passo único" em MAB.

---

*Nota: Estas fontes são externas. Embora confiáveis para a teoria, priorize sempre os guias internos do projeto para detalhes específicos de implementação.*
