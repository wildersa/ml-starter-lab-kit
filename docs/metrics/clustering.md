# Clustering Metrics

In clustering, you don't have a "right answer" (target) to compare against. Evaluation is about measuring the quality of the groups and their usefulness.

## Inertia

- **What it answers**: How tightly packed are my clusters?
- **When to use it**: Primarily with K-Means to find the "Elbow" (the point where adding more clusters doesn't significantly reduce inertia).
- **When to avoid it**: When your clusters have irregular shapes (not spherical).

## Silhouette Score

- **What it answers**: How well-separated are the clusters?
- **When to use it**: To check if a sample is much closer to its own cluster than to others. Scores range from -1 to 1 (higher is better).
- **Example**: A score near 1 means the clusters are very distinct; a score near 0 means they overlap significantly.

## Qualitative Interpretation

- **What it answers**: Do these groups make sense for my business?
- **When to use it**: Always. After clustering, you must describe the "profile" of each group.
- **Common trap**: Relying only on mathematical metrics. A mathematically "perfect" clustering that groups customers in a way that doesn't lead to different actions is useless.

---

### Next Steps

Always check the [Before Evaluation Checklist](../checklists/before-evaluation.md) and remember that clustering is often an exploratory step, not a final answer.
- Review the [Evaluation and Monitoring](../concepts/evaluation-and-monitoring.md) concept for the full lifecycle.
