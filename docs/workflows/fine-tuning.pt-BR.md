# Fine-tuning

Fine-tuning é adaptar um modelo pré-treinado para uma tarefa específica.

## Casos comuns

- classificador de imagem a partir de uma CNN/ViT pré-treinada;
- classificador de texto a partir de um modelo de linguagem;
- modelo temporal adaptado a um domínio;
- modelo de embedding adaptado para busca.

## Precisa de framework?

Normalmente, sim.

Na prática, fine-tuning costuma usar PyTorch, TensorFlow/Keras, Hugging Face ou outra biblioteca especializada.

Este starter kit não instala isso por padrão.

## Fluxo de fine-tuning leve

```text
modelo pré-treinado -> pequena base rotulada -> congelar algumas camadas -> treinar pouco -> avaliar
```

## Aviso prático

Fine-tuning pode overfitar rápido quando a base é pequena. Mantenha validação e compare com baseline simples.
