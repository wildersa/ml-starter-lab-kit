# Vision Metrics

Vision tasks (Classification, Detection, Segmentation) require metrics that account for both the "what" and the "where" in an image.

For a deeper dive into how to measure model performance and how it relates to business value, see the [Evaluation and Monitoring](../concepts/evaluation-and-monitoring.md) guide.

## Image Classification (Accuracy, F1, etc.)

- **What it answers:** Did the model correctly identify the main object in the image?
- **When to use:** When your output is a single label for the whole image.
- **When to avoid:** When the image contains multiple important objects that all need to be identified.
- **Common trap:** Ignoring small objects or backgrounds that might be confusing the model (e.g., a model that learns to identify "cows" only because it sees "green grass").
- **Example:** A model labeling an image as "Cat" with 95% confidence.

## mAP (mean Average Precision)

- **What it answers:** In Object Detection, how good is the model at both finding the boxes and labeling them correctly?
- **When to use:** The standard metric for Object Detection (e.g., finding cars in a street).
- **When to avoid:** When you only care about if an object is present, not where it is located.
- **Common trap:** Comparing mAP across different IoU thresholds without specifying which one was used (e.g., mAP@0.5 vs mAP@0.75).
- **Example:** A model with 0.8 mAP is generally very good at both locating and identifying objects.

## IoU (Intersection over Union)

- **What it answers:** How much does the predicted box/mask overlap with the actual box/mask?
- **When to use:** To measure the localization accuracy in Detection and Segmentation.
- **When to avoid:** As a standalone metric for business value, as it doesn't tell you if the classification was correct.
- **Common trap:** Setting an IoU threshold that is too strict for the problem (e.g., requiring 90% overlap for a very blurry object).
- **Example:** An IoU of 0.7 means 70% of the area of the two boxes is shared.

## Dice Score (F1-score for masks)

- **What it answers:** How similar is the predicted shape to the true shape in Image Segmentation?
- **When to use:** Very common in medical imaging (segmenting tumors, organs).
- **When to avoid:** When you have many small, disconnected objects.
- **Common trap:** It is very sensitive to small objects; a few pixels of error can drastically change the score for a tiny mask.
- **Example:** A Dice score of 0.9 on a lung segmentation means the predicted mask almost perfectly matches the ground truth.
