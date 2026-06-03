# Medição de Features

Medição de features é a prática de verificar se uma nova feature realmente melhora o modelo.

O objetivo é evitar manter features que adicionam ruído, vazamento, custo ou complexidade.

## Processo básico

```text
features baseline -> treina/avalia -> adiciona feature candidata -> treina/avalia -> compara delta
```

Use o mesmo:

- split dos dados;
- método de validação;
- semente aleatória;
- família de modelo;
- métrica.

## O que medir

| Checagem | Pergunta |
|---|---|
| Delta da métrica | A métrica de validação melhorou? |
| Delta por segmento | Ajudou segmentos importantes ou só um? |
| Estabilidade | A feature se comporta parecido em treino/validação/teste? |
| Risco de vazamento | Esse valor existiria no momento da previsão? |
| Missingness | A feature fica ausente com frequência? |
| Custo | É caro calcular ou servir essa feature? |
| Interpretabilidade | A feature consegue ser explicada? |

## Regra simples de decisão

Mantenha uma feature quando ela tem:

- ganho mensurável em validação;
- sem vazamento óbvio;
- ausência aceitável;
- complexidade aceitável.

Remova ou isole uma feature quando ela tem:

- melhoria suspeitamente grande;
- informação futura;
- comportamento instável;
- nenhum ganho mensurável.

## Relatório sugerido

```text
Feature: media_compra_cliente_30d
Métrica antes: 0.712
Métrica depois: 0.728
Delta: +0.016
Decisão: manter
Motivo: ganho estável, sem vazamento óbvio
```

## Aviso prático

Uma feature que melhora o score de treino, mas não melhora validação, provavelmente não ajudou.
