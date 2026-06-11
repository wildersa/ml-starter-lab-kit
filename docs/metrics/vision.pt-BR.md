# Métricas de Visão Computacional

A avaliação de Visão Computacional depende da tarefa específica: Classificação, Detecção ou Segmentação.

## Classificação de Imagem

Usa as mesmas métricas da [Classificação](classification.pt-BR.md): Acurácia, Precisão, Recall e F1-Score.

## Detecção de Objetos

- **mAP (mean Average Precision)**:
  - **O que responde**: Quão bem o modelo encontrou todos os objetos e os rotulou corretamente?
  - **Quando usar**: Para avaliar modelos de detecção em diferentes classes.
  - **Armadilha comum**: O mAP pode ser confuso porque depende de um threshold de IoU (veja abaixo). Um modelo pode ter mAP alto, mas ainda perder objetos pequenos.

- **IoU (Intersection over Union)**:
  - **O que responde**: O quanto a caixa prevista se sobrepõe à caixa real (ground truth)?
  - **Quando usar**: Para medir a precisão da localização. Geralmente, um IoU > 0,5 é considerado um "acerto".

## Segmentação

- **Dice Score / F1-Score**:
  - **O que responde**: Quão semelhante é a máscara prevista em relação à máscara real?
  - **Quando usar**: Para avaliar a precisão ao nível do pixel. É muito comum em imagens médicas.

---

### Próximos Passos

Sempre verifique o [Checklist Antes da Avaliação](../checklists/before-evaluation.pt-BR.md). Para tarefas de visão, métricas matemáticas nunca são suficientes — sempre **inspecione visualmente** uma amostra de sucessos e falhas.
- Veja o conceito de [Avaliação e Monitoramento](../concepts/evaluation-and-monitoring.pt-BR.md) para o ciclo completo.
