from pathlib import Path
from .helpers import run_generator

def test_pipeline_manifest_generation(tmp_path):
    output_dir = tmp_path / "manifest_project"

    # optionals list length in helpers.py is now 18
    # eda(0), preproc(1), metrics(2), opt(3), feat(4), viz(5), nb(6), rep(7), exp(8),
    # advisor(9), insights(10), screening(11), learn(12), baseline(13), bandit(14),
    # monitoring(15), synthetic(16), manifest(17)
    optionals = ["n"] * 17 + ["y"]

    run_generator(
        project_name="manifest_project",
        output_dir=output_dir,
        experience_mode="minimal",
        optional_profile="custom",
        optionals=optionals,
        include_ml_basics="y"
    )

    package_path = output_dir / "src/manifest_project"
    manifest_py = package_path / "pipeline_manifest.py"

    assert manifest_py.exists()
    assert "class PipelineManifestGenerator" in manifest_py.read_text()

def test_pipeline_manifest_in_recommended_profile(tmp_path):
    output_dir = tmp_path / "recommended_project"

    run_generator(
        project_name="recommended_project",
        output_dir=output_dir,
        experience_mode="minimal",
        optional_profile="recommended",
        include_ml_basics="y"
    )

    package_path = output_dir / "src/recommended_project"
    assert (package_path / "pipeline_manifest.py").exists()

def test_lab_cli_has_manifest_command(tmp_path):
    output_dir = tmp_path / "cli_project"

    run_generator(
        project_name="cli_project",
        output_dir=output_dir,
        experience_mode="minimal",
        optional_profile="recommended",
        include_ml_basics="y"
    )

    lab_py = output_dir / "src/cli_project/lab.py"
    content = lab_py.read_text()

    assert 'subparsers.add_parser("manifest"' in content
    assert 'elif args.command == "manifest":' in content
    assert 'run_manifest()' in content
