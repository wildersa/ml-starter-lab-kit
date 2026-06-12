import argparse
import sys
import importlib
from pathlib import Path

def run_check():
    from . import guide
    guide.main()

def run_eda():
    try:
        eda = importlib.import_module(".eda", package=__package__)
        eda.run_eda()
    except ImportError:
        print("\n[INFO] EDA module is not enabled in this project.")
        print("To enable it, generate a project with the 'recommended' or 'full' profile,")
        print("or manually add an eda.py module.")

def run_advisor():
    try:
        advisor = importlib.import_module(".advisor", package=__package__)
        advisor.main()
    except ImportError:
        print("\n[INFO] Dataset Advisor is not enabled in this project.")
        print("To enable it, generate a project with the 'guided' mode or 'recommended' profile.")

def run_learn():
    try:
        learning = importlib.import_module(".learning", package=__package__)
        learning.main()
    except ImportError:
        print("\n[INFO] Learning Notes module is not enabled in this project.")
        print("To enable it, generate a project with the 'guided' mode or 'recommended' profile.")

def run_baseline():
    try:
        baseline = importlib.import_module(".baseline_lab", package=__package__)
        baseline.main()
    except ImportError:
        print("\n[INFO] Baseline Lab is not enabled in this project.")
        print("To enable it, generate a project with the 'guided' mode or 'recommended' profile.")

def run_bandit():
    try:
        bandit = importlib.import_module(".bandit_lab", package=__package__)
        bandit.main()
    except ImportError:
        print("\n[INFO] Multi-Armed Bandit Lab is not enabled in this project.")
        print("To enable it, generate a project with the 'guided' mode or 'full' profile.")

def run_monitor():
    try:
        monitor = importlib.import_module(".monitor", package=__package__)
        monitor.main()
    except ImportError:
        print("\n[INFO] Monitoring stub is not enabled in this project.")
        print("To enable it, generate a project with the 'guided' mode or 'recommended' profile.")

{% if GENERATE_BANDIT == "true" %}
def run_bandit_dashboard():
    # Bandit Dashboard is a Streamlit app named bandit_dashboard.py inside the package
    pkg_dir = Path(__file__).parent
    dashboard_path = pkg_dir / "bandit_dashboard.py"

    if dashboard_path.exists():
        print("\n[INFO] Bandit Lab dashboard found.")
        print("Run it with:")
        print(f"  streamlit run {dashboard_path}")
    else:
        print("\n[INFO] Bandit Lab dashboard is not available in this project.")
        print("To enable it, generate a project with 'Guided Learning Mode' or the 'full' profile.")
{% endif %}

def run_train():
    from . import train
    train.main()

def run_evaluate():
    from . import evaluate
    evaluate.main()

def run_all():
    print("\n>>> Running Full Pipeline: check -> eda -> train -> evaluate")
    run_check()

    # Optional EDA
    try:
        importlib.import_module(".eda", package=__package__)
        print("\n>>> Step: EDA")
        run_eda()
    except ImportError:
        pass

    print("\n>>> Step: Training")
    run_train()
    print("\n>>> Step: Evaluation")
    run_evaluate()

def run_workspace():
    # Workspace is a Streamlit app named learning_workspace.py inside the package
    pkg_dir = Path(__file__).parent
    workspace_path = pkg_dir / "learning_workspace.py"

    if workspace_path.exists():
        print("\n[INFO] Streamlit workspace found.")
        print("Run it with:")
        print(f"  streamlit run {workspace_path}")
    else:
        print("\n[INFO] Streamlit workspace is not available in this project.")
        print("Guided Learning Mode projects include a workspace for interactive exploration.")
        print("You can create one by running a new generation with 'Guided Learning Mode'.")

def main():
    parser = argparse.ArgumentParser(
        description="Unified CLI for {{PROJECT_NAME}} ML pipeline.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    subparsers.add_parser("check", help="Run dataset and configuration readiness check")
    subparsers.add_parser("eda", help="Run exploratory data analysis")
    subparsers.add_parser("advisor", help="Run Dataset Advisor for modeling suggestions")
    subparsers.add_parser("learn", help="Generate dataset-contextual learning notes")
    subparsers.add_parser("baseline", help="Run Baseline Lab for simple model benchmarking")
    subparsers.add_parser("bandit", help="Run educational Multi-Armed Bandit Lab")
    subparsers.add_parser("monitor", help="Run educational monitoring/drift stub")
    {% if GENERATE_BANDIT == "true" %}
    subparsers.add_parser("bandit-dashboard", help="Visual explorer for Bandit Lab results")
    {% endif %}
    subparsers.add_parser("train", help="Train the baseline model")
    subparsers.add_parser("evaluate", help="Evaluate the model performance")
    subparsers.add_parser("all", help="Run the full pipeline (check, eda, train, evaluate)")
    subparsers.add_parser("workspace", help="Interactive Streamlit workspace guidance")

    args = parser.parse_args()

    if args.command == "check":
        run_check()
    elif args.command == "eda":
        run_eda()
    elif args.command == "advisor":
        run_advisor()
    elif args.command == "learn":
        run_learn()
    elif args.command == "baseline":
        run_baseline()
    elif args.command == "bandit":
        run_bandit()
    elif args.command == "monitor":
        run_monitor()
    {% if GENERATE_BANDIT == "true" %}
    elif args.command == "bandit-dashboard":
        run_bandit_dashboard()
    {% endif %}
    elif args.command == "train":
        run_train()
    elif args.command == "evaluate":
        run_evaluate()
    elif args.command == "all":
        run_all()
    elif args.command == "workspace":
        run_workspace()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
