from __future__ import annotations

import re
from pathlib import Path
from .constants import STARTER_ROOT, TASKS
from .config import create_config
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

def ask(prompt: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    full_prompt = f"{prompt}{suffix}: "
    print(full_prompt, end="", flush=True)
    value = input().strip()
    return value or (default or "")


def ask_yes_no(prompt: str, default: bool = True) -> bool:
    default_label = "Y/n" if default else "y/N"
    full_prompt = f"{prompt} [{default_label}]: "
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
    print()
    print("Starter-kit created.")
    print(f"Destination: {root.resolve()}")
    print(f"Project: {values['PROJECT_NAME']}")
    print(f"Package: {values['PACKAGE_NAME']}")
    print(f"Type: {values['TASK']}")
    print()
    print("Next steps:")
    print("1. Adjust configs/config.json")
    print("2. Place your dataset in data/raw/")
    print("3. Edit src/<package>/features.py")
    print("4. Run:")
    print(f"   python -m {values['PACKAGE_NAME']}.data")
    print(f"   python -m {values['PACKAGE_NAME']}.train")
    print(f"   python -m {values['PACKAGE_NAME']}.evaluate")


def main() -> None:
    print("ML Starter Kit Builder")
    print("======================")

    default_project = Path.cwd().name
    project_name = ask("Project name", default_project)
    package_name = normalize_package_name(
        ask("Python package name", normalize_package_name(project_name))
    )
    task = choose_task()
    preset = "none"

    dataset_path = ask("Dataset path", "data/raw/dataset.csv")

    if task == "unsupervised":
        target_column = ""
    else:
        target_column = ask("Target column name", "target")

    default_output_dir = STARTER_ROOT.parent / package_name
    while True:
        output_dir = Path(ask("Directory to create the structure", str(default_output_dir))).resolve()

        is_inside = False
        try:
            if output_dir == STARTER_ROOT or output_dir.is_relative_to(STARTER_ROOT):
                is_inside = True
        except (ValueError, AttributeError):
            is_inside = False

        if is_inside:
            print("\nWARNING: The target directory is inside the starter kit repository.")
            print("Warning: The selected output directory is inside the starter repository.")
            if ask_yes_no("Do you want to continue anyway?", default=False):
                break
        else:
            break

    include_docs = ask_yes_no("Create documentation files?", True)
    include_pyproject = ask_yes_no("Create pyproject.toml and environment files?", True)

    python_version = "3.11"
    torch_variant = "none"
    include_ml_basics = False

    if include_pyproject:
        python_version = choose_python_profile()
        include_ml_basics = ask_yes_no("Include basic ML dependencies (pandas, numpy, scikit-learn, matplotlib, seaborn)?", False)
        torch_variant = choose_torch_variant()

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
        print("\nNOTE: Dataset Advisor requires basic ML dependencies (pandas, scikit-learn).")
        if ask_yes_no("Enable basic ML dependencies now?", True):
            include_ml_basics = True

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

    create_dirs(output_dir, package_name, preset, include_docs)
    create_config(output_dir, values, force=force)
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
