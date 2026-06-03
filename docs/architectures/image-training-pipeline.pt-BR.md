# Pipeline de treino com imagem

Use quando a entrada é uma imagem.

Exemplos:

- classificação de imagem;
- detecção de objetos;
- segmentação;
- fine-tuning leve a partir de modelo pré-treinado.

## Fluxo simplificado

```mermaid
flowchart LR
    A[Imagens] --> B[Labels/anotações]
    B --> C[Split treino/validação]
    C --> D[Transformações/aumento]
    D --> E[Modelo pré-treinado]
    E --> F[Fine-tuning]
    F --> G[Avaliação]
    G --> H[Artefato do modelo]
```

## Notas

- Treino com imagem normalmente precisa de PyTorch ou TensorFlow/Keras.
- Fine-tuning costuma ser melhor que treinar do zero.
- Sempre inspecione predições visualmente.

Veja:

- [modelos de visão](../models/vision.pt-BR.md)
- [métricas de visão](../metrics/vision.pt-BR.md)
- [fine-tuning](../workflows/fine-tuning.pt-BR.md)
