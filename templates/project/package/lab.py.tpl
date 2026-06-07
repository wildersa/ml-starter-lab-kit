from __future__ import annotations

import argparse
import sys
from typing import Callable

def run_check() -> None:
    from .guide import main
    main()

def run_eda() -> None:
    try:
        from .eda import main
        main()
    except ImportError:
        print("\n[!] EDA module not found.")
        print("This project was generated without EDA support or the file was removed.")

def run_advisor() -> None:
    try:
        from .advisor import main
        main()
    except ImportError:
        print("\n[!] Dataset Advisor module not found.")
        print("This project was generated without the Advisor or the file was removed.")

def run_train() -> None:
    from .train import main
    main()

def run_evaluate() -> None:
    from .evaluate import main
    main()

def run_all() -> None:
    print("\n=== Running All Project Steps ===")

    print("\n--- [1/4] Checking readiness ---")
    run_check()

    print("\n--- [2/4] Running EDA ---")
    run_eda()

    print("\n--- [3/4] Training baseline ---")
    run_train()

    print("\n--- [4/4] Evaluating results ---")
    run_evaluate()

    print("\n=== All steps completed ===")

def run_workspace() -> None:
    import os
    from pathlib import Path

    pkg_dir = Path(__file__).parent
    workspace_file = pkg_dir / "learning_workspace.py"

    print("\n--- ML Workspace ---")

    if workspace_file.exists():
        print("Starting Streamlit workspace...")
        # Since we don't want to add a hard dependency on streamlit in the generator
        # but the generated project might have it if the user installed it.
        print(f"Run the following command to start the UI:")
        print(f"  streamlit run {workspace_file}")
    else:
        print("Streamlit workspace not found in this project.")
        print("Guided Learning Mode projects include a workspace for visual exploration.")
        print("If you want to add one, you can create a Streamlit app that uses the project's core modules.")

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Unified Lab CLI for {{PROJECT_NAME}}",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", help="Project command to run")

    subparsers.add_parser("check", help="Check dataset and configuration readiness")
    subparsers.add_parser("eda", help="Run basic Exploratory Data Analysis")
    subparsers.add_parser("advisor", help="Run Dataset Advisor for modeling suggestions")
    subparsers.add_parser("train", help="Train the baseline model")
    subparsers.add_parser("evaluate", help="Evaluate the model performance")
    subparsers.add_parser("all", help="Run check, eda, train, and evaluate in sequence")
    subparsers.add_parser("workspace", help="Open the visual learning workspace (if available)")

    args = parser.parse_args()

    commands: dict[str, Callable[[], None]] = {
        "check": run_check,
        "eda": run_eda,
        "advisor": run_advisor,
        "train": run_train,
        "evaluate": run_evaluate,
        "all": run_all,
        "workspace": run_workspace,
    }

    if args.command in commands:
        commands[args.command]()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
