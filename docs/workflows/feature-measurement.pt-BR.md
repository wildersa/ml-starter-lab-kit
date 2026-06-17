# Medição e Análise de Features

A medição e análise de features ajudam você a entender quais entradas realmente impulsionam o desempenho do seu modelo.

É importante distinguir entre duas atividades diferentes:
1. **Medição de Feature (Delta Antes/Depois):** Avaliar uma feature *candidata* específica comparando o desempenho do modelo com e sem ela.
2. **Análise de Feature (Importância/Screening):** Avaliar e ranquear features *existentes* em um conjunto de dados para ver quais parecem mais úteis.

O objetivo é evitar manter features que adicionam ruído, vazamento, custo ou complexidade.

## Medindo uma Feature Candidata

Para decidir se uma nova feature deve ser mantida, use o processo de **delta incremental**:

```text
features baseline -> treina/avalia -> adiciona feature candidata -> treina/avalia -> compara delta
```

### Consistência é Fundamental
Ao comparar os resultados "antes" e "depois", você **deve** usar exatamente o mesmo:
- Split de dados (conjuntos de treino/validação/teste);
- Método de validação (ex: K-Fold);
- Semente aleatória;
- Família de modelo e hiperparâmetros;
- Métrica de avaliação.

## Analisando Features Existentes

Se você deseja ranquear as features que já estão no seu dataset, considere estes métodos comuns:

| Método | Foco | Melhor Para |
|---|---|---|
| **Univariate Screening** | Relação individual entre uma feature e o alvo (target). | Filtragem inicial rápida de colunas irrelevantes. |
| **Importância Baseada no Modelo** | O quanto o modelo dependeu de uma feature durante o treino. | Entender a lógica interna de um modelo específico. |
| **Importância por Permutação** | O quanto o score cai quando os valores de uma feature são embaralhados. | Medir o impacto real no erro de previsão, independentemente do tipo de modelo. |

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

- **Ganho mensurável em validação:** Uma melhoria clara na sua métrica escolhida.
- **Comportamento estável:** Desempenho consistente em diferentes splits de dados.
- **Disponibilidade na previsão:** Garantia de que o dado existirá no momento da inferência.

Remova ou investigue uma feature quando ela tem:

- **Sinal suspeitamente alto:** Se uma única feature leva a scores "perfeitos" ou quase perfeitos, é provável que seja um sinal de **vazamento de alvo (target leakage)** (a feature contém a informação que o modelo está tentando prever).
- **Nenhum ganho mensurável:** Adicionar a feature aumenta a complexidade sem melhorar a métrica.
- **Informação futura:** A feature depende de dados que não seriam conhecidos em produção.

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
