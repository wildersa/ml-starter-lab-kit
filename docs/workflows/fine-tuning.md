# Fine-tuning

Fine-tuning means adapting a pretrained model to a specific task.

## Common cases

- image classifier from a pretrained CNN/ViT;
- text classifier from a language model;
- time series model adapted to a domain;
- embedding model adapted to a retrieval task.

## Does it need a framework?

Usually, yes.

For practical fine-tuning you normally use PyTorch, TensorFlow/Keras, Hugging Face, or another specialized library.

This starter kit does not install those by default.

## Light fine-tuning workflow

```text
pretrained model -> small labeled dataset -> freeze some layers -> train a little -> evaluate
```

## Practical warning

Fine-tuning can overfit quickly when the dataset is small. Keep a validation set and compare against a simple baseline.
