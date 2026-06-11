# Classification Metrics

Use classification metrics when the model predicts a category (class).

For a deeper dive into how to measure model performance and how it relates to business value, see the [Evaluation and Monitoring](../concepts/evaluation-and-monitoring.md) guide.

## Confusion Matrix

- **What it answers:** How many items were correctly classified and what kind of errors (False Positives or False Negatives) the model is making.
- **When to use:** Always. It is the foundation for all other classification metrics.
- **When to avoid:** Never, though for many classes (e.g., >20), it can become hard to read.
- **Common trap:** Ignoring the diagonal. If the diagonal is weak, your model is essentially guessing.
- **Example:** In a spam filter, it shows 80 real spams caught, 5 real spams missed, and 2 normal emails wrongly blocked.

## Accuracy

- **What it answers:** What percentage of total predictions were correct?
- **When to use:** When your classes are balanced (e.g., 50% spam, 50% not spam).
- **When to avoid:** When one class is much more frequent than others (imbalanced data).
- **Common trap:** A model that always predicts "Not Fraud" on a dataset with 99% non-fraud transactions will have 99% accuracy but is useless.
- **Example:** A cat vs dog classifier gets 90 out of 100 images right. Accuracy = 90%.

## Precision

- **What it answers:** Of all items the model labeled as "Positive", how many were actually correct?
- **When to use:** When the **False Positive cost** is high (e.g., blocking a legitimate user's account).
- **When to avoid:** When missing positive cases is more dangerous than being wrong about one.
- **Common trap:** Having 100% precision by only predicting "Positive" for the single most obvious case, while missing 99 others.
- **Example:** A "Safe to invest" recommender. You only want to be told "Yes" when it is extremely likely to be true.

## Recall

- **What it answers:** Of all the actual "Positive" items that exist, how many did the model find?
- **When to use:** When the **False Negative cost** is high (e.g., missing a cancer diagnosis).
- **When to avoid:** When the cost of a false alarm is too high.
- **Common trap:** Getting 100% recall by simply labeling everything as "Positive".
- **Example:** A security alarm. You want it to go off for *every* break-in, even if it occasionally triggers for a cat.

## F1-Score

- **What it answers:** What is the harmonic balance between Precision and Recall?
- **When to use:** When you want a single number to compare models and both Precision and Recall are important.
- **When to avoid:** When business requirements specifically favor one over the other (e.g., a "Safety First" system favors Recall).
- **Common trap:** Using it when classes are very imbalanced without checking individual Precision/Recall.
- **Example:** A chatbot intent classifier where you want to be both accurate and comprehensive.

## ROC-AUC and PR-AUC

- **What it answers:** How good is the model at ranking items by probability, regardless of the chosen **Threshold**?
- **When to use:** To evaluate the general "power" of the model before picking a specific cutoff. Use PR-AUC for highly imbalanced datasets.
- **When to avoid:** When you need to know the actual performance at a specific operational point.
- **Common trap:** A high AUC doesn't mean the model is ready for production; you still need to pick a good threshold.
- **Example:** Comparing two fraud detection algorithms to see which one "separates" fraudsters from customers better.

## Thresholds

- **What it answers:** At what probability should I flip from "No" to "Yes"?
- **When to use:** Whenever your model outputs probabilities (0.0 to 1.0).
- **When to avoid:** Never. Choosing a threshold is a business decision.
- **Common trap:** Using the default 0.5 for everything. If False Negatives are expensive, you should lower the threshold.
- **Example:** Lowering the threshold to 0.2 to catch more potential frauds, even if it increases false alarms.
