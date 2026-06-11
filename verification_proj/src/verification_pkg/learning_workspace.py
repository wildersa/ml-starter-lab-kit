import streamlit as st
import pandas as pd
import json
from pathlib import Path
import importlib
import sys

# Setup path for local imports
# We expect to be in src/verification_pkg/learning_workspace.py
pkg_dir = Path(__file__).resolve().parent
src_dir = pkg_dir.parent

if str(src_dir) not in sys.path:
    sys.path.append(str(src_dir))

try:
    # Try absolute import via package name
    module_name = "verification_pkg"
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
    page_title="verification_proj - Learning Workspace",
    page_icon="🎓",
    layout="wide"
)

def render_project_doc(relative_path: str):
    """
    Safely reads and renders a project-local Markdown file.
    Only allows paths from a predefined allowlist of docs and reports.
    """
    # Define safe allowed paths
    allowed_paths = {
        # Docs
        "docs/evaluation.md",
        "docs/evaluation.pt-BR.md",
        "docs/monitoring.md",
        "docs/monitoring.pt-BR.md",
        "docs/mab-lab.md",
        "docs/mab-lab.pt-BR.md",
        "docs/data-dictionary.md",
        "docs/demo-scenario.md",
        "docs/demo-scenario.pt-BR.md",
        # Reports
        "reports/learning-notes.md",
        "reports/dataset-advice.md",
        "reports/baseline-results.md",
        "reports/bandit-results.md",
        "reports/evaluation-report.md",
        "reports/model-report.md",
        "reports/modeling-notes.md",
    }

    if relative_path not in allowed_paths:
        st.error(f"Access denied: {relative_path} is not in the allowlist.")
        return

    full_path = project_root() / relative_path

    if full_path.exists():
        try:
            content = full_path.read_text(encoding="utf-8")
            st.markdown(content)
        except Exception as e:
            st.warning(f"Could not read {relative_path}: {e}")
    else:
        st.info(f"💡 **Documentation not found**: `{relative_path}` does not exist yet.")
        if "reports/" in relative_path:
            st.write("This report is generated after you run the corresponding pipeline step.")

def main():
    st.title("🎓 verification_proj Learning Workspace")
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

            "Train & Evaluate",
            "Production & Monitoring",
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
            python -m verification_pkg.lab eda
            ```
            Then refresh this page to see the results.
            """)

    elif section == "Learning Notes":
        st.header("📚 Learning Notes")
        st.write("Understand ML concepts through the lens of your own data.")

        eda_summary_path = project_root() / "configs/eda_summary.json"

        if not eda_summary_path.exists():
            st.warning("📊 **EDA Required**: Learning notes require data analysis first.")
            st.markdown(f"""
            Please run the EDA step first:
            ```bash
            python -m verification_pkg.lab eda
            ```
            """)
        else:
            render_project_doc("reports/learning-notes.md")

            st.divider()
            st.subheader("How to refresh")
            st.info("If you updated your data or features, regenerate your contextual learning notes:")
            st.code(f"python -m verification_pkg.lab learn")

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

        if not eda_summary_path.exists():
            st.warning("📊 **EDA Required**: Exploratory Data Analysis (EDA) is required before generating suggestions.")
            st.markdown(f"""
            Suggestions must be data-driven. Please run the EDA step first to understand your dataset characteristics:
            ```bash
            python -m verification_pkg.lab eda
            ```
            Then refresh this page to continue.
            """)
        else:
            render_project_doc("reports/dataset-advice.md")

            st.divider()
            st.info("Run the Dataset Advisor to regenerate suggestions:")
            st.code(f"python -m verification_pkg.lab advisor")

    elif section == "Baseline Lab":
        st.header("🔬 Baseline Lab")

        eda_summary_path = project_root() / "configs/eda_summary.json"
        baseline_results_path = project_root() / "configs/baseline_results.json"

        if not eda_summary_path.exists():
            st.warning("📊 **EDA Required**: We recommend running EDA before starting your baseline experiments.")
            st.markdown(f"""
            Understanding your data distribution and missing values is crucial for setting up a proper baseline.
            ```bash
            python -m verification_pkg.lab eda
            ```
            """)
        else:
            render_project_doc("reports/baseline-results.md")

            if baseline_results_path.exists():
                with open(baseline_results_path, "r") as f:
                    baseline_results = json.load(f)
                with st.expander("Raw Metrics (JSON)"):
                    st.json(baseline_results)

            st.divider()
            st.info("Run the Baseline Lab to establish or update your performance benchmark:")
            st.code(f"python -m verification_pkg.lab baseline")

    elif section == "Train & Evaluate":
        st.header("🚀 Train & Evaluate")
        st.write("The core cycle of Machine Learning.")

        tabs = st.tabs(["Execution", "Concepts"])

        with tabs[0]:
            st.subheader("Training")
            st.write("Training uses historical data to teach the model patterns.")
            st.code(f"python -m verification_pkg.lab train")

            st.subheader("Evaluation")
            st.write("Evaluation tests how well the model generalizes to new, unseen data.")
            st.code(f"python -m verification_pkg.lab evaluate")

            st.divider()
            st.subheader("Latest Results")
            render_project_doc("reports/evaluation-report.md")

        with tabs[1]:
            lang_suffix = ".pt-BR" if "en" == "pt-BR" else ""
            render_project_doc(f"docs/evaluation{lang_suffix}.md")

    elif section == "Production & Monitoring":
        st.header("📡 Production & Monitoring")
        st.write("What happens after the model is ready?")

        lang_suffix = ".pt-BR" if "en" == "pt-BR" else ""
        render_project_doc(f"docs/monitoring{lang_suffix}.md")

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
