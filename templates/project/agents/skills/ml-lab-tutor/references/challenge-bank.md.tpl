# Challenge Bank

Use these challenges to prompt the learner at different stages of the project.

## 1. Data Understanding & EDA
- **"The Hidden Signal"**: Can you find three features that correlate most with the target? Why do you think they are predictive?
- **"Quality Check"**: Are there missing values or outliers? How should we handle them?
- **"Leakage Hunter"**: Is there any feature that "knows too much" about the future or the target?

## 2. Preprocessing & Features
- **"Feature Crafting"**: Create a new feature that combines two existing ones. Does it improve the model's signal?
- **"Scaling Impact"**: Try training the baseline with and without feature scaling. Does it change the results?

## 3. Modeling & Evaluation
- **"The Simple Rival"**: Can you beat the baseline model with just one new feature or a different simple algorithm?
- **"Metric Tension"**: If we maximize Precision, what happens to Recall? Which is more important for our scenario?
- **"Bias Check"**: Does the model perform significantly worse on a specific segment of the data (e.g., a certain age group)?

## 4. Task-Specific Challenges
- **Time Series**: What happens if we use a random split instead of a temporal split? Why is this a problem?
- **Bandits**: Can you identify a situation where the current policy would explore too much (becoming inefficient)?
- **Unsupervised**: If we change the number of clusters (K), do the results still make sense business-wise?
