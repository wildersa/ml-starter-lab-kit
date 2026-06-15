# Guia de Redação de Documentação de Aprendizado

Este guia define as regras para a criação de conteúdo educacional para garantir que seja seguro em termos de direitos autorais, preciso e conciso.

## Papéis das Fontes

Ao redigir a documentação, utilize apenas estas fontes aprovadas, dependendo do tipo de conteúdo:

| Papel | Fonte | Escopo |
|---|---|---|
| **Prático / API** | [Documentação do scikit-learn](https://scikit-learn.org/) | Fonte primária para tópicos clássicos de Machine Learning, detalhes de implementação e padrões de API. |
| **Teoria** | [Slivkins (2019) - Introduction to Multi-Armed Bandits](https://arxiv.org/abs/1904.07272) | Fonte primária para a teoria de Multi-Armed Bandit (MAB). |
| **Contexto Opcional** | [Sutton & Barto (2018) - Reinforcement Learning: An Introduction](http://incompleteideas.net/book/the-book-2nd.html) | Contexto de fundo apenas para Reinforcement Learning (RL). |

## Regras de Direitos Autorais

Para proteger a propriedade intelectual e evitar plágio:

1.  **Sem Cópia Direta**: Não copie parágrafos, figuras, tabelas, resumos de artigos ou exercícios de nenhuma fonte, inclusive das aprovadas.
2.  **Sintetize e Parafraseie**: Explique os conceitos com suas próprias palavras. Foque em como o conceito se aplica às ferramentas e fluxos de trabalho deste projeto.
3.  **Sem Pesquisa Independente**: Não peça a agentes de IA (como Jules) para pesquisar novas bibliografias ou fontes externas, a menos que explicitamente solicitado por um autor humano.
4.  **Sem Bibliografia Inventada**: Use apenas as fontes listadas neste guia ou aquelas especificamente fornecidas para uma tarefa.

## Princípios de Redação

-   **Concisão sobre Profundidade Acadêmica**: Prefira seções curtas de "Saiba mais" em vez de documentação densamente acadêmica. O objetivo é ajudar o usuário a começar, não fornecer uma base teórica completa.
-   **Foco Prático**: Sempre relacione conceitos teóricos de volta ao código do projeto, comandos da CLI (`lab`) ou artefatos gerados.
-   **Notas de Limitação**: Todo documento que cubra conceitos teóricos **deve** incluir uma nota de "Limitações" ou "Quando não usar" para fornecer expectativas realistas.

## Instruções para Agentes

Se você for um agente de IA:
- Siga as regras acima rigorosamente.
- Não "alucine" ou pesquise artigos acadêmicos adicionais para citar.
- Se um conceito não for coberto pelas fontes aprovadas e você não tiver recebido material específico, mantenha a explicação em alto nível e focada na implementação prática no código.
