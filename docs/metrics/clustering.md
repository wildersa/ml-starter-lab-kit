# Clustering Metrics

Clustering is unsupervised, meaning there is no "right answer" to compare against. Evaluation is about finding patterns that make sense for the business.

For a deeper dive into how to measure model performance and how it relates to business value, see the [Evaluation and Monitoring](../concepts/evaluation-and-monitoring.md) guide.

## Inertia (Within-cluster Sum of Squares)

- **What it answers:** How tightly packed are the clusters?
- **When to use:** In K-Means, to help choose the number of clusters (the "Elbow Method").
- **When to avoid:** When your clusters have irregular shapes (not spherical).
- **Common trap:** Assuming lower inertia always means better clusters. A model with as many clusters as data points has zero inertia but is useless.
- **Example:** In customer segmentation, seeing how inertia drops as you move from 2 to 5 clusters.

## Silhouette Score

- **What it answers:** How well-separated are the clusters? (Are points much closer to their own cluster than to others?)
- **When to use:** To evaluate the quality of a clustering without knowing the ground truth. It ranges from -1 to 1.
- **When to avoid:** On very large datasets, as it can be computationally expensive to calculate.
- **Common trap:** Relying solely on the average score. You should also look at the silhouette plot for each cluster to ensure they are all "healthy".
- **Example:** A score of 0.6 suggests strong structure, while 0.2 suggests significant overlap.

## Qualitative Cluster Interpretation

- **What it answers:** Do these groups actually mean anything for the business?
- **When to use:** Always. After clustering, you must "profile" the clusters by looking at the averages of their features.
- **When to avoid:** Never.
- **Common trap:** Giving a cluster a name (e.g., "High Spenders") without verifying if they actually spend significantly more than the average.
- **Example:** Discovering that "Cluster 1" represents users who only visit on weekends and buy luxury items.
