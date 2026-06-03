# Modelos de imagem / Visão Computacional

Use modelos de imagem quando a entrada é uma imagem ou frame.

Exemplos:

- classificar imagens;
- detectar objetos;
- segmentar regiões;
- ler padrões visuais;
- fazer fine-tuning de um modelo pré-treinado para uma tarefa menor.

## Fluxo típico

```text
imagens -> labels -> split treino/validação -> transformações -> modelo -> avaliação
```

## Tarefas comuns

| Tarefa | Saída | Métrica exemplo |
|---|---|---|
| Classificação | uma classe por imagem | accuracy, F1 |
| Detecção de objetos | caixas + classes | mAP |
| Segmentação | máscaras por pixel/região | IoU, Dice |

Veja [métricas de visão](../metrics/vision.pt-BR.md).

## Fine-tuning leve exige framework?

Normalmente, sim.

Para fine-tuning de imagem, geralmente você usa um framework de deep learning como PyTorch ou TensorFlow/Keras.

Este starter kit não instala isso por padrão. Adicione só quando o projeto realmente precisar treinar imagem ou fazer fine-tuning.

## Conselho prático

Comece com modelo pré-treinado. Treinar do zero normalmente exige muito mais dados e computação.
