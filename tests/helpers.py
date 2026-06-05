import io
from unittest.mock import patch
import create_ml_starter

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
    optionals=None,
    force="y",
    output_dir_sequence=None
):
    if optionals is None:
        optionals = ["n"] * 9

    inputs = [
        project_name,
        package_name,
        task,
        dataset_path,
    ]

    # task can be "1".."5" or "generic".."vision"
    is_unsupervised = (task == "3" or task == "unsupervised")
    if not is_unsupervised:
        inputs.append(target_column)

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

    inputs.extend(optionals)
    inputs.append(force)

    with patch("create_ml_starter.input", side_effect=inputs):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            create_ml_starter.main()
            return fake_out.getvalue()
