# Implementation Spec: Feature Screening Lab

## 1. Purpose
The Feature Screening Lab is a diagnostic tool designed for pre-modeling feature analysis. Its primary goal is to help users identify the predictive power of individual features and detect potential data leakage before committing to full model training. It is NOT intended for final model training or hyperparameter optimization.

## 2. Intended User Flow
1. **Data Preparation**: User prepares a raw or processed dataset.
2. **Screening**: User runs the Feature Screening Lab to understand feature-target relationships.
3. **Analysis**: User reviews generated reports to decide which features to keep, transform, or investigate for leakage.
4. **Refinement**: User updates data preparation logic or configuration based on screening results.
5. **Training**: User proceeds to the training command with a refined feature set.

## 3. CLI Interface (Future)
The lab will be accessible via the unified CLI:
```bash
python -m <package>.lab feature-screening --data-path <path> --target <column> --task <type>
```

## 4. Required Inputs
- `dataset_path`: Path to the tabular file (e.g., CSV or Parquet) to analyze.
- `target_column`: The name of the column to predict.
- `problem_type`: `classification` or `regression`.
- `metric`: The primary metric for evaluation (e.g., ROC AUC, F1, RMSE, R-squared).
- `split_settings`: Configuration for train/validation split (e.g., 80/20).
- `max_rows` (optional): Limit the number of rows processed for faster diagnostics on large datasets.

## 5. Output Artifacts
- `reports/feature-screening-report.md`: A summary report containing the diagnostic results.
- `reports/feature-scores.csv`: A tabular breakdown of scores for every feature.
- `reports/feature-importance.png` (optional): A visualization of the most important features (if plotting dependencies are available).

## 6. Implementation Scope
### Phase 1 Scope (Current Spec)
- **Data Types**: Tabular data.
- **Tasks**: Supervised learning only (Binary/Multiclass Classification and Regression).

### Non-Goals for Phase 1
- Clustering or unsupervised feature discovery.
- Computer Vision (image-level features).
- Time Series (temporal dependencies and windowed features).
- Multi-Armed Bandits (reward-based importance).

## 7. Screening Strategies
The lab must support and distinguish between these three distinct concepts:
1. **Univariate Predictive Screening**: Evaluating each feature independently (e.g., fitting a simple model per feature) to measure its individual predictive power.
2. **Final-Model Feature Importance**: Extracting intrinsic importance scores from a baseline model (e.g., tree-based importance).
3. **Permutation Importance**: Measuring the drop in model performance when a feature's values are randomly shuffled, providing a model-agnostic view of feature dependency.

## 8. Leakage Warning Rules
The lab will implement automated warnings for:
- **Perfect/Near-Perfect Signal**: Features with suspicious performance (e.g., AUC > 0.99 or R2 > 0.99) that may indicate the target was leaked into the features.
- **Prediction-Time Availability**: Reminders to verify if high-performing features are actually available at the time of inference in production.

## 9. Dependency Policy
- **Generator Integrity**: The generator itself must remain dependency-free.
- **Runtime Dependencies**: The Feature Screening Lab will utilize project-level optional Machine Learning and Dataframe libraries only when the corresponding features are selected by the user during generation.

## 10. Future Test Plan
1. **CLI Wiring**: Verify the lab correctly routes the `feature-screening` command.
2. **Diagnostic Accuracy**: Test with synthetic datasets containing known "strong" features, "noisy" features, and "leaked" features to ensure correct identification.
3. **Artifact Generation**: Verify all CSV and Markdown reports are created in the correct reports directory.
4. **Boundary Checks**: Ensure the lab gracefully fails or warns when used with unsupported task types.
5. **Memory/Performance**: Verify `max_rows` correctly limits resource usage on large files.

## 11. Limitations
- Feature screening provides statistical correlations and predictive proxies, not causal relationships.
- High importance does not guarantee performance in a complex, multi-variable model environment where feature interactions are dominant.
- Screening results are dependent on the chosen metric and baseline model used for diagnostics.

## 12. Theory and References
For deeper theory on feature selection and importance, refer to established Machine Learning documentation and research papers on predictive feature analysis.
