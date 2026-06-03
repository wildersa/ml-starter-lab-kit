# Unsupervised Learning Pipeline

Use this when there is no target column.

Examples:

- customer segmentation;
- exploratory clustering;
- dimensionality reduction;
- anomaly discovery.

## Simplified flow

```mermaid
flowchart LR
    A[Raw data] --> B[EDA]
    B --> C[Cleaning]
    C --> D[Scaling]
    D --> E[PCA optional]
    E --> F[Clustering]
    F --> G[Cluster interpretation]
    G --> H[Report]
```

## Notes

- Scaling is usually important.
- PCA can help visualization and noise reduction.
- Clusters need interpretation.
- A cluster is not automatically a business segment.

See:

- [unsupervised learning](../models/unsupervised.md)
- [clustering metrics](../metrics/clustering.md)
