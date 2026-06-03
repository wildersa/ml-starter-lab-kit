# Vision Metrics

Use vision metrics when the model works with images.

## Image classification

Common metrics:

- accuracy;
- precision;
- recall;
- F1-score;
- confusion matrix.

## Object detection

Common metric:

- mAP: mean Average Precision.

It evaluates whether detected boxes and classes are correct.

## Segmentation

Common metrics:

- IoU: Intersection over Union;
- Dice score.

They compare predicted masks with expected masks.

## Practical warning

Always inspect examples visually. A metric can look good while predictions fail in important edge cases.
