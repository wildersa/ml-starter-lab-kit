import io
from unittest.mock import patch
from ml_starter_generator.cli import main

def run_generator(
    project_name="test_project",
    package_name="",
    task="2",
    dataset_path="data/raw/dataset.csv",
    target_column="target",
    output_dir=None,
    include_docs="y",
    include_pyproject="y",
    python_profile="1",
    include_ml_basics="y",
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
    output_dir_sequence=None,
    language="1"
):
    if optionals is None:
        optionals = ["n"] * 10

    inputs = [
        language,
        project_name,
        package_name,
        task,
        dataset_path,
    ]

    # task can be "1".."5" or "generic".."vision"
    is_unsupervised = (task == "3" or task == "unsupervised")
    if not is_unsupervised:
        inputs.append(target_column)

    # Problem Framing Wizard inputs
    inputs.append(problem_goal if problem_goal is not None else "")
    inputs.append(problem_priority if problem_priority is not None else "")
    inputs.append(problem_error_cost if problem_error_cost is not None else "")
    inputs.append(problem_size if problem_size is not None else "")
    inputs.append(problem_baseline if problem_baseline is not None else "")
    inputs.append(problem_note if problem_note is not None else "")

    if output_dir_sequence:
        inputs.extend(output_dir_sequence)
    else:
        inputs.append(str(output_dir))

    inputs.append(include_docs)
    inputs.append(include_pyproject)

    if include_pyproject.lower() in ["y", "yes", ""]:
        inputs.append(python_profile)
        inputs.append(include_ml_basics)
        inputs.append(torch_variant)

    inputs.append(optional_profile)
    if optional_profile == "4" or optional_profile == "custom":
        inputs.extend(optionals)

    inputs.append(force)

    with patch("ml_starter_generator.cli.input", side_effect=inputs):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            main()
            return fake_out.getvalue()
