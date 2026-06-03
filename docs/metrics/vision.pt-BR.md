# Métricas de visão computacional

Use métricas de visão quando o modelo trabalha com imagens.

## Classificação de imagem

Métricas comuns:

- accuracy;
- precision;
- recall;
- F1-score;
- matriz de confusão.

## Detecção de objetos

Métrica comum:

- mAP: mean Average Precision.

Ela avalia se as caixas detectadas e as classes estão corretas.

## Segmentação

Métricas comuns:

- IoU: Intersection over Union;
- Dice score.

Elas comparam máscaras previstas com máscaras esperadas.

## Aviso prático

Sempre inspecione exemplos visualmente. Uma métrica pode parecer boa enquanto o modelo falha em casos de borda importantes.
