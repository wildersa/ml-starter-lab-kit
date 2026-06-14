from __future__ import annotations

from pathlib import Path
from .io import write_text, touch_gitkeep
from .templates import load_template
from .demo_data import get_demo_data

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
        f"src/{package_name}/core",
        "tests",
    ]

    if include_docs:
        dirs.append("docs")

    for directory in dirs:
        touch_gitkeep(root / directory)


def create_readme(root: Path, values: dict[str, str], *, force: bool) -> None:
    lang = values.get("LANGUAGE", "en")
    template_name = "README.md"
    if lang == "pt-BR":
        template_name = "README.pt-BR.md"

    content = load_template(template_name, values, folder="project")
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
        "guide.py": load_template("guide.py", values, folder="project/package"),
        "lab.py": load_template("lab.py", values, folder="project/package"),
        "core/__init__.py": load_template("__init__.py", values, folder="project/package/core"),
        "core/config.py": load_template("config.py", values, folder="project/package/core"),
        "core/data.py": load_template("data.py", values, folder="project/package/core"),
        "core/readiness.py": load_template("readiness.py", values, folder="project/package/core"),
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
    lang = values.get("LANGUAGE", "en")
    suffix = ".pt-BR" if lang == "pt-BR" else ""

    docs = {
        "docs/data-dictionary.md": load_template("data-dictionary.md", values, folder="project/docs"),
        f"docs/evaluation{suffix}.md": load_template(f"evaluation{suffix}.md", values, folder="project/docs"),
        f"docs/monitoring{suffix}.md": load_template(f"monitoring{suffix}.md", values, folder="project/docs"),
        f"docs/synthetic-data-lab{suffix}.md": load_template(f"synthetic-data-lab{suffix}.md", values, folder="project/docs"),
        "reports/modeling-notes.md": load_template("modeling-notes.md", values, folder="project/reports"),
        ".gitignore": load_template("gitignore", values, folder="project"),
        ".env.example": load_template("env.example", values, folder="project"),
    }

    if values.get("GENERATE_BANDIT") == "true":
        docs[f"docs/mab-lab{suffix}.md"] = load_template(f"mab-lab{suffix}.md", values, folder="project/docs")
        docs[f"docs/bandit-walkthrough{suffix}.md"] = load_template(f"bandit-walkthrough{suffix}.md", values, folder="project/docs")

    if values.get("INCLUDE_DEMO") == "true":
        template_name = "demo-scenario.md"
        if lang == "pt-BR":
            template_name = "demo-scenario.pt-BR.md"
        docs["docs/demo-scenario.md"] = load_template(template_name, values, folder="project/docs")

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
    include_mlflow: bool = False,
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

    if include_mlflow:
        files_to_create.append("requirements-mlflow.txt")

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
        "advisor": package_path / "advisor.py",
        "learning": package_path / "learning.py",
        "baseline_lab": package_path / "baseline_lab.py",
        "monitoring": package_path / "monitor.py",
        "learning_workspace": package_path / "learning_workspace.py",
        "bandit_lab": package_path / "bandit_lab.py",
        "bandit_dashboard": package_path / "bandit_dashboard.py",
        "bandit_config": root / "configs/bandit_config.json",
        "synthetic_data": package_path / "synthetic_data.py",
        "synthetic_config": root / "configs/synthetic_data.json",
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
        "advisor": "advisor.py",
        "learning": "learning.py.tpl",
        "baseline_lab": "baseline_lab.py.tpl",
        "monitoring": "monitor.py.tpl",
        "learning_workspace": "learning_workspace.py",
        "bandit_lab": "bandit_lab.py.tpl",
        "bandit_dashboard": "bandit_dashboard.py.tpl",
        "bandit_config": "bandit_config.json.tpl",
        "synthetic_data": "synthetic_data.py.tpl",
        "synthetic_config": "synthetic_data.json.tpl",
    }

    # Special wiring for Bandit Lab: it REQUIRES metrics.py
    if options.get("bandit_lab"):
        options["metrics"] = True

    # Special wiring for Synthetic Data: it might be enabled but not in the mapping?
    # Ensure synthetic_config is treated like synthetic_data
    if options.get("synthetic_data"):
        options["synthetic_config"] = True

    for key, enabled in options.items():
        if enabled and key in mapping:
            folder = "common"
            if "config" in key:
                folder = "project/configs"
            content = load_template(template_names[key], values, folder=folder)
            write_text(mapping[key], content, force=force)

    # Config and Dashboard are specific to Bandit Lab and not in the main loop above
    if options.get("bandit_lab"):
        # Config
        content = load_template(template_names["bandit_config"], values)
        write_text(mapping["bandit_config"], content, force=force)
        # Dashboard
        content = load_template(template_names["bandit_dashboard"], values)
        write_text(mapping["bandit_dashboard"], content, force=force)


def create_demo_data(
    root: Path,
    values: dict[str, str],
    problem_profile: dict[str, str],
    *,
    force: bool
) -> None:
    if values.get("INCLUDE_DEMO") != "true":
        return

    task = values["TASK"]
    goal = problem_profile.get("goal", "")
    content = get_demo_data(task, goal)

    write_text(
        root / "data/raw/demo_dataset.csv",
        content,
        force=force
    )
