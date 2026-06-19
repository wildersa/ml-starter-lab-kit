import io
from unittest.mock import patch
from ml_starter_generator.cli import main

def run_generator(
    language="1",
    project_name="test_project",
    package_name="",
    task="2",
    experience_mode="1",
    dataset_path="data/raw/dataset.csv",
    target_column="target",
    include_demo="n",
    output_dir=None,
    include_docs="y",
    include_pyproject="y",
    python_profile="1",
    include_ml_basics="y",
    include_mlflow="n",
    torch_variant="1",
    optional_profile="4",
    optionals=None,
    problem_goal=None,
    problem_priority=None,
    problem_error_cost=None,
    problem_size=None,
    problem_baseline=None,
    problem_note=None,
    force="y",
    output_dir_sequence=None
):
    if optionals is None:
        optionals = ["n"] * 16

    is_guided = (experience_mode == "2" or experience_mode == "guided")

    inputs = [
        language,
        project_name,
        package_name,
        task,
        experience_mode,
        dataset_path,
    ]

    # task can be "1".."5" or "generic".."vision"
    is_unsupervised = (task == "3" or task == "unsupervised")
    if not is_unsupervised:
        inputs.append(target_column)

    inputs.append(include_demo)

    # Problem Framing Wizard inputs
    if problem_goal is None:
        if task == "2" or task == "supervised":
            problem_goal = "1" # default to classification

    inputs.append(problem_goal if problem_goal is not None else "")
    inputs.append(problem_priority if problem_priority is not None else "")
    inputs.append(problem_error_cost if problem_error_cost is not None else "")
    inputs.append(problem_size if problem_size is not None else "")
    inputs.append(problem_baseline if problem_baseline is not None else "")
    inputs.append(problem_note if problem_note is not None else "")

    # Environment
    inputs.append(include_pyproject)
    if include_pyproject.lower() in ["y", "yes", ""]:
        # python_profile can be "1", "2", "3.12", or "3.14"
        inputs.append(python_profile)
        if not is_guided:
            inputs.append(include_ml_basics)
        inputs.append(include_mlflow)
        inputs.append(torch_variant)

    # Optional tools
    is_guided = (experience_mode == "2" or experience_mode == "guided")
    if not is_guided:
        inputs.append(include_docs)
        # Skip optional profile templates header if needed?
        # No, choose_optional_profile(t) shows it and asks.
        inputs.append(optional_profile)
        if optional_profile == "4" or optional_profile == "custom":
            # The number of custom options might change.
            # We take what was provided.
            inputs.extend(optionals)

    # Dependency check for advisor/baseline_lab happens AFTER section 5 selection
    if not is_guided:
        # Check if advisor or baseline_lab was enabled in the provided optionals
        # Profile recommended (2) includes them, profile full (3) includes them.
        # Profile custom (4) depends on optionals list.
        # Index mapping in cli.py: eda(0), preproc(1), metrics(2), opt(3), feat(4), viz(5), nb(6), rep(7), exp(8), advisor(9), learn(10), baseline(11)

        has_advisor = False
        has_baseline = False

        if optional_profile == "2": # recommended
            has_advisor = True
            has_baseline = True
        elif optional_profile == "3": # full
            has_advisor = True
            has_baseline = True
        elif optional_profile == "4" or optional_profile == "custom":
            if optionals[9] == "y": has_advisor = True
            if optionals[11] == "y": has_baseline = True

        has_monitoring = False
        if optional_profile == "2": # recommended
            has_monitoring = True
        elif optional_profile == "3": # full
            has_monitoring = True
        elif optional_profile == "4" or optional_profile == "custom":
            if len(optionals) > 13 and optionals[13] == "y": has_monitoring = True

        has_synthetic = False
        if optional_profile == "2": # recommended
            has_synthetic = True
        elif optional_profile == "3": # full
            has_synthetic = True
        elif optional_profile == "4" or optional_profile == "custom":
            if len(optionals) > 14 and optionals[14] == "y": has_synthetic = True

        if (has_advisor or has_baseline or has_synthetic) and include_ml_basics == "n":
            # The wizard will prompt to enable ML basics
            inputs.append("y")

    # Output location
    if output_dir_sequence:
        inputs.extend(output_dir_sequence)
    else:
        # 1. current, 2. nested, 3. sibling, 4. custom
        # We use 4 (custom) to provide a specific path for tests
        inputs.append("4")
        inputs.append(str(output_dir))

    inputs.append(force)

    # Final summary confirmation
    inputs.append("y")

    with patch("ml_starter_generator.cli.input", side_effect=inputs):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            main()
            return fake_out.getvalue()
