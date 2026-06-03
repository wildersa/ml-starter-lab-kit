# Image Models / Computer Vision

Use image models when the input is an image or frame.

Examples:

- classify images;
- detect objects;
- segment regions;
- read visual patterns;
- fine-tune a pretrained model for a small task.

## Typical workflow

```text
images -> labels -> train/validation split -> transforms -> model -> evaluation
```

## Common tasks

| Task | Output | Example metric |
|---|---|---|
| Classification | one class per image | accuracy, F1 |
| Object detection | boxes + classes | mAP |
| Segmentation | pixel/region masks | IoU, Dice |

See [vision metrics](../metrics/vision.md).

## Does light fine-tuning need a framework?

Usually, yes.

For image fine-tuning, you normally use a deep learning framework such as PyTorch or TensorFlow/Keras.

This starter kit does not install those by default. Add them only when the project needs image training or fine-tuning.

## Practical advice

Start with a pretrained model. Training from scratch usually needs much more data and compute.
