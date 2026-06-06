# Experiment Visualization Strategy

This document outlines the decision-making process for experiment visualization in the ML Starter Lab Kit. It defines the current "MLflow-first" approach and the criteria for considering a custom lightweight dashboard in the future.

## Decision: MLflow-First Strategy

The primary tool for experiment visualization and tracking in this project is **MLflow**.

MLflow is a mature, industry-standard tool that provides comprehensive tracking capabilities out of the box. For beginners, it offers a professional-grade experience with minimal setup, aligning with our goal of teaching best practices from the start.

### What MLflow Covers

The generated project's MLflow integration covers the following:

- **Runs**: Each execution of `train.py` or `evaluate.py` is recorded as a unique run.
- **Parameters**: Automatic logging of model type, dataset paths, and problem framing metadata.
- **Metrics**: Tracking of performance indicators like accuracy, precision, recall, and loss over time or across different experiments.
- **Artifacts**: Storage and versioning of trained models (`model.json`), datasets, and generated reports (`metrics.json`).
- **Local UI**: A built-in web dashboard accessible via `mlflow server` that allows for easy browsing of results.
- **Comparison Workflow**: Side-by-side comparison of multiple runs to visualize the impact of parameter changes or feature engineering.

## Future Consideration: Lightweight Custom Dashboard

While MLflow is powerful, we recognize it may have a steeper learning curve for absolute beginners or provide more complexity than needed for some "first-day" experiments.

### Potential Gaps for Beginners

A custom, lightweight dashboard might be justified if it addresses specific needs not easily met by MLflow:

- **Guided Diagnostic Interpretations**: Automated "plain English" summaries of why a run performed poorly (e.g., "The high gap between training and validation suggests overfitting").
- **Simplified Project "Status at a Glance"**: A single-page view that combines Dataset Advisor findings with the latest baseline performance.
- **Direct Integration with Starter-Specific Artifacts**: Deeply tailored views for the `reports/` folder contents that go beyond standard MLflow artifact previews.

### Decision Checklist for Future Implementation

Before opening an issue to implement a custom dashboard, the following criteria must be met:

1. [ ] **Identified Friction**: There is clear evidence that beginners find the MLflow UI confusing for the specific scope of this starter kit.
2. [ ] **Non-Duplicative**: The proposed dashboard feature cannot be easily replicated by an MLflow plugin or a simple custom artifact (like an HTML report) logged to MLflow.
3. [ ] **Zero-Dependency Goal**: The dashboard must not introduce heavy new dependencies (like Streamlit, FastAPI, or React) that would complicate the project's minimal setup.
4. [ ] **Educational Value**: The dashboard must prioritize teaching "what the numbers mean" over just "showing the numbers".

## Non-Goals

The following are explicitly **not** part of the current scope or planned dashboard work:

- **Implementing a custom web server/UI**: No dashboard code is being added at this time.
- **Replacing MLflow**: MLflow will remain the recommended path for professional-grade tracking.
- **Remote Tracking/Auth**: We focus on local, single-user experimentation.
- **Model Registry/Deployment**: Production-level model management is outside the scope of this starter kit.
