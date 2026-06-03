# Métricas de bandits

Use estas métricas quando uma política escolhe ações e recebe recompensas.

## Reward

Feedback imediato de uma ação.

Exemplo: clique, conversão, receita, score.

## Recompensa acumulada

Soma das recompensas ao longo do tempo.

Útil para comparar políticas.

## Regret

Quanto de recompensa foi perdido em relação a uma escolha melhor possível.

Quanto menor, melhor.

## Taxa de exploração

Com que frequência a política testa opções incertas.

Baixa demais pode parar o aprendizado. Alta demais pode desperdiçar tráfego.

## Fairness de exposição

Verifica se segmentos elegíveis recebem exposição razoável.

Importante quando ações afetam usuários de formas diferentes.
