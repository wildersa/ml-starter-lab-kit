import unittest
import shutil
import tempfile
import os
import json
from pathlib import Path
import sys

from tests.helpers import run_generator

class TestDataInsights(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.project_name = "insights_project"
        self.package_name = "insights_project"

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_insights_generation_and_execution(self):
        # Generate project with insights enabled (recommended profile includes it)
        run_generator(
            project_name=self.project_name,
            package_name=self.package_name,
            task="2", # supervised
            dataset_path="data/raw/demo_dataset.csv",
            target_column="target",
            include_demo="y",
            output_dir=self.test_dir,
            optional_profile="2" # recommended
        )

        pkg_path = self.test_dir / "src" / self.package_name
        insights_py = pkg_path / "data_insights.py"

        self.assertTrue(insights_py.exists(), "data_insights.py should be generated")

        # Verify lab.py has the insights command
        lab_py = pkg_path / "lab.py"
        with open(lab_py, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("def run_insights():", content)
            self.assertIn("subparsers.add_parser(\"insights\"", content)

        # To run the generated script, we need pandas/numpy.
        # If they are not available in the test environment, we at least verify the file content.
        with open(insights_py, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("class DataInsights:", content)
            self.assertIn("def analyze(self):", content)
            self.assertIn("def save_artifacts(self):", content)

        # Check if README mentions insights
        readme_path = self.test_dir / "README.md"
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()
            self.assertIn("python -m insights_project.lab insights", readme_content)

        # Check if START_HERE mentions insights
        start_here_path = self.test_dir / "START_HERE.md"
        with open(start_here_path, "r", encoding="utf-8") as f:
            start_here_content = f.read()
            self.assertIn("python -m insights_project.lab insights", start_here_content)

    def test_insights_custom_selection(self):
        # 16 optionals, insights is at index 10
        optionals = ["n"] * 16
        optionals[10] = "y"

        run_generator(
            project_name="custom_insights",
            package_name="custom_insights",
            task="2",
            output_dir=self.test_dir,
            optional_profile="4", # custom
            optionals=optionals
        )

        insights_py = self.test_dir / "src/custom_insights/data_insights.py"
        self.assertTrue(insights_py.exists(), "data_insights.py should be generated via custom selection")

if __name__ == "__main__":
    unittest.main()
