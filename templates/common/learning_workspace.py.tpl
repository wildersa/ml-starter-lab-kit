import streamlit as st
import pandas as pd
import json
from pathlib import Path
import importlib
import sys

# Setup path for local imports
# We expect to be in src/{{PACKAGE_NAME}}/learning_workspace.py
pkg_dir = Path(__file__).resolve().parent
src_dir = pkg_dir.parent

if str(src_dir) not in sys.path:
    sys.path.append(str(src_dir))

try:
    # Try absolute import via package name
    module_name = "{{PACKAGE_NAME}}"
    config_mod = importlib.import_module(f"{module_name}.config")
    load_config = config_mod.load_config
    project_root = config_mod.project_root
    get_mlflow_status = getattr(config_mod, "get_mlflow_status", None)

    readiness_mod = importlib.import_module(f"{module_name}.core.readiness")
    check_dataset_readiness = readiness_mod.check_dataset_readiness
except ImportError:
    # Fallback to local imports if package structure is not found as expected
    try:
        from config import get_mlflow_status, load_config, project_root
        from core.readiness import check_dataset_readiness
    except ImportError as e:
        st.error(f"Could not import project modules: {e}")
        st.stop()

# Page config
st.set_page_config(
    page_title="{{PROJECT_NAME}} - Learning Workspace",
    page_icon="🎓",
    layout="wide"
)

