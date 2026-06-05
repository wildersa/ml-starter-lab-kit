import unittest
import os
import shutil
import tempfile
from pathlib import Path
import json

import create_ml_starter
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
            optionals=["y"] * 9
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
        self.assertEqual(create_ml_starter.normalize_package_name("My Project"), "my_project")
        self.assertEqual(create_ml_starter.normalize_package_name("123-Project!"), "ml_123_project")

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

if __name__ == "__main__":
    unittest.main()
