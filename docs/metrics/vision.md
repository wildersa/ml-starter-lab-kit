# Vision Metrics

Computer Vision evaluation depends on the specific task: Classification, Detection, or Segmentation.

## Image Classification

Uses the same metrics as [Classification](classification.md): Accuracy, Precision, Recall, and F1-Score.

## Object Detection

- **mAP (mean Average Precision)**:
  - **What it answers**: How well did the model find all objects and correctly label them?
  - **When to use it**: To evaluate detection models across different classes.
  - **Common trap**: mAP can be confusing because it depends on an IoU threshold (see below). A model might have high mAP but still miss small objects.

- **IoU (Intersection over Union)**:
  - **What it answers**: How much does the predicted box overlap with the ground truth box?
  - **When to use it**: To measure localization accuracy. Usually, an IoU > 0.5 is considered a "hit".

## Segmentation

- **Dice Score / F1-Score**:
  - **What it answers**: How similar is the predicted mask to the actual mask?
  - **When to use it**: To evaluate pixel-level accuracy. It is very common in medical imaging.

---

### Next Steps

Always check the [Before Evaluation Checklist](../checklists/before-evaluation.md). For vision tasks, mathematical metrics are never enough—always **visually inspect** a sample of successes and failures.
- Review the [Evaluation and Monitoring](../concepts/evaluation-and-monitoring.md) concept for the full lifecycle.
