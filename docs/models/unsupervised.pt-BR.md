# Modelos não supervisionados

Use aprendizado não supervisionado quando você não tem uma coluna target.

O objetivo normalmente é descobrir estrutura nos dados.

Exemplos:

- agrupar clientes parecidos;
- reduzir dimensões;
- encontrar padrões estranhos;
- visualizar dados com muitas colunas.

## Técnicas comuns

| Técnica | Uso |
|---|---|
| K-Means | clusterização simples |
| PCA | redução de dimensionalidade |
| DBSCAN | clusterização por densidade |
| Isolation Forest | detecção de anomalias |

## Fluxo típico

```text
dados -> EDA -> escala -> redução de dimensão -> clusterização -> interpretação
```

## PCA em uma frase

PCA cria novas colunas que preservam o máximo possível da variação dos dados usando menos dimensões.

## K-Means em uma frase

K-Means separa os dados em K grupos pela distância até centros de cluster.

## Erros comuns

- Esquecer de escalar features numéricas.
- Tratar clusters como verdade absoluta.
- Escolher K sem análise.
- Usar features demais e muito ruidosas.

## Conselho prático

Modelos não supervisionados exigem interpretação. O modelo cria grupos; você ainda precisa explicar o que esses grupos significam.
