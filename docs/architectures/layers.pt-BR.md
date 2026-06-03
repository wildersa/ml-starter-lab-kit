# Camadas de pipeline ML

Um projeto de treino pode ser organizado em camadas mesmo quando o modelo é simples.

Isso não é a mesma coisa que camadas de rede neural.

## Camadas comuns de pipeline

```text
dados brutos
  -> validação dos dados
  -> limpeza
  -> engenharia de features
  -> estratégia de split
  -> baseline
  -> treino do modelo
  -> avaliação
  -> registro de modelo / artefatos
  -> inferência
  -> monitoramento
```

## O que cada camada faz

| Camada | Objetivo |
|---|---|
| Dados brutos | arquivos originais, extrações de banco, APIs |
| Validação dos dados | checar schema, nulos, duplicados, colunas suspeitas |
| Limpeza | corrigir tipos, remover linhas inválidas, tratar nulos |
| Engenharia de features | criar entradas úteis para o modelo |
| Estratégia de split | separar treino/validação/teste sem vazamento |
| Baseline | referência simples para superar |
| Treino | ajustar o modelo |
| Avaliação | comparar métricas e inspecionar erros |
| Registro/artefatos | salvar modelo e metadados |
| Inferência | usar o modelo treinado |
| Monitoramento | acompanhar qualidade, drift, latência e custo |

## Regra prática

Use camadas para deixar o projeto entendível. Não crie camadas só para parecer enterprise.
