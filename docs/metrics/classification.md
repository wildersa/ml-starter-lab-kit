# Classification Metrics

Use classification metrics when your model predicts a category or label (e.g., "Spam" vs. "Not Spam").

Choosing the right metric depends on the **cost of being wrong** in different ways.

## Confusion Matrix

A table that summarizes the model's performance by comparing predicted labels against actual labels.

- **What it answers**: Where exactly is my model getting confused?
- **When to use it**: Always. It is the foundation for all other classification metrics.
- **Example**: A table showing that your model correctly identified 90 "Spam" emails but misclassified 10 "Not Spam" emails as "Spam".

## Accuracy

- **What it answers**: What fraction of all predictions were correct?
- **When to use it**: When your classes are roughly equal in size (balanced dataset).
- **When to avoid it**: When one class is much more frequent than others (imbalanced dataset).
- **Common trap**: High accuracy on an imbalanced dataset (e.g., 99% accuracy because 99% of the data belongs to one class) can hide a model that fails completely on the minority class.
- **Example**: In a dataset with 50% cats and 50% dogs, 0.90 accuracy means 9 out of 10 animals were identified correctly.

## Precision

- **What it answers**: Of all cases predicted as positive, how many were actually positive?
- **When to use it**: When the cost of a **False Positive** (FP) is high.
- **Common trap**: Optimizing only for precision can lead to missing many positive cases (low recall).
- **Example**: A "Not Guilty" person being sent to jail. High precision ensures we only convict those who are truly guilty.

## Recall (Sensitivity)

- **What it answers**: Of all actual positive cases, how many did the model find?
- **When to use it**: When the cost of a **False Negative** (FN) is high.
- **Common trap**: High recall is easy to achieve by predicting "Positive" for everything, which ruins precision.
- **Example**: A sick person being told they are healthy. High recall ensures we find as many sick people as possible.

## F1-Score

- **What it answers**: What is the harmonic balance between Precision and Recall?
- **When to use it**: When you need a single number to compare models and you care about both FP and FN.
- **Common trap**: It treats Precision and Recall as equally important, which might not be true for your specific business case.
- **Example**: An F1 of 0.85 suggests a strong balance between finding all positives and ensuring those found are correct.

## ROC-AUC and PR-AUC

- **What it answers**: How good is the model at ranking items by probability?
- **When to use it**: When you haven't decided on a final **Threshold** yet. Use PR-AUC for highly imbalanced datasets.
- **When to avoid it**: When you need to know the actual performance at a specific operational point.
- **Example**: An AUC of 0.90 means there is a 90% chance the model will rank a random positive instance higher than a random negative one.

## Understanding Thresholds

Classification models usually output a probability (0.0 to 1.0). The **Threshold** (default 0.5) is the cutoff point where you decide to label something as "Positive".

- Moving the threshold **up** (e.g., to 0.8) increases Precision but decreases Recall.
- Moving the threshold **down** (e.g., to 0.2) increases Recall but decreases Precision.

---

### Next Steps

Always check the [Before Evaluation Checklist](../checklists/before-evaluation.md) to ensure your metrics are reliable and match your business goals.
- Review the [Evaluation and Monitoring](../concepts/evaluation-and-monitoring.md) concept for the full lifecycle.
