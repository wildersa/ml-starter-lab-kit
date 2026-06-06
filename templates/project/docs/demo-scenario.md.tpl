# Demo Scenario: {{PROJECT_NAME}}

> **Important**: This dataset is **synthetic** and intended for **learning-only**. It does not represent real-world data and should not be used to draw valid business or scientific conclusions.

{% if DEMO_SUBTYPE == "classification" %}
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
{% endif %}

{% if DEMO_SUBTYPE == "regression" %}
## Scenario: House Prices (Regression)
This demo simulates a real estate dataset where the goal is to predict the sale price of a house based on its characteristics.

### Data Dictionary
| Column | Type | Description | Role |
|---|---|---|---|
| id | Numeric | Unique house identifier | ID |
| sqft | Numeric | Square footage of the house | Feature |
| bedrooms | Numeric | Number of bedrooms | Feature |
| age | Numeric | Age of the house in years | Feature |
| price | Numeric | Sale price | **Target** |
{% endif %}

{% if DEMO_SUBTYPE == "unsupervised" %}
## Scenario: Customer Segmentation (Unsupervised)
This demo simulates customer data for clustering. The goal is to discover patterns or segments among customers without a predefined target.

### Data Dictionary
| Column | Type | Description | Role |
|---|---|---|---|
| customer_id | Numeric | Unique customer identifier | ID |
| age | Numeric | Customer age | Feature |
| annual_income | Numeric | Annual income | Feature |
| spend_score | Numeric | Score assigned by the shop based on customer behavior | Feature |

**Note**: As an unsupervised task, there is no target column. The goal is to find groupings.
{% endif %}

{% if DEMO_SUBTYPE == "timeseries" %}
## Scenario: Daily Sales (Time Series)
This demo simulates daily sales data. The goal is to understand temporal patterns and forecast future sales.

### Data Dictionary
| Column | Type | Description | Role |
|---|---|---|---|
| date | Date | The day of the record | Time Index |
| sales | Numeric | Units sold | **Target** |
| on_promotion | Categorical | Was there a promotion on that day? | Feature |

**Note**: This is a forecasting task where the relationship between date and value is key.
{% endif %}

{% if DEMO_SUBTYPE == "vision" %}
## Scenario: Image Metadata (Vision)
This demo simulates a metadata file for an image classification task.

> **Note**: This demo only includes the CSV metadata. It does **not** include real image files.

### Data Dictionary
| Column | Type | Description | Role |
|---|---|---|---|
| image_path | Text | Path to the image file | Reference |
| label | Categorical | Image category (cat, dog, bird) | **Target** |
| width | Numeric | Image width | Metadata |
| height | Numeric | Image height | Metadata |
{% endif %}

## Intended Learning Path
1. Explore the `data/raw/demo_dataset.csv` file.
2. Run `python -m {{PACKAGE_NAME}}.guide` to validate the setup.
3. Use the provided notebooks to perform Exploratory Data Analysis (EDA).
4. Run the training script to see a baseline model in action.
