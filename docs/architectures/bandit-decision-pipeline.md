# Bandit Decision Pipeline

Use this when the system chooses between options and learns from feedback.

Examples:

- offer selection;
- banner selection;
- channel selection;
- message variation selection.

## Simplified flow

```mermaid
flowchart LR
    A[Context] --> B[Eligibility rules]
    B --> C[Available arms]
    C --> D[Bandit policy]
    D --> E[Decision log]
    E --> F[User interaction]
    F --> G[Reward event]
    G --> H[Policy update]
    H --> D
```

## Notes

- The decision must be logged.
- Rewards can be delayed.
- Exploration should be controlled.
- Fairness and suitability matter.

See:

- [bandits](../models/bandits.md)
- [bandit metrics](../metrics/bandits.md)
