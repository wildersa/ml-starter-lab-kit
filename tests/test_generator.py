import unittest
import os
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch
import io
import json

import create_ml_starter

class TestGenerator(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.project_name = "test_project"
        self.package_name = "test_project"

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch('create_ml_starter.input')
    def test_create_supervised_project(self, mock_input):
        # 1. generic, 2. supervised, 3. unsupervised, 4. timeseries, 5. datathon
        mock_input.side_effect = [
            self.project_name, # Project Name
            "", # Package Name (default)
            "2", # Task: supervised
            "data/raw/train.csv", # Dataset path
            "target", # Target column
            str(self.test_dir), # Output dir
            "y", # include docs
            "y", # include pyproject
            "1", # Python profile: safe (3.12)
            "y", # include ml basics
            "1", # Torch variant: none
            "n", "n", "n", "n", "n", "n", "n", "n", "n", # Opcionais (9 nãos)
            "y", # force
        ]

        with patch('sys.stdout', new=io.StringIO()):
            create_ml_starter.main()

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

    @patch('create_ml_starter.input')
    def test_create_generic_project(self, mock_input):
        mock_input.side_effect = [
            "generic_proj", # Project Name
            "generic_pkg", # Package Name
            "1", # Task: generic
            "data/raw/data.csv", # Dataset path
            "target", # Target column
            str(self.test_dir), # Output dir
            "y", # include docs
            "y", # include pyproject
            "1", # Python profile: safe (3.12)
            "y", # include ml basics
            "1", # Torch variant: none
            "n", "n", "n", "n", "n", "n", "n", "n", "n", # Opcionais (9 nãos)
            "y", # force
        ]

        with patch('sys.stdout', new=io.StringIO()):
            create_ml_starter.main()

        self.assertTrue((self.test_dir / "src/generic_pkg/train.py").exists())

    @patch('create_ml_starter.input')
    def test_create_project_with_optional_files(self, mock_input):
        mock_input.side_effect = [
            "opt_proj", # Project Name
            "opt_pkg", # Package Name
            "2", # Task: supervised
            "data/raw/train.csv", # Dataset path
            "target", # Target column
            str(self.test_dir), # Output dir
            "y", # include docs
            "y", # include pyproject
            "1", # Python profile: safe (3.12)
            "y", # include ml basics
            "1", # Torch variant: none
            "y", # eda
            "y", # preprocessing
            "y", # metrics
            "y", # optimization
            "y", # feature_measurement
            "y", # visualization
            "y", # notebook_factory
            "y", # model_report
            "y", # experiment_log
            "y", # force
        ]

        with patch('sys.stdout', new=io.StringIO()):
            create_ml_starter.main()

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

    @patch('create_ml_starter.input')
    def test_no_third_party_dependencies(self, mock_input):
        mock_input.side_effect = [
            "no_deps_proj", # Project Name
            "no_deps_pkg", # Package Name
            "1", # Task: generic
            "data/raw/data.csv", # Dataset path
            "target", # Target column
            str(self.test_dir), # Output dir
            "y", # include docs
            "y", # include pyproject
            "1", # Python profile: safe (3.12)
            "n", # include ml basics: NO
            "1", # Torch variant: none
            "n", "n", "n", "n", "n", "n", "n", "n", "n", # Opcionais
            "y", # force
        ]

        with patch('sys.stdout', new=io.StringIO()):
            create_ml_starter.main()

        pyproject_path = self.test_dir / "pyproject.toml"
        self.assertTrue(pyproject_path.exists())

        with open(pyproject_path) as f:
            content = f.read()
            # Should not have dependencies in [project] section
            # The current template has a comment mentioning pandas, but no dependencies key.
            self.assertNotIn("dependencies =", content)
            self.assertNotIn("scikit-learn =", content)
            self.assertNotIn("numpy =", content)

    def test_normalize_package_name(self):
        self.assertEqual(create_ml_starter.normalize_package_name("My Project"), "my_project")
        self.assertEqual(create_ml_starter.normalize_package_name("123-Project!"), "ml_123_project")

    @patch('create_ml_starter.input')
    def test_python_profiles(self, mock_input):
        # Test Safe Profile (3.12)
        mock_input.side_effect = [
            "safe_proj", "safe_pkg", "1", "data/raw/data.csv", "target",
            str(self.test_dir), "y", "y", "1", "n", "1",
            "n", "n", "n", "n", "n", "n", "n", "n", "n", "y"
        ]
        with patch('sys.stdout', new=io.StringIO()):
            create_ml_starter.main()

        with open(self.test_dir / "pyproject.toml") as f:
            content = f.read()
            self.assertIn('requires-python = ">=3.12,<3.13"', content)

        shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)

        # Test Modern Profile (3.14)
        mock_input.side_effect = [
            "modern_proj", "modern_pkg", "1", "data/raw/data.csv", "target",
            str(self.test_dir), "y", "y", "2", "n", "1",
            "n", "n", "n", "n", "n", "n", "n", "n", "n", "y"
        ]
        with patch('sys.stdout', new=io.StringIO()):
            create_ml_starter.main()

        with open(self.test_dir / "pyproject.toml") as f:
            content = f.read()
            self.assertIn('requires-python = ">=3.14,<3.15"', content)

    @patch('create_ml_starter.input')
    def test_torch_generation(self, mock_input):
        # Test Torch CPU
        mock_input.side_effect = [
            "torch_cpu", "torch_cpu", "1", "data/raw/data.csv", "target",
            str(self.test_dir), "y", "y", "1", "n", "2",
            "n", "n", "n", "n", "n", "n", "n", "n", "n", "y"
        ]
        with patch('sys.stdout', new=io.StringIO()):
            create_ml_starter.main()

        self.assertTrue((self.test_dir / "requirements-torch-cpu.txt").exists())
        self.assertFalse((self.test_dir / "requirements-torch-cuda126.txt").exists())

        shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)

        # Test Torch CUDA 12.8
        mock_input.side_effect = [
            "torch_cuda", "torch_cuda", "1", "data/raw/data.csv", "target",
            str(self.test_dir), "y", "y", "1", "n", "4",
            "n", "n", "n", "n", "n", "n", "n", "n", "n", "y"
        ]
        with patch('sys.stdout', new=io.StringIO()):
            create_ml_starter.main()

        self.assertTrue((self.test_dir / "requirements-torch-cu128.txt").exists())
        with open(self.test_dir / "requirements-torch-cu128.txt") as f:
            self.assertIn("CUDA 12.8", f.read())

if __name__ == "__main__":
    unittest.main()