def main():
    st.title("🎓 {{PROJECT_NAME}} Learning Workspace")
    st.markdown("""
    Welcome to your **Guided Learning Workspace**! This tool helps you navigate the ML pipeline
    visually and understand each step of the process.
    """)

    # Sidebar
    st.sidebar.title("Navigation")
    section = st.sidebar.radio(
        "Go to",
        [
            "Setup Check",
            "Guided EDA",
            "Learning Notes",
            "Target Analysis",
            "Feature Explorer",
            "Model Suggestions",
            "Baseline Lab",
            {% if GENERATE_BANDIT == "true" %}
            "Bandit Lab",
            {% endif %}
            "Train & Evaluate",
            "Experiments & MLflow"
        ]
    )

    try:
        config = load_config()
    except Exception as e:
        st.error(f"Error loading config: {e}")
        st.stop()

    data_config = config.get("data", {})
    raw_path_str = data_config.get("raw_path", "data/raw/dataset.csv")
    data_path = project_root() / raw_path_str

    if section == "Setup Check":
        st.header("🔍 Setup Check")
        st.write(f"Checking dataset at: `{raw_path_str}`")

        readiness = check_dataset_readiness(data_path)

        if readiness.get("exists"):
            st.success("Dataset found!")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Sample Rows", readiness.get("sample_count", 0))
            with col2:
                st.metric("Columns Found", len(readiness.get("columns", {})))

            st.subheader("Column Information")
            st.table(pd.DataFrame.from_dict(readiness.get("columns", {}), orient='index'))
        else:
            st.warning("Dataset not found.")
            st.info(f"Please place your dataset at `{raw_path_str}` and refresh this page.")
            st.markdown("""
            **Recommended Action:**
            If you enabled the demo dataset during generation, it should be at `data/raw/demo_dataset.csv`.
            You can update `configs/config.json` to point to it.
            """)

    elif section == "Guided EDA":
        st.header("📊 Guided EDA")
        st.write("Exploratory Data Analysis helps you understand patterns and issues in your data.")

        eda_summary_path = project_root() / "configs/eda_summary.json"
        if eda_summary_path.exists():
            with open(eda_summary_path, "r") as f:
                eda_summary = json.load(f)
            st.success("EDA Summary loaded.")
            st.json(eda_summary)
        else:
            st.info("No EDA summary found yet.")
            st.markdown(f"""
            To generate a visual summary, run:
            ```bash
            python -m {{PACKAGE_NAME}}.lab eda
            ```
            Then refresh this page to see the results.
            """)

    elif section == "Learning Notes":
        st.header("📚 Learning Notes")
        st.write("Understand ML concepts through the lens of your own data.")

        eda_summary_path = project_root() / "configs/eda_summary.json"
        learning_report = project_root() / "reports/learning-notes.md"

        if not eda_summary_path.exists():
            st.warning("📊 **EDA Required**: Learning notes require data analysis first.")
            st.markdown(f"""
            Please run the EDA step first:
            ```bash
            python -m {{PACKAGE_NAME}}.lab eda
            ```
            """)
        elif learning_report.exists():
            st.success("Contextual learning notes found.")
            st.markdown(learning_report.read_text())
        else:
            st.info("Generate your contextual learning notes:")
            st.code(f"python -m {{PACKAGE_NAME}}.lab learn")
            st.write("Then refresh this page to see the notes.")

    elif section == "Target Analysis":
        st.header("🎯 Target Analysis")
        target_col = config.get("target", {}).get("column")
        if target_col:
            st.write(f"Configured target: **{target_col}**")
            st.info("Target analysis helps you understand the balance and distribution of what you want to predict.")
            st.write("Check if your target has missing values or extreme outliers (for regression).")
        else:
            st.warning("No target column configured in `configs/config.json`.")

    elif section == "Feature Explorer":
        st.header("🧪 Feature Explorer")
        st.write("Explore relationships between your features and the target.")
        st.info("Use this section to identify which columns might be most useful for your model.")
        st.markdown("""
        **Common things to check:**
        - High correlation between features (redundancy)
        - Correlation between features and target (predictive power)
        - Missing values in important features
        """)

    elif section == "Model Suggestions":
        st.header("💡 Model Suggestions")
        st.write("Recommendations based on your problem framing and data profile.")

        eda_summary_path = project_root() / "configs/eda_summary.json"
        advisor_report = project_root() / "reports/dataset-advice.md"

        if not eda_summary_path.exists():
            st.warning("📊 **EDA Required**: Exploratory Data Analysis (EDA) is required before generating suggestions.")
            st.markdown(f"""
            Suggestions must be data-driven. Please run the EDA step first to understand your dataset characteristics:
            ```bash
            python -m {{PACKAGE_NAME}}.lab eda
            ```
            Then refresh this page to continue.
            """)
        elif advisor_report.exists():
            try:
                st.success("Dataset Advisor report found.")
                st.markdown(advisor_report.read_text())
            except Exception:
                st.warning("Could not read the Advisor suggestions report.")
        else:
            st.info("Run the Dataset Advisor to get modeling suggestions based on your data:")
            st.code(f"python -m {{PACKAGE_NAME}}.lab advisor")

    elif section == "Baseline Lab":
        st.header("🔬 Baseline Lab")
        st.write("Start with simple models to establish a 'floor' for performance.")

        eda_summary_path = project_root() / "configs/eda_summary.json"
        baseline_results_path = project_root() / "configs/baseline_results.json"
        baseline_report_path = project_root() / "reports/baseline-results.md"

        if not eda_summary_path.exists():
            st.warning("📊 **EDA Required**: We recommend running EDA before starting your baseline experiments.")
            st.markdown(f"""
            Understanding your data distribution and missing values is crucial for setting up a proper baseline.
            ```bash
            python -m {{PACKAGE_NAME}}.lab eda
            ```
            """)
        elif baseline_report_path.exists():
            st.success("Baseline results found.")
            st.markdown(baseline_report_path.read_text())

            if baseline_results_path.exists():
                with open(baseline_results_path, "r") as f:
                    baseline_results = json.load(f)
                st.subheader("Raw Metrics")
                st.json(baseline_results)
        else:
            st.info("Run the Baseline Lab to establish a performance benchmark:")
            st.code(f"python -m {{PACKAGE_NAME}}.lab baseline")

            st.markdown("""
            **Why a baseline?**
            You should always know how a simple model (like a Mean/Mode predictor or a Linear Regression)
            performs before trying complex algorithms. Any real model must significantly outperform this baseline.
            """)

    {% if GENERATE_BANDIT == "true" %}
    elif section == "Bandit Lab":
        st.header("🎰 Multi-Armed Bandit Lab")
        st.markdown("""
        **Multi-Armed Bandits (MAB)** are a different paradigm from supervised learning.
        While supervised learning focuses on predicting a target from features, MAB focuses on
        **sequential decision learning** under uncertainty.

        In this lab, you simulate a scenario where you must choose between multiple 'arms' (actions)
        to maximize a reward. It is a core concept in Reinforcement Learning and A/B Testing.
        """)

        bandit_results_path = project_root() / "configs/bandit_results.json"
        bandit_report_path = project_root() / "reports/bandit-results.md"
        bandit_history_path = project_root() / "reports/bandit-history.csv"

        if bandit_report_path.exists():
            st.success("Bandit simulation results found.")

            # Summary charts
            if bandit_history_path.exists():
                try:
                    df = pd.read_csv(bandit_history_path)
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("Cumulative Reward")
                        reward_df = df.pivot(index="round", columns="policy", values="cumulative_reward")
                        st.line_chart(reward_df)
                    with col2:
                        st.subheader("Cumulative Regret")
                        regret_df = df.pivot(index="round", columns="policy", values="cumulative_regret")
                        st.line_chart(regret_df)

                    st.info("💡 **Tip**: For more detailed analysis, use the standalone dashboard:")
                    st.code(f"python -m {{PACKAGE_NAME}}.lab bandit-dashboard")
                except Exception as e:
                    st.error(f"Error loading charts: {e}")

            st.markdown(bandit_report_path.read_text())

            if bandit_results_path.exists():
                with open(bandit_results_path, "r") as f:
                    bandit_results = json.load(f)
                st.subheader("Raw Metrics")
                st.json(bandit_results)
        else:
            st.info("Run the Bandit Lab simulation to see results:")
            st.code(f"python -m {{PACKAGE_NAME}}.lab bandit")

            st.markdown("""
            **What is the goal?**
            You want to find the best-performing action (arm) while minimizing the cost of
            exploring sub-optimal ones. This is known as the **Exploration-Exploitation trade-off**.
            """)
    {% endif %}

    elif section == "Train & Evaluate":
        st.header("🚀 Train & Evaluate")
        st.write("The core cycle of Machine Learning.")

        st.subheader("Training")
        st.write("Training uses historical data to teach the model patterns.")
        st.code(f"python -m {{PACKAGE_NAME}}.lab train")

        st.subheader("Evaluation")
        st.write("Evaluation tests how well the model generalizes to new, unseen data.")
        st.code(f"python -m {{PACKAGE_NAME}}.lab evaluate")

    elif section == "Experiments & MLflow":
        st.header("📈 Experiments & MLflow")
        # MLflow status lookup - prioritize enabled_mlflow from generator, with fallback for nested structure
        if get_mlflow_status:
            mlflow_enabled = get_mlflow_status(config)
        else:
            # Inline fallback for cases where the helper is missing
            mlflow_enabled = config.get("tracking", {}).get("enabled_mlflow")
            if mlflow_enabled is None:
                mlflow_enabled = config.get("tracking", {}).get("mlflow", {}).get("enabled", False)

        if mlflow_enabled:
            st.success("MLflow tracking is enabled for this project!")
            st.write("All your training runs and metrics are being recorded.")
            st.markdown("""
            To see your experiment dashboard, run:
            ```bash
            mlflow ui
            ```
            And open http://localhost:5000
            """)
        else:
            st.info("MLflow tracking is not enabled for this project.")
            st.write("In Minimal Starter, we keep dependencies light. Guided Mode usually enables this for learning.")

if __name__ == "__main__":
    main()
