import unittest
import os
import shutil
import tempfile
from pathlib import Path
import json

from ml_starter_generator.cli import normalize_package_name
from tests.helpers import run_generator

class TestGenerator(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.project_name = "test_project"
        self.package_name = "test_project"

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_create_supervised_project(self):
        run_generator(
            project_name=self.project_name,
            package_name="",
            task="2",
            dataset_path="data/raw/train.csv",
            target_column="target",
            output_dir=self.test_dir
        )

        self.assertTrue((self.test_dir / "README.md").exists())
        self.assertTrue((self.test_dir / "src" / self.package_name / "train.py").exists())
        self.assertTrue((self.test_dir / "src" / self.package_name / "core/config.py").exists())
        self.assertTrue((self.test_dir / "src" / self.package_name / "core/data.py").exists())
        self.assertTrue((self.test_dir / "src" / self.package_name / "core/readiness.py").exists())
        self.assertTrue((self.test_dir / "configs/config.json").exists())

        with open(self.test_dir / "configs/config.json") as f:
            config = json.load(f)
            self.assertEqual(config["project"]["task"], "supervised")
            self.assertIn("eda", config)
            self.assertIn("id_columns", config["eda"])

        # Verify EDA notebook
        eda_nb_path = self.test_dir / "notebooks/01_eda.ipynb"
        self.assertTrue(eda_nb_path.exists())
        with open(eda_nb_path) as f:
            nb_content = json.load(f)
            self.assertEqual(nb_content["nbformat"], 4)
            # Check for placeholders
            self.assertIn(self.project_name, str(nb_content))
            self.assertIn(self.package_name, str(nb_content))

    def test_create_generic_project(self):
        run_generator(
            project_name="generic_proj",
            package_name="generic_pkg",
            task="1",
            dataset_path="data/raw/data.csv",
            output_dir=self.test_dir
        )

        self.assertTrue((self.test_dir / "src/generic_pkg/train.py").exists())

    def test_create_project_with_optional_files(self):
        run_generator(
            project_name="opt_proj",
            package_name="opt_pkg",
            task="2",
            dataset_path="data/raw/train.csv",
            target_column="target",
            output_dir=self.test_dir,
            optionals=["y"] * 15
        )

        pkg_path = self.test_dir / "src/opt_pkg"
        reports_path = self.test_dir / "reports"

        self.assertTrue((pkg_path / "eda.py").exists())
        self.assertTrue((pkg_path / "preprocessing.py").exists())
        self.assertTrue((pkg_path / "metrics.py").exists())
        self.assertTrue((pkg_path / "optimization.py").exists())
        self.assertTrue((pkg_path / "feature_measurement.py").exists())
        self.assertTrue((pkg_path / "visualization.py").exists())
        self.assertTrue((pkg_path / "notebook_factory.py").exists())
        self.assertTrue((reports_path / "model-report.md").exists())
        self.assertTrue((reports_path / "experiment-log.md").exists())

        # Verify feature measurement content
        with open(pkg_path / "feature_measurement.py") as f:
            content = f.read()
            self.assertIn("class FeatureImpact:", content)

        # Verify model report content
        with open(reports_path / "model-report.md") as f:
            content = f.read()
            self.assertIn("# Model Report — opt_proj", content)

    def test_no_third_party_dependencies(self):
        run_generator(
            project_name="no_deps_proj",
            package_name="no_deps_pkg",
            task="1",
            dataset_path="data/raw/data.csv",
            output_dir=self.test_dir,
            include_ml_basics="n"
        )

        pyproject_path = self.test_dir / "pyproject.toml"
        self.assertTrue(pyproject_path.exists())

        with open(pyproject_path) as f:
            content = f.read()
            self.assertNotIn("dependencies =", content)
            self.assertNotIn("scikit-learn =", content)
            self.assertNotIn("numpy =", content)

    def test_normalize_package_name(self):
        self.assertEqual(normalize_package_name("My Project"), "my_project")
        self.assertEqual(normalize_package_name("123-Project!"), "ml_123_project")

    def test_python_profiles(self):
        # Test Safe Profile (3.12)
        run_generator(
            project_name="safe_proj",
            package_name="safe_pkg",
            task="1",
            output_dir=self.test_dir,
            python_profile="1",
            include_ml_basics="n"
        )

        with open(self.test_dir / "pyproject.toml") as f:
            content = f.read()
            self.assertIn('requires-python = ">=3.12,<3.13"', content)

        shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)

        # Test Modern Profile (3.14)
        run_generator(
            project_name="modern_proj",
            package_name="modern_pkg",
            task="1",
            output_dir=self.test_dir,
            python_profile="2",
            include_ml_basics="n"
        )

        with open(self.test_dir / "pyproject.toml") as f:
            content = f.read()
            self.assertIn('requires-python = ">=3.14,<3.15"', content)

    def test_torch_generation(self):
        # Test Torch CPU
        run_generator(
            project_name="torch_cpu",
            package_name="torch_cpu",
            task="1",
            output_dir=self.test_dir,
            include_ml_basics="n",
            torch_variant="2"
        )

        self.assertTrue((self.test_dir / "requirements-torch-cpu.txt").exists())
        self.assertFalse((self.test_dir / "requirements-torch-cuda126.txt").exists())

        shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)

        # Test Torch CUDA 12.8
        run_generator(
            project_name="torch_cuda",
            package_name="torch_cuda",
            task="1",
            output_dir=self.test_dir,
            include_ml_basics="n",
            torch_variant="4"
        )

        self.assertTrue((self.test_dir / "requirements-torch-cu128.txt").exists())
        with open(self.test_dir / "requirements-torch-cu128.txt") as f:
            self.assertIn("CUDA 12.8", f.read())

    def test_create_vision_project(self):
        run_generator(
            project_name="vision_proj",
            package_name="vision_pkg",
            task="5",
            dataset_path="data/raw/images.csv",
            target_column="label",
            output_dir=self.test_dir,
            include_pyproject="n"
        )

        with open(self.test_dir / "configs/config.json") as f:
            config = json.load(f)
            self.assertEqual(config["project"]["task"], "vision")
            self.assertEqual(config["target"]["column"], "label")

        train_path = self.test_dir / "src/vision_pkg/train.py"
        with open(train_path) as f:
            content = f.read()
            self.assertIn('"vision"', content)
            self.assertNotIn('"datathon"', content)

    def test_pyproject_src_layout(self):
        run_generator(
            project_name="src_layout_proj",
            package_name="src_layout_pkg",
            task="1",
            output_dir=self.test_dir,
            include_ml_basics="n"
        )

        pyproject_path = self.test_dir / "pyproject.toml"
        with open(pyproject_path) as f:
            content = f.read()
            self.assertIn("[build-system]", content)
            self.assertIn('requires = ["setuptools>=61.0"]', content)
            self.assertIn('[tool.setuptools.packages.find]', content)
            self.assertIn('where = ["src"]', content)
            self.assertIn('pythonpath = ["src"]', content)

    def test_readme_suggested_commands(self):
        run_generator(
            project_name="cmd_proj",
            package_name="cmd_pkg",
            task="1",
            output_dir=self.test_dir,
            include_ml_basics="n"
        )

        readme_path = self.test_dir / "README.md"
        with open(readme_path) as f:
            content = f.read()
            self.assertIn("python -m cmd_pkg.lab check", content)
            self.assertIn("python -m cmd_pkg.lab train", content)
            self.assertIn("python -m cmd_pkg.lab evaluate", content)
            self.assertNotIn("python -m src.cmd_pkg.lab", content)

    def test_minimal_profile(self):
        run_generator(
            project_name="minimal_proj",
            package_name="minimal_pkg",
            task="1",
            output_dir=self.test_dir,
            optional_profile="1"
        )

        pkg_path = self.test_dir / "src/minimal_pkg"
        self.assertFalse((pkg_path / "eda.py").exists())
        self.assertFalse((pkg_path / "preprocessing.py").exists())
        self.assertFalse((pkg_path / "visualization.py").exists())

    def test_full_profile(self):
        run_generator(
            project_name="full_proj",
            package_name="full_pkg",
            task="1",
            output_dir=self.test_dir,
            optional_profile="3"
        )

        pkg_path = self.test_dir / "src/full_pkg"
        reports_path = self.test_dir / "reports"
        self.assertTrue((pkg_path / "eda.py").exists())
        self.assertTrue((pkg_path / "preprocessing.py").exists())
        self.assertTrue((pkg_path / "metrics.py").exists())
        self.assertTrue((pkg_path / "optimization.py").exists())
        self.assertTrue((pkg_path / "feature_measurement.py").exists())
        self.assertTrue((pkg_path / "visualization.py").exists())
        self.assertTrue((pkg_path / "notebook_factory.py").exists())
        self.assertTrue((pkg_path / "baseline_lab.py").exists())
        self.assertTrue((reports_path / "model-report.md").exists())
        self.assertTrue((reports_path / "experiment-log.md").exists())

    def test_custom_profile(self):
        # Custom profile, selecting only eda and metrics
        optionals = ["y", "n", "y", "n", "n", "n", "n", "n", "n", "n", "n", "n", "n", "n", "n", "n", "n"]
        run_generator(
            project_name="custom_proj",
            package_name="custom_pkg",
            task="1",
            output_dir=self.test_dir,
            optional_profile="4",
            optionals=optionals
        )

        pkg_path = self.test_dir / "src/custom_pkg"
        self.assertTrue((pkg_path / "eda.py").exists())
        self.assertTrue((pkg_path / "metrics.py").exists())
        self.assertFalse((pkg_path / "preprocessing.py").exists())
        self.assertFalse((pkg_path / "visualization.py").exists())

    def test_recommended_profile(self):
        run_generator(
            project_name="rec_proj",
            package_name="rec_pkg",
            task="1",
            output_dir=self.test_dir,
            optional_profile="2"
        )

        pkg_path = self.test_dir / "src/rec_pkg"
        reports_path = self.test_dir / "reports"

        # Should generate
        self.assertTrue((pkg_path / "eda.py").exists())
        self.assertTrue((pkg_path / "preprocessing.py").exists())
        self.assertTrue((pkg_path / "metrics.py").exists())
        self.assertTrue((pkg_path / "visualization.py").exists())
        self.assertTrue((pkg_path / "baseline_lab.py").exists())

        # Should NOT generate
        self.assertFalse((pkg_path / "optimization.py").exists())
        self.assertFalse((pkg_path / "feature_measurement.py").exists())
        self.assertFalse((pkg_path / "notebook_factory.py").exists())
        self.assertFalse((reports_path / "model-report.md").exists())
        self.assertFalse((reports_path / "experiment-log.md").exists())

    def test_ml_dependency_prompt_text(self):
        output = run_generator(
            project_name="ml_prompt_proj",
            package_name="ml_prompt_pkg",
            task="1",
            output_dir=self.test_dir,
            include_ml_basics="y"
        )

        expected_text = "Include basic ML dependencies (pandas, numpy, scikit-learn, matplotlib, seaborn)?"
        self.assertIn(expected_text, output)

    def test_lab_cli_generation(self):
        # Test generation in minimal mode
        run_generator(
            project_name="lab_minimal",
            package_name="lab_minimal",
            task="1",
            output_dir=self.test_dir,
            experience_mode="1", # minimal
            optional_profile="1" # minimal
        )

        lab_path = self.test_dir / "src/lab_minimal/lab.py"
        self.assertTrue(lab_path.exists())

        with open(lab_path) as f:
            content = f.read()
            self.assertIn("argparse", content)
            self.assertIn("subparsers.add_parser(\"check\"", content)
            self.assertIn("subparsers.add_parser(\"train\"", content)
            self.assertIn("subparsers.add_parser(\"workspace\"", content)
            self.assertIn("def run_workspace():", content)

        # Ensure existing commands are still there
        self.assertTrue((self.test_dir / "src/lab_minimal/guide.py").exists())
        self.assertTrue((self.test_dir / "src/lab_minimal/train.py").exists())

        shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)

        # Test generation in guided mode
        run_generator(
            project_name="lab_guided",
            package_name="lab_guided",
            task="1",
            output_dir=self.test_dir,
            experience_mode="2" # guided
        )

        lab_path = self.test_dir / "src/lab_guided/lab.py"
        self.assertTrue(lab_path.exists())

        with open(lab_path) as f:
            content = f.read()
            self.assertIn("def run_all():", content)

    def test_lab_cli_workspace_guidance(self):
        # In a minimal project, workspace should just print guidance
        run_generator(
            project_name="ws_test",
            package_name="ws_test",
            task="1",
            output_dir=self.test_dir,
            experience_mode="1"
        )

        lab_path = self.test_dir / "src/ws_test/lab.py"
        with open(lab_path) as f:
            content = f.read()
            self.assertIn("learning_workspace.py", content)
            self.assertIn("pkg_dir = Path(__file__).parent", content)
            self.assertIn("Streamlit workspace is not available in this project.", content)

    def test_guided_mode_generates_workspace(self):
        run_generator(
            project_name="guided_ws",
            package_name="guided_ws",
            task="1",
            output_dir=self.test_dir,
            experience_mode="2" # guided
        )

        ws_path = self.test_dir / "src/guided_ws/learning_workspace.py"
        self.assertTrue(ws_path.exists())

        # Check for streamlit in requirements-ml.txt
        req_path = self.test_dir / "requirements-ml.txt"
        self.assertTrue(req_path.exists())
        with open(req_path) as f:
            content = f.read()
            self.assertIn("streamlit", content)

    def test_minimal_mode_no_workspace(self):
        run_generator(
            project_name="minimal_ws",
            package_name="minimal_ws",
            task="1",
            output_dir=self.test_dir,
            experience_mode="1" # minimal
        )

        ws_path = self.test_dir / "src/minimal_ws/learning_workspace.py"
        self.assertFalse(ws_path.exists())

        # Even if ML basics are enabled, streamlit should not be there in minimal
        shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)

        run_generator(
            project_name="minimal_ws_ml",
            package_name="minimal_ws_ml",
            task="1",
            output_dir=self.test_dir,
            experience_mode="1", # minimal
            include_ml_basics="y"
        )

        req_path = self.test_dir / "requirements-ml.txt"
        self.assertTrue(req_path.exists())
        with open(req_path) as f:
            content = f.read()
            self.assertNotIn("streamlit", content)

    def test_train_evaluate_preserved(self):
        """P0.5: train.py and evaluate.py are preserved and not replaced by baseline lab."""
        package_name = "preserve_pkg"
        output_dir = self.test_dir / "preserve_project"

        run_generator(
            project_name="Preserve Project",
            package_name=package_name,
            output_dir=output_dir,
            experience_mode="2" # guided, includes baseline_lab
        )

        pkg_path = output_dir / f"src/{package_name}"
        self.assertTrue((pkg_path / "baseline_lab.py").exists())
        self.assertTrue((pkg_path / "train.py").exists())
        self.assertTrue((pkg_path / "evaluate.py").exists())

        train_content = (pkg_path / "train.py").read_text()
        self.assertIn("def train_baseline_classifier", train_content)
        self.assertNotIn("class BaselineLab", train_content)

        evaluate_content = (pkg_path / "evaluate.py").read_text()
        self.assertIn("def evaluate_classification", evaluate_content)

if __name__ == "__main__":
    unittest.main()
