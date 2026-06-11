# Demo Scenario: verification_proj

> **Important**: This dataset is **synthetic** and intended for **learning-only**. It does not represent real-world data and should not be used to draw valid business or scientific conclusions.

## Scenario: Bank Campaign (Classification)
This demo simulates a marketing campaign where the goal is to predict if a client will subscribe to a term deposit.

### Data Dictionary
| Column | Type | Description | Role |
|---|---|---|---|
| id | Numeric | Unique client identifier | ID |
| age | Numeric | Client age | Feature |
| job | Categorical | Type of job | Feature |
| balance | Numeric | Average yearly balance | Feature |
| subscribed | Categorical | Did the client subscribe? (yes/no) | **Target** |

## Intended Learning Path
1. Explore the `data/raw/demo_dataset.csv` file.
2. Run `python -m verification_pkg.guide` to validate the setup.
3. Use the provided notebooks to perform Exploratory Data Analysis (EDA).
4. Run the training script to see a baseline model in action.
