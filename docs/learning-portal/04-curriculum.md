# Curriculum

## Curriculum design rule

The curriculum is a dependency map, not a mandatory single path.

Some learners may enter with existing competencies. The portal should eventually allow validation/placement instead of forcing every node from the beginning.

The sequences below define an initial teaching order and prerequisite logic.

---

# 1. Shared foundations

## Python and data foundations

Teach only what is needed to unlock ML work.

Proposed order:

1. Python values and basic types
2. collections needed for data work
3. functions and reusable operations
4. NumPy arrays and vectorized thinking
5. pandas Series and DataFrame
6. rows, columns, observations, variables
7. selecting/filtering data
8. missing data basics
9. basic aggregation
10. basic visualization

This is not intended to become a complete Python course.

## Data understanding

1. dataset
2. observation / row
3. variable / column
4. feature
5. target
6. numerical vs categorical variables
7. data types vs semantic meaning
8. missing values
9. distribution
10. outliers
11. correlation
12. leakage introduction

## Mathematical and statistical foundations

Only concepts that materially support later ML skills should be required.

Initial sequence:

1. mean / median
2. variance / standard deviation
3. percentiles
4. probability intuition
5. conditional probability intuition
6. distributions
7. distance
8. vectors
9. basic matrix intuition
10. function intuition
11. loss / error intuition
12. gradient intuition

The objective is conceptual readiness, not a general mathematics curriculum.

---

# 2. Classical ML foundations

1. what an ML problem is
2. supervised vs unsupervised learning
3. regression vs classification
4. train / validation / test
5. baseline
6. preprocessing
7. feature engineering
8. leakage
9. evaluation workflow
10. reproducibility

## Classification branch

1. classes and decision boundaries
2. confusion matrix
3. accuracy
4. precision
5. recall
6. F1
7. thresholds
8. class imbalance
9. logistic regression intuition
10. decision trees
11. Random Forest
12. boosting
13. XGBoost / gradient boosting libraries
14. model comparison
15. cross-validation
16. hyperparameter tuning
17. feature importance
18. interpretability basics

## Regression branch

1. continuous targets
2. error/residual intuition
3. MAE
4. MSE / RMSE
5. R² intuition
6. linear regression
7. tree regression
8. Random Forest regression
9. boosting regression
10. cross-validation
11. hyperparameter tuning
12. residual analysis

## Unsupervised branch

1. similarity and distance
2. clustering intuition
3. K-Means assignment
4. centroid update
5. choosing K
6. cluster interpretation
7. scaling impact
8. dimensionality intuition
9. PCA
10. anomaly detection introduction

---

# 3. Reinforcement Learning

The initial RL line should make the decision-process model explicit before algorithms.

## RL foundations

1. agent
2. environment
3. state
4. observation
5. action
6. reward
7. episode
8. trajectory
9. return
10. discount factor
11. Markov property
12. MDP
13. policy
14. state-value function `V`
15. action-value function `Q`

## Value and Bellman branch

1. expected return intuition
2. Bellman expectation relationship
3. one-state Bellman backup by hand
4. Bellman optimality intuition
5. policy evaluation
6. policy improvement
7. value iteration
8. policy iteration

## Learning from experience branch

1. model-based vs model-free intuition
2. Monte Carlo prediction
3. Temporal Difference intuition
4. TD target / TD error
5. exploration vs exploitation
6. epsilon-greedy
7. SARSA
8. Q-Learning

## Deep RL convergence

Deep RL should require skills from both RL and neural-network branches.

Example dependency:

```text
Q-Learning + Neural Networks -> DQN
```

Later nodes may include:

1. function approximation
2. DQN
3. replay buffer
4. target networks
5. policy gradients
6. actor-critic
7. PPO

Deep RL ordering should be validated separately before becoming an implementation contract.

---

# 4. Deep Learning

Initial branch:

1. neuron / linear combination
2. activation functions
3. loss
4. weight update intuition
5. gradient descent
6. forward pass
7. backpropagation intuition
8. training loop
9. overfitting
10. regularization
11. train/eval modes
12. dense networks

Then branch into:

- computer vision / CNN;
- sequence models;
- transformers;
- deep RL prerequisite nodes.

---

# 5. Time series

Initial sequence:

1. time ordering
2. trend
3. seasonality
4. lag
5. rolling statistics
6. time-aware train/test split
7. leakage in temporal data
8. naive baseline
9. error metrics
10. feature-based forecasting
11. classical forecasting methods
12. neural forecasting introduction

---

# 6. Computer vision

Initial sequence:

1. image as data
2. pixels / channels
3. normalization
4. labels
5. train/validation/test for image datasets
6. augmentation
7. convolution intuition
8. filters
9. feature maps
10. pooling
11. CNN training
12. transfer learning
13. evaluation and error inspection

---

# 7. MLOps and experimentation

This track should connect back to experiments created in the starter project.

Initial sequence:

1. reproducible experiment
2. config vs code
3. data/version awareness
4. experiment metadata
5. metrics and artifacts
6. experiment comparison
7. model persistence
8. model card
9. pipeline concept
10. training pipeline
11. validation gates
12. deployment concepts
13. monitoring
14. drift
15. retraining triggers
16. lineage and governance basics

---

# Example cross-track dependencies

- Classification Metrics -> Model Monitoring
- Data Quality -> Drift
- Experiment Tracking -> MLOps Pipelines
- Neural Networks + Q-Learning -> DQN
- Probability + Sequential Decision Concepts -> RL Foundations
- Distance + Data Scaling -> K-Means
- Tree Models -> Random Forest -> Gradient Boosting

## Curriculum authoring rule

A curriculum entry should become a skill node only if there is something the learner can demonstrably understand or perform.

Do not create nodes merely to reproduce textbook chapter headings.