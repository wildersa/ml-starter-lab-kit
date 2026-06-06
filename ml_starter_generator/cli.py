from __future__ import annotations

import re
import os
import sys
from pathlib import Path
from .constants import STARTER_ROOT, TASKS
from .config import create_config, create_problem_profile
from .scaffold import (
    create_dirs,
    create_readme,
    create_package_files,
    create_optional_files,
    create_tests,
    create_notebook_placeholder,
    create_docs,
    create_pyproject,
    create_env_files,
)

class UI:
    """Helper for terminal UI, colors, and sections."""
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    END = '\033[0m'

    @staticmethod
    def use_color() -> bool:
        """Check if colors should be used."""
        if os.getenv("NO_COLOR"):
            return False
        # If we are in a test or piped, isatty() might be False.
        # But for tests we might want to see colors or not.
        if not sys.stdout.isatty():
            return False
        if os.getenv("TERM") == "dumb":
            return False
        return True

    @classmethod
    def color(cls, text: str, color_code: str) -> str:
        if cls.use_color():
            return f"{color_code}{text}{cls.END}"
        return text

    @classmethod
    def section(cls, title: str, number: int) -> None:
        print()
        header = f"--- {number}. {title} ---"
        print(cls.color(header, cls.BLUE + cls.BOLD))

    @classmethod
    def panel(cls, title: str, text: str) -> None:
        print()
        print(cls.color(f"[{title}]", cls.CYAN + cls.BOLD))
        for line in text.strip().split('\n'):
            print(f"  {line.strip()}")

    @classmethod
    def success(cls, text: str) -> None:
        print(cls.color(f"✔ {text}", cls.GREEN))

    @classmethod
    def warning(cls, text: str) -> None:
        print(cls.color(f"⚠ {text}", cls.YELLOW))


def ask(prompt: str, default: str | None = None) -> str:
    suffix = f" [{UI.color(default, UI.CYAN)}]" if default else ""
    full_prompt = f"{prompt}{suffix}: "
    print(full_prompt, end="", flush=True)
    value = input().strip()
    return value or (default or "")


def ask_yes_no(prompt: str, default: bool = True) -> bool:
    default_label = "Y/n" if default else "y/N"
    colored_label = UI.color(default_label, UI.CYAN)
    full_prompt = f"{prompt} [{colored_label}]: "
    print(full_prompt, end="", flush=True)
    value = input().strip().lower()

    if not value:
        return default

    return value in {"y", "yes"}


def choose_task() -> str:
    print()
    print("Project Type (ML Task):")
    print("1. generic       - generic ML structure")
    print("2. supervised    - classification/regression")
    print("3. unsupervised  - PCA/K-Means/clustering")
    print("4. timeseries    - time series/LSTM")
    print("5. vision        - image classification/detection")

    while True:
        choice = ask("Choose an option", "2")
        if choice in TASKS:
            return TASKS[choice]
        if choice in TASKS.values():
            return choice
        print("Invalid option.")


def choose_python_profile() -> str:
    print()
    print("Python Profile:")
    print("1. safe   - Python 3.12 (stable)")
    print("2. modern - Python 3.14 (experimental/recent)")

    while True:
        choice = ask("Choose an option", "1")
        if choice == "1" or choice == "safe":
            return "3.12"
        if choice == "2" or choice == "modern":
            return "3.14"
        print("Invalid option.")


def choose_torch_variant() -> str:
    print()
    print("PyTorch Support:")
    print("1. none     - Do not include Torch")
    print("2. cpu      - Torch for CPU")
    print("3. cuda126  - Torch for CUDA 12.6")
    print("4. cuda128  - Torch for CUDA 12.8")

    mapping = {
        "1": "none",
        "2": "cpu",
        "3": "cu126",
        "4": "cu128"
    }

    while True:
        choice = ask("Choose an option", "1")
        if choice in mapping:
            return mapping[choice]
        if choice in mapping.values():
            return choice
        print("Invalid option.")


def choose_optional_profile() -> str:
    print()
    print("Optional Template Profile:")
    print("1. minimal     - no optional templates")
    print("2. recommended - eda, preprocessing, metrics, visualization")
    print("3. full        - all optional templates")
    print("4. custom      - select templates individually")

    while True:
        choice = ask("Choose an option", "2")
        if choice in {"1", "2", "3", "4"}:
            mapping = {"1": "minimal", "2": "recommended", "3": "full", "4": "custom"}
            return mapping[choice]
        if choice in {"minimal", "recommended", "full", "custom"}:
            return choice
        print("Invalid option.")


def get_options_by_profile(profile: str) -> dict[str, bool]:
    options = {
        "eda": False,
        "preprocessing": False,
        "metrics": False,
        "optimization": False,
        "feature_measurement": False,
        "visualization": False,
        "notebook_factory": False,
        "model_report": False,
        "experiment_log": False,
        "advisor": False,
    }

    if profile == "minimal":
        return options

    if profile == "recommended":
        options["eda"] = True
        options["preprocessing"] = True
        options["metrics"] = True
        options["visualization"] = True
        options["advisor"] = True
        return options

    if profile == "full":
        for key in options:
            options[key] = True
        return options

    return options


