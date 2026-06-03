# Unsupervised Learning

Use unsupervised learning when you do not have a target column.

The goal is usually to discover structure in the data.

Examples:

- group similar customers;
- reduce dimensions;
- find unusual patterns;
- visualize high-dimensional data.

## Common techniques

| Technique | Use for |
|---|---|
| K-Means | simple clustering |
| PCA | dimensionality reduction |
| DBSCAN | density-based clustering |
| Isolation Forest | anomaly detection |

## Typical workflow

```text
data -> EDA -> preprocessing -> scaling -> dimensionality reduction -> clustering -> interpretation
```

## PCA in one sentence

PCA creates new columns that preserve as much variance as possible with fewer dimensions.

## K-Means in one sentence

K-Means separates data into K groups by distance to cluster centers.

## Important preprocessing note

Scaling is usually important for K-Means, PCA, KNN, DBSCAN, and other distance/variance-based techniques.

See [preprocessing](../workflows/preprocessing.md) and [clustering metrics](../metrics/clustering.md).

## Common mistakes

- Forgetting to scale numeric features.
- Treating clusters as absolute truth.
- Choosing K without analysis.
- Using too many noisy features.

## Practical advice

Unsupervised models usually need interpretation. The model gives groups; you still need to explain what those groups mean.
