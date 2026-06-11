# Métricas de Multi-Armed Bandits (MAB)

Os Multi-Armed Bandits (MAB) focam no equilíbrio entre **Exploração** (tentar coisas novas) e **Explotação** (usar o que você já sabe que funciona).

Para um mergulho profundo em como medir o desempenho do modelo e como isso se relaciona com o valor de negócio, consulte o guia de [Avaliação e Monitoramento](../concepts/evaluation-and-monitoring.pt-BR.md).

## Recompensa (Reward)

- **O que responde:** A ação escolhida resultou em sucesso?
- **Quando usar:** Para medir o feedback imediato de uma única decisão.
- **Quando evitar:** Quando o resultado demora muito para se manifestar (recompensa atrasada).
- **Armadilha comum:** Escolher uma recompensa que seja fácil de otimizar, mas que não gere valor para o negócio (ex: cliques vs. vendas reais).
- **Exemplo:** Um usuário clicando em um anúncio (recompensa binária) ou o valor da receita de uma compra (recompensa contínua).

## Recompensa Acumulada (Cumulative Reward)

- **O que responde:** Quanto valor total a política gerou ao longo do tempo?
- **Quando usar:** Para comparar o desempenho de longo prazo de diferentes estratégias.
- **Quando evitar:** Ao comparar execuções de durações diferentes sem normalizar.
- **Armadilha comum:** Comparar recompensas acumuladas de execuções com diferentes números totais de rodadas.
- **Exemplo:** A Estratégia A rendeu R$ 5.000 em 1.000 rodadas, enquanto a Estratégia B rendeu R$ 4.500.

## Regret (Arrependimento)

- **O que responde:** Quanta recompensa foi "perdida" porque escolhemos uma ação sub-ótima em vez da melhor possível?
- **Quando usar:** Para medir a eficiência do processo de aprendizado. Um regret menor significa que a política encontrou a melhor ação mais rápido.
- **Quando evitar:** Em ambientes de produção onde você não conhece as "verdadeiras" probabilidades de cada braço.
- **Armadilha comum:** O regret geralmente só é calculável em simulações onde você já conhece a "verdadeira" melhor ação.
- **Exemplo:** Se o melhor braço dá 10% de conversão e escolhemos um braço que dá 2%, temos 8% de regret naquela rodada.

## Lift vs. Baseline

- **O que responde:** Quanto a política de Bandit é melhor do que uma regra estática simples (como sempre mostrar o item mais popular)?
- **Quando usar:** Para justificar a complexidade de usar um sistema de Bandit.
- **Quando evitar:** Quando a baseline é tão forte que o custo do bandit não compensa.
- **Armadilha comum:** Usar uma baseline muito fraca que seja fácil de superar.
- **Exemplo:** O Bandit aumentou a conversão em 15% em comparação com a lista estática anterior de "Produtos em Destaque".

## Distribuição de Seleção de Braços (Arm Selection)

- **O que responde:** Com que frequência cada opção (braço) está sendo escolhida?
- **Quando usar:** Para garantir que o modelo está realmente convergindo para a melhor opção e não ficando "preso" em uma sub-ótima.
- **Quando evitar:** Nos estágios iniciais de exploração, quando a distribuição é naturalmente aleatória.
- **Armadilha comum:** Esperar 100% de convergência imediata; a exploração leva tempo.
- **Exemplo:** Observar que o modelo eventualmente escolhe a "Melhor Oferta" 90% do tempo.

## Custo de Exploração e Drift de Usuário

- **O que responde:** Quanto estamos "pagando" (em recompensa imediata perdida) para aprender sobre novas opções, e a melhor opção está mudando ao longo do tempo?
- **Quando usar:** Para equilibrar o risco de mostrar uma opção ruim a um usuário contra a necessidade de aprender.
- **Quando evitar:** Quando o ambiente é perfeitamente estático e você já conhece a escolha ideal.
- **Armadilha comum:** Não levar em conta o **Drift de Usuário**. O que era o melhor braço no mês passado pode não ser o melhor braço hoje.
- **Exemplo:** Perceber que o braço "Promoção de Verão" está perdendo sua eficácia à medida que o outono se aproxima.
