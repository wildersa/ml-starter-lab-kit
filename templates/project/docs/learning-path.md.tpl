# Learning Path: {{PROJECT_NAME}}

This guide helps you understand the workflow for this **{{TASK}}** project.

## 1. What is "{{TASK}}"?

{% if TASK == "supervised" %}
Supervised learning means training a model using examples where the answer (target) is already known. The model learns to map inputs (features) to the output.
{% else %}
{% if TASK == "unsupervised" %}
Unsupervised learning finds hidden patterns or structures in data without pre-defined labels. It is often used for grouping similar items or reducing complexity.
{% else %}
{% if TASK == "timeseries" %}
Time series analysis deals with data points collected or recorded at successive time intervals. The goal is often to forecast future values based on past behavior.
{% else %}
{% if TASK == "vision" %}
Computer Vision tasks involve teaching computers to "see" and interpret visual information from the world, such as classifying images or detecting objects.
{% else %}
{% if TASK == "bandit" %}
Multi-Armed Bandit (MAB) is a form of reinforcement learning where the system makes sequential decisions (choosing "arms") to maximize a reward while balancing exploration and exploitation.
{% else %}
A generic ML structure provides a standard organization for data, features, and modeling, applicable to various custom experimentation workflows.
{% endif %}
{% endif %}
{% endif %}
{% endif %}
{% endif %}

## 2. Understanding your data

In this context:
- **Rows**: {% if TASK == "bandit" %}Individual decision events or interactions.{% else %}Individual observations or samples.{% endif %}
- **Features**: The inputs used by the model to understand the data.
- **{{TARGET_COLUMN}}**: {% if TASK == "supervised" %}The target column you want to predict.{% else %}{% if TASK == "timeseries" %}The value to be forecasted over time.{% else %}{% if TASK == "bandit" %}The reward observed after taking an action.{% else %}{% if TASK == "unsupervised" %}There is no fixed target; we look at all features together.{% else %}The main column of interest for your task.{% endif %}{% endif %}{% endif %}{% endif %}
{% if TASK == "timeseries" %}
- **Time Index**: The column that defines the chronological order of events.
{% endif %}

## 3. The Role of the First Baseline

The first baseline is **not** your final model. Its purpose is to:
- Establish a "performance floor" (the minimum result any real model must beat).
- Verify that the data pipeline (loading, features, training) is working.
- Give you a reference point for future improvements.

{% if TASK == "supervised" %}
Common baselines: Predicting the average value (Regression) or the most frequent class (Classification).
{% else %}
{% if TASK == "bandit" %}
Common baselines: Randomly choosing actions or always choosing the historically best-performing action.
{% endif %}
{% endif %}

## 4. Metrics: What they do (and don't) prove

Useful metrics for this task include:
- {% if TASK == "supervised" %}**Accuracy/F1** (Classification) or **MAE/RMSE** (Regression).{% else %}{% if TASK == "timeseries" %}**MAPE/WAPE** for forecasting accuracy.{% else %}{% if TASK == "bandit" %}**Cumulative Reward** and **Regret**.{% else %}Task-specific performance indicators.{% endif %}{% endif %}{% endif %}

**Important**: A good metric score does not prove your model is "smart" or "fair". It only proves the model found a mathematical pattern in the provided dataset. Always check for biases.

## 5. Common Mistakes to Check

Before you spend time optimizing:
- **Target Leakage**: Are you using features that wouldn't be available at prediction time?
- **Imbalanced Data**: Is one class or scenario much more frequent than others?
- **Data Quality**: Are there missing values or outliers that shouldn't be there?
{% if TASK == "timeseries" %}
- **Chronological Leakage**: Did you accidentally use "future" data to predict the "past"?
{% endif %}

## 6. What's Next?

Once the baseline is running:
1. **Feature Engineering**: Create more meaningful inputs from your raw data.
2. **Error Analysis**: Look at where the model fails. Is there a pattern in the mistakes?
3. **Model Selection**: Try different algorithms (Linear, Trees, etc.).
4. **Hyperparameter Tuning**: Optimize the settings of your chosen model.
