from __future__ import annotations

from pathlib import Path
from .io import write_text, touch_gitkeep
from .templates import load_template

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
