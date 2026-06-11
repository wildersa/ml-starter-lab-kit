# Métricas de Agrupamento (Clustering)

No agrupamento, você não tem uma "resposta certa" (alvo) para comparar. A avaliação consiste em medir a qualidade dos grupos e sua utilidade.

## Inércia (Inertia)

- **O que responde**: Quão compactos são meus clusters?
- **Quando usar**: Principalmente com K-Means para encontrar o "Cotovelo" (o ponto onde adicionar mais clusters não reduz significativamente a inércia).
- **Quando evitar**: Quando seus clusters têm formas irregulares (não esféricos).

## Coeficiente de Silhueta (Silhouette Score)

- **O que responde**: Quão bem separados estão os clusters?
- **Quando usar**: Para verificar se uma amostra está muito mais próxima do seu próprio cluster do que de outros. Os valores variam de -1 a 1 (quanto maior, melhor).
- **Exemplo**: Um valor próximo de 1 significa que os clusters são bem distintos; um valor próximo de 0 significa que eles se sobrepõem significativamente.

## Interpretação Qualitativa

- **O que responde**: Esses grupos fazem sentido para o meu negócio?
- **Quando usar**: Sempre. Após o agrupamento, você deve descrever o "perfil" de cada grupo.
- **Armadilha comum**: Confiar apenas em métricas matemáticas. Um agrupamento matematicamente "perfeito" que agrupa clientes de uma forma que não leva a ações diferentes é inútil.

---

### Próximos Passos

Sempre verifique o [Checklist Antes da Avaliação](../checklists/before-evaluation.pt-BR.md) e lembre-se de que o agrupamento é frequentemente uma etapa exploratória, não uma resposta final.
- Veja o conceito de [Avaliação e Monitoramento](../concepts/evaluation-and-monitoring.pt-BR.md) para o ciclo completo.
