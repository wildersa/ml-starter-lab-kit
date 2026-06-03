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

if __name__ == "__main__":
    unittest.main()