def run_problem_framing_wizard(task: str) -> dict[str, str]:
    UI.panel("Problem Framing", "This optional wizard helps configure the starter kit to your specific goals.")
    print("Press Enter to use defaults.")

    # 1. Main goal?
    print("\n1. Main goal?")
    goals = {
        "supervised": "predict a category",
        "unsupervised": "group similar records",
        "timeseries": "forecast future values",
        "vision": "work with images/text",
        "generic": "predict a category"
    }
    default_goal = goals.get(task, "predict a category")
    print(f"   - predict a category")
    print(f"   - predict a number")
    print(f"   - group similar records")
    print(f"   - forecast future values")
    print(f"   - work with images/text")
    goal = ask("Goal", default_goal)

    # 2. What matters most?
    print("\n2. What matters most?")
    print("   - interpretability")
    print("   - predictive performance")
    print("   - speed/simplicity")
    print("   - handling imbalanced classes")
    print("   - learning/experimentation")
    priority = ask("Priority", "learning/experimentation")

    # 3. Which error is more costly?
    print("\n3. Which error is more costly?")
    print("   - false positive")
    print("   - false negative")
    print("   - both similar")
    print("   - not sure")
    error_cost = ask("Error cost", "not sure")

    # 4. Expected dataset size?
    print("\n4. Expected dataset size?")
    print("   - small")
    print("   - medium")
    print("   - large")
    print("   - not sure")
    dataset_size = ask("Size", "not sure")

    # 5. Prefer simple baseline first?
    prefer_baseline = "yes" if ask_yes_no("\n5. Prefer simple baseline first?", True) else "no"

    # 6. Any domain note?
    domain_note = ask("\n6. Any domain note? (optional)", "")

    return {
        "goal": goal,
        "priority": priority,
        "error_cost": error_cost,
        "dataset_size": dataset_size,
        "prefer_baseline": prefer_baseline,
        "domain_note": domain_note
    }


def normalize_package_name(value: str) -> str:
    value = value.strip().lower().replace("-", "_").replace(" ", "_")
    value = re.sub(r"[^a-z0-9_]", "", value)
    value = re.sub(r"_+", "_", value).strip("_")

    if not value:
        value = "ml_project"

    if value[0].isdigit():
        value = f"ml_{value}"

    return value


def print_summary(root: Path, values: dict[str, str]) -> None:
    UI.success("Starter-kit created successfully!")
    print(f"Destination: {UI.color(str(root.resolve()), UI.CYAN)}")
    print()
    UI.panel("Next steps",
             f"1. Place your dataset at: {values['DATASET_PATH']}\n"
             f"2. Review and adjust metadata in: configs/config.json\n"
             f"3. Define your features in: src/{values['PACKAGE_NAME']}/features.py\n"
             f"4. Run the pipeline:\n"
             f"   - Step 1 (Data):     python -m {values['PACKAGE_NAME']}.data\n"
             f"   - Step 2 (Train):    python -m {values['PACKAGE_NAME']}.train\n"
             f"   - Step 3 (Evaluate): python -m {values['PACKAGE_NAME']}.evaluate")

    if values.get("ADVISOR_COMMAND"):
        print(f"   - Dataset Advice:   {values['ADVISOR_COMMAND']}")


