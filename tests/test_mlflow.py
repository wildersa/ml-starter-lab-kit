import unittest
import os
import shutil
import tempfile
from pathlib import Path
import json
import re

from tests.helpers import run_generator

class TestMLflowIntegration(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.project_name = "mlflow_project"
        self.package_name = "mlflow_project"

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_mlflow_option_defaults_to_off(self):
        # Run with default 'recommended' profile (which should have MLflow off)
        run_generator(
            project_name=self.project_name,
            output_dir=self.test_dir,
            optional_profile="2", # Recommended
            include_mlflow="n"    # Explicitly say no if prompted
        )

        # P0.3: config records tracking setting
        config_path = self.test_dir / "configs/config.json"
        with open(config_path) as f:
            config = json.load(f)
            self.assertFalse(config.get("tracking", {}).get("enabled_mlflow", False))

        # P0.2: MLflow requirement only when enabled
        req_mlflow = self.test_dir / "requirements-mlflow.txt"
        self.assertFalse(req_mlflow.exists())

        # P0.6: default path has no MLflow runtime requirement (no top-level import)
        train_py = self.test_dir / "src" / self.package_name / "train.py"
        with open(train_py) as f:
            content = f.read()
            # Check that 'import mlflow' is not at the start of any line
            self.assertFalse(re.search(r'^import mlflow', content, re.MULTILINE))

        # P0.8: UI command documented conditionally
        readme_path = self.test_dir / "README.md"
        with open(readme_path) as f:
            content = f.read()
            self.assertNotIn("mlflow server", content)

    def test_mlflow_enabled_integration(self):
        # P0.1, P0.2, P0.3, P0.4, P0.5, P0.8
        run_generator(
            project_name=self.project_name,
            output_dir=self.test_dir,
            optional_profile="4", # Custom
            include_mlflow="y",
            optionals=["n"] * 10
        )

        # P0.3: config records tracking setting
        config_path = self.test_dir / "configs/config.json"
        with open(config_path) as f:
            config = json.load(f)
            self.assertTrue(config.get("tracking", {}).get("enabled_mlflow", True))

        # P0.2: MLflow requirement only when enabled
        req_mlflow = self.test_dir / "requirements-mlflow.txt"
        self.assertTrue(req_mlflow.exists())

        # P0.4 & P0.5: generated train/evaluate contain MLflow logic
        train_py = self.test_dir / "src" / self.package_name / "train.py"
        with open(train_py) as f:
            content = f.read()
            self.assertIn("mlflow", content.lower())
            self.assertIn("tracking", content.lower())

        evaluate_py = self.test_dir / "src" / self.package_name / "evaluate.py"
        with open(evaluate_py) as f:
            content = f.read()
            self.assertIn("mlflow", content.lower())
            self.assertIn("tracking", content.lower())

        # P0.8: UI command documented conditionally
        readme_path = self.test_dir / "README.md"
        with open(readme_path) as f:
            content = f.read()
            self.assertIn("mlflow server", content)

    def test_missing_dependency_hint(self):
        # P0.7: If MLflow is enabled but not installed, output gives a didactic install hint
        run_generator(
            project_name=self.project_name,
            output_dir=self.test_dir,
            include_mlflow="y",
            optional_profile="3" # Full
        )

        train_py = self.test_dir / "src" / self.package_name / "train.py"
        with open(train_py) as f:
            content = f.read()
            self.assertIn("pip install -r requirements-mlflow.txt", content)

if __name__ == "__main__":
    unittest.main()
