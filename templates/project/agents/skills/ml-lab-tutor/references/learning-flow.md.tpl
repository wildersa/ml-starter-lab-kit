# Learning Flow

The project is structured around a recommended didactic progression. Help the user stay on track.

## Step-by-Step Progression

1.  **Onboarding (00)**: Understand the toolkit and set up the environment.
2.  **Data Understanding (01)**: Use Dataset Intelligence and the Data Dictionary to assess data quality and readiness.
3.  **Exploratory Data Analysis (02)**: Visualize distributions, correlations, and relationships to form hypotheses.
4.  **Preprocessing & Features (03)**: Prepare the data for modeling. The approach varies by task (e.g., temporal splits for time series).
5.  **Baseline Modeling (04)**: Establish a simple starting point (e.g., Logistic Regression, Naive Seasonal, or Fixed Policy) to set a benchmark.
6.  **Evaluation & Interpretation (05)**: Deep dive into metrics and model behavior (e.g., feature importance, error analysis).
7.  **Experiments & Reflection (06)**: Document iterations in `reports/experiment-notes.md` and plan next steps.

## When to Deviate

Users might jump ahead or need to backtrack.
- If they are struggling with modeling, suggest more EDA.
- If they have good results, suggest checking for leakage or bias.
- If they are using synthetic data, encourage them to "break" the data and see how the model reacts.