def main() -> None:
    print(UI.color("ML Starter Kit Builder", UI.BLUE + UI.BOLD))
    print(UI.color("======================", UI.BLUE + UI.BOLD))

    UI.section("Project basics", 1)
    default_project = Path.cwd().name
    project_name = ask("Project name", default_project)
    package_name = normalize_package_name(
        ask("Python package name", normalize_package_name(project_name))
    )
    task = choose_task()
    preset = "none"

    UI.section("Dataset and target", 2)
    if task == "supervised":
        UI.panel("Supervised Learning",
                 "In supervised learning, you need a 'target' column (what you want to predict)\n"
                 "and 'features' (the data used to make the prediction).")
    elif task == "unsupervised":
        UI.panel("Unsupervised Learning",
                 "Unsupervised learning finds patterns in data without a specific target column.")

    dataset_path = ask("Dataset path", "data/raw/dataset.csv")

    if task == "unsupervised":
        target_column = ""
    else:
        target_column = ask("Target column name", "target")

    UI.section("Problem framing", 3)
    problem_profile = run_problem_framing_wizard(task)

    UI.section("Environment", 4)
    include_pyproject = ask_yes_no("Create pyproject.toml and environment files?", True)

    python_version = "3.11"
    torch_variant = "none"
    include_ml_basics = False

    if include_pyproject:
        python_version = choose_python_profile()
        include_ml_basics = ask_yes_no("Include basic ML dependencies (pandas, numpy, scikit-learn, matplotlib, seaborn)?", False)
        torch_variant = choose_torch_variant()

    UI.section("Optional tools", 5)
    include_docs = ask_yes_no("Create documentation files?", True)
    print("\nOptional files (templates):")
    profile = choose_optional_profile()
    if profile == "custom":
        optional_options = {
            "eda": ask_yes_no("Include EDA support?", False),
            "preprocessing": ask_yes_no("Include preprocessing support?", False),
            "metrics": ask_yes_no("Include custom metrics?", False),
            "optimization": ask_yes_no("Include optimization scaffolding?", False),
            "feature_measurement": ask_yes_no("Include feature measurement?", False),
            "visualization": ask_yes_no("Include visualization support?", False),
            "notebook_factory": ask_yes_no("Include notebook factory?", False),
            "model_report": ask_yes_no("Include model report template?", False),
            "experiment_log": ask_yes_no("Include experiment log template?", False),
            "advisor": ask_yes_no("Include explainable Dataset Advisor?", False),
        }
    else:
        optional_options = get_options_by_profile(profile)

    if optional_options.get("advisor") and not include_ml_basics:
        UI.panel("Dependency Note", "Dataset Advisor requires basic ML dependencies (pandas, scikit-learn).")
        if ask_yes_no("Enable basic ML dependencies now?", True):
            include_ml_basics = True

    UI.section("Output location", 6)
    sibling_dir = (STARTER_ROOT.parent / package_name).resolve()
    current_dir = Path.cwd().resolve()
    nested_dir = (current_dir / package_name).resolve()

    print(f"1. Current directory: {current_dir}")
    print(f"2. New folder in current directory: {nested_dir}")
    print(f"3. Sibling folder (recommended): {sibling_dir}")
    print(f"4. Custom path")

    while True:
        choice = ask("Choose an option", "3")
        if choice == "1":
            output_dir = current_dir
        elif choice == "2":
            output_dir = nested_dir
        elif choice == "3":
            output_dir = sibling_dir
        elif choice == "4":
            output_dir = Path(ask("Enter custom path")).resolve()
        else:
            print("Invalid option.")
            continue

        is_inside = False
        try:
            if output_dir == STARTER_ROOT or output_dir.is_relative_to(STARTER_ROOT):
                is_inside = True
        except (ValueError, AttributeError):
            is_inside = False

        if is_inside:
            UI.warning("The selected output directory is inside the starter repository.")
            if ask_yes_no("Do you want to continue anyway?", default=False):
                break
        else:
            break

    force = ask_yes_no("Overwrite existing files if there is a conflict?", False)

    python_requires = f">={python_version}"
    if python_version == "3.12":
        python_requires = ">=3.12,<3.13"
    elif python_version == "3.14":
        python_requires = ">=3.14,<3.15"

    advisor_cmd = f"python -m {package_name}.advisor" if optional_options.get("advisor") else ""

    values = {
        "PROJECT_NAME": project_name,
        "PACKAGE_NAME": package_name,
        "TASK": task,
        "PRESET": preset,
        "DATASET_PATH": dataset_path,
        "TARGET_COLUMN": target_column,
        "PYTHON_REQUIRES": python_requires,
        "ADVISOR_COMMAND": advisor_cmd,
    }

    UI.section("Final summary", 7)
    print(f"Project name:      {values['PROJECT_NAME']}")
    print(f"Package name:      {values['PACKAGE_NAME']}")
    print(f"ML Task:           {values['TASK']}")
    print(f"Dataset path:      {values['DATASET_PATH']}")
    if target_column:
        print(f"Target column:     {values['TARGET_COLUMN']}")
    print(f"Python version:    {python_version}")
    print(f"PyTorch variant:   {torch_variant}")
    print(f"Include ML basics: {'yes' if include_ml_basics else 'no'}")
    print(f"Output directory:  {output_dir}")
    print(f"Overwrite files:   {'yes' if force else 'no'}")

    print()
    if not ask_yes_no("Create project files?", True):
        print("Aborted.")
        return

    create_dirs(output_dir, package_name, preset, include_docs)
    create_config(output_dir, values, force=force)
    create_problem_profile(output_dir, problem_profile, force=force)
    create_readme(output_dir, values, force=force)
    create_package_files(output_dir, values, force=force)
    create_optional_files(output_dir, package_name, values, optional_options, force=force)
    create_tests(output_dir, values, force=force)
    create_notebook_placeholder(output_dir, values, force=force)

    if include_docs:
        create_docs(output_dir, values, force=force)

    if include_pyproject:
        create_pyproject(output_dir, values, force=force)
        create_env_files(
            output_dir,
            values,
            include_ml_basics,
            torch_variant,
            force=force
        )

    print_summary(output_dir, values)
