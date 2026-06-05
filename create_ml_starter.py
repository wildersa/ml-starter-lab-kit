from __future__ import annotations

import json
import re
from pathlib import Path


STARTER_ROOT = Path(__file__).resolve().parent


TASKS = {
    "1": "generic",
    "2": "supervised",
    "3": "unsupervised",
    "4": "timeseries",
    "5": "vision",
}


def ask(prompt: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{prompt}{suffix}: ").strip()
    return value or (default or "")


def ask_yes_no(prompt: str, default: bool = True) -> bool:
    default_label = "Y/n" if default else "y/N"
    value = input(f"{prompt} [{default_label}]: ").strip().lower()

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


def normalize_package_name(value: str) -> str:
    value = value.strip().lower().replace("-", "_").replace(" ", "_")
    value = re.sub(r"[^a-z0-9_]", "", value)
    value = re.sub(r"_+", "_", value).strip("_")

    if not value:
        value = "ml_project"

    if value[0].isdigit():
        value = f"ml_{value}"

    return value


def render(content: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        content = content.replace("{{" + key + "}}", value)
    return content


def load_template(name: str, values: dict[str, str], folder: str = "common") -> str:
    if name.endswith(".tpl"):
        template_path = Path(__file__).parent / "templates" / folder / name
    else:
        template_path = Path(__file__).parent / "templates" / folder / f"{name}.tpl"

    if not template_path.exists():
        return f"# Template {name} not found.\n"

    content = template_path.read_text(encoding="utf-8")
    return render(content, values)


def write_text(path: Path, content: str, *, force: bool) -> bool:
    if path.exists() and not force:
        return False

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.lstrip(), encoding="utf-8")

    return True


def touch_gitkeep(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    gitkeep = path / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.write_text("", encoding="utf-8")


def create_dirs(root: Path, package_name: str, preset: str, include_docs: bool) -> None:
    dirs = [
        "configs",
        "data/raw",
        "data/processed",
        "data/external",
        "notebooks",
        "models",
        "reports/figures",
        f"src/{package_name}",
        "tests",
    ]

    if include_docs:
        dirs.append("docs")

    for directory in dirs:
        touch_gitkeep(root / directory)


def create_config(root: Path, values: dict[str, str], *, force: bool) -> None:
    task = values["TASK"]
    preset = values.get("PRESET", "none")

    config: dict[str, object] = {
        "project": {
            "name": values["PROJECT_NAME"],
            "package": values["PACKAGE_NAME"],
            "task": task
        },
        "data": {
            "raw_path": values["DATASET_PATH"],
            "processed_path": "data/processed/modeling_table.csv"
        },
        "target": {
            "column": values["TARGET_COLUMN"]
        },
        "split": {
            "test_size": 0.2,
            "random_state": 42
        },
        "features": {
            "drop_columns": [],
            "calculated_features": [
                {
                    "type": "ratio",
                    "name": "example_ratio",
                    "numerator": "col_a",
                    "denominator": "col_b",
                    "enabled": False
                },
                {
                    "type": "datetime_parts",
                    "column": "event_date",
                    "enabled": False
                },
                {
                    "type": "lag",
                    "column": "value",
                    "lags": [1, 7],
                    "groupby": None,
                    "order_by": "event_date",
                    "enabled": False
                },
                {
                    "type": "rolling_mean",
                    "column": "value",
                    "windows": [7, 30],
                    "groupby": None,
                    "order_by": "event_date",
                    "shift": 1,
                    "enabled": False
                }
            ]
        },
        "model": {
            "type": "baseline",
            "params": {}
        },
        "eda": {
            "id_columns": [],
            "date_columns": [],
            "categorical_columns": [],
            "numeric_columns": [],
            "suspected_leakage_columns": []
        }
    }

    if task == "unsupervised":
        config["target"] = {"column": ""}
        config["model"] = {
            "type": "pca_kmeans",
            "params": {
                "n_components": 2,
                "n_clusters": 3,
                "random_state": 42
            }
        }

    if task == "timeseries":
        config["time_series"] = {
            "date_column": "date",
            "value_column": "value",
            "window_size": 30,
            "horizon": 7,
            "groupby": None
        }

    write_text(
        root / "configs/config.json",
        json.dumps(config, indent=2, ensure_ascii=False),
        force=force,
    )


def create_readme(root: Path, values: dict[str, str], *, force: bool) -> None:
    content = load_template("README.md", values, folder="project")
    write_text(root / "README.md", content, force=force)


def create_package_files(root: Path, values: dict[str, str], *, force: bool) -> None:
    package = values["PACKAGE_NAME"]
    base = root / "src" / package

    files = {
        "__init__.py": load_template("__init__.py", values, folder="project/package"),
        "config.py": load_template("config.py", values, folder="project/package"),
        "data.py": load_template("data.py", values, folder="project/package"),
        "features.py": load_template("features.py", values, folder="project/package"),
        "train.py": load_template("train.py", values, folder="project/package"),
        "evaluate.py": load_template("evaluate.py", values, folder="project/package"),
        "predict.py": load_template("predict.py", values, folder="project/package"),
    }

    for rel, content in files.items():
        write_text(base / rel, content, force=force)


def create_tests(root: Path, values: dict[str, str], *, force: bool) -> None:
    content = load_template("test_features.py", values, folder="project/tests")
    write_text(root / "tests/test_features.py", content, force=force)


def create_notebook_placeholder(root: Path, values: dict[str, str], *, force: bool) -> None:
    content = load_template("01_eda.ipynb", values, folder="notebooks")

    write_text(
        root / "notebooks/01_eda.ipynb",
        content,
        force=force,
    )


def create_docs(root: Path, values: dict[str, str], *, force: bool) -> None:
    docs = {
        "docs/data-dictionary.md": load_template("data-dictionary.md", values, folder="project/docs"),
        "reports/modeling-notes.md": load_template("modeling-notes.md", values, folder="project/reports"),
        ".gitignore": load_template("gitignore", values, folder="project"),
        ".env.example": load_template("env.example", values, folder="project"),
    }

    for rel, content in docs.items():
        write_text(root / rel, content, force=force)


def create_pyproject(root: Path, values: dict[str, str], *, force: bool) -> None:
    content = load_template("pyproject.toml", values, folder="env")
    write_text(root / "pyproject.toml", content, force=force)


def create_env_files(
    root: Path,
    values: dict[str, str],
    include_ml_basics: bool,
    torch_variant: str,
    *,
    force: bool,
) -> None:
    files_to_create = [
        "requirements.txt",
        "requirements-dev.txt",
        "requirements-notebook.txt",
    ]

    if include_ml_basics:
        files_to_create.append("requirements-ml.txt")

    if torch_variant != "none":
        files_to_create.append(f"requirements-torch-{torch_variant}.txt")

    for filename in files_to_create:
        content = load_template(filename, values, folder="env")
        write_text(root / filename, content, force=force)


def create_optional_files(
    root: Path,
    package_name: str,
    values: dict[str, str],
    options: dict[str, bool],
    *,
    force: bool,
) -> None:
    package_path = root / "src" / package_name
    reports_path = root / "reports"

    mapping = {
        "eda": package_path / "eda.py",
        "preprocessing": package_path / "preprocessing.py",
        "visualization": package_path / "visualization.py",
        "metrics": package_path / "metrics.py",
        "optimization": package_path / "optimization.py",
        "feature_measurement": package_path / "feature_measurement.py",
        "notebook_factory": package_path / "notebook_factory.py",
        "model_report": reports_path / "model-report.md",
        "experiment_log": reports_path / "experiment-log.md",
    }

    template_names = {
        "eda": "eda.py",
        "preprocessing": "preprocessing.py",
        "visualization": "visualization.py",
        "metrics": "metrics.py",
        "optimization": "optimization.py",
        "feature_measurement": "feature_measurement.py",
        "notebook_factory": "notebook_factory.py",
        "model_report": "model_report.md",
        "experiment_log": "experiment_log.md",
    }

    for key, enabled in options.items():
        if enabled and key in mapping:
            content = load_template(template_names[key], values)
            write_text(mapping[key], content, force=force)


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
    print(f"   python -m src.{values['PACKAGE_NAME']}.data")
    print(f"   python -m src.{values['PACKAGE_NAME']}.train")
    print(f"   python -m src.{values['PACKAGE_NAME']}.evaluate")


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
        include_ml_basics = ask_yes_no("Include basic ML dependencies (pandas, scikit-learn)?", False)
        torch_variant = choose_torch_variant()

    print("\nOptional files (templates):")
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
    }

    force = ask_yes_no("Overwrite existing files if there is a conflict?", False)

    python_requires = f">={python_version}"
    if python_version == "3.12":
        python_requires = ">=3.12,<3.13"
    elif python_version == "3.14":
        python_requires = ">=3.14,<3.15"

    values = {
        "PROJECT_NAME": project_name,
        "PACKAGE_NAME": package_name,
        "TASK": task,
        "PRESET": preset,
        "DATASET_PATH": dataset_path,
        "TARGET_COLUMN": target_column,
        "PYTHON_REQUIRES": python_requires,
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


if __name__ == "__main__":
    main()
