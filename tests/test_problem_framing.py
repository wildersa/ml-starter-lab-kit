import unittest
import shutil
import tempfile
import os
import sys
import subprocess
import json
import csv
from pathlib import Path
from tests.helpers import run_generator

class TestProblemFraming(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_wizard_writes_config(self):
        """Verify that the wizard writes configs/problem_profile.json."""
        project_name = "wizard_project"
        package_name = "wizard_pkg"
        output_dir = self.test_dir / project_name

        run_generator(
            project_name=project_name,
            package_name=package_name,
            output_dir=output_dir,
            problem_goal="predict a number",
            problem_priority="interpretability",
            problem_error_cost="false positive",
            problem_size="small",
            problem_baseline="y",
            problem_note="Testing wizard"
        )

        profile_path = output_dir / "configs/problem_profile.json"
        self.assertTrue(profile_path.exists())

        with open(profile_path, "r") as f:
            data = json.load(f)

        self.assertEqual(data["goal"], "predict a number")
        self.assertEqual(data["priority"], "interpretability")
        self.assertEqual(data["error_cost"], "false positive")
        self.assertEqual(data["dataset_size"], "small")
        self.assertEqual(data["prefer_baseline"], "yes")
        self.assertEqual(data["domain_note"], "Testing wizard")

    def test_wizard_defaults(self):
        """Verify that pressing Enter uses defaults."""
        project_name = "defaults_project"
        package_name = "defaults_pkg"
        output_dir = self.test_dir / project_name

        # Empty strings in run_generator inputs simulate pressing Enter
        run_generator(
            project_name=project_name,
            package_name=package_name,
            output_dir=output_dir,
            problem_goal="",
            problem_priority="",
            problem_error_cost="",
            problem_size="",
            problem_baseline="",
            problem_note=""
        )

        profile_path = output_dir / "configs/problem_profile.json"
        self.assertTrue(profile_path.exists())

        with open(profile_path, "r") as f:
            data = json.load(f)

        # Default for supervised goal is "predict a category"
        self.assertEqual(data["goal"], "predict a category")
        self.assertEqual(data["priority"], "learning/experimentation")
        self.assertEqual(data["error_cost"], "not sure")
        self.assertEqual(data["dataset_size"], "not sure")
        self.assertEqual(data["prefer_baseline"], "yes") # default for ask_yes_no is True
        self.assertEqual(data["domain_note"], "")

    def test_advisor_integration(self):
        """Verify advisor reads profile and includes suggested models."""
        is_ci = os.environ.get("GITHUB_ACTIONS") == "true"
        try:
            import pandas
            import numpy
            import sklearn
        except ImportError:
            if is_ci:
                self.fail("ML dependencies missing in CI.")
            self.skipTest("ML dependencies missing.")

        project_name = "advisor_integration"
        package_name = "advisor_pkg"
        output_dir = self.test_dir / project_name

        # Include eda and advisor template
        optionals = ["y"] + ["n"] * 8 + ["y", "n", "n", "n", "n", "n", "n", "n"]

        run_generator(
            project_name=project_name,
            package_name=package_name,
            output_dir=output_dir,
            optional_profile="4",
            optionals=optionals,
            include_ml_basics="y",
            problem_goal="predict a category",
            problem_priority="imbalanced classes",
            problem_error_cost="false negative",
            problem_size="small",
            problem_baseline="y"
        )

        # Create dummy data
        dataset_path = output_dir / "data/raw/dataset.csv"
        dataset_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dataset_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["feature", "target"])
            for i in range(20): # small dataset
                writer.writerow([i, i % 2])

        # Run advisor
        env = os.environ.copy()
        env["PYTHONPATH"] = str(output_dir / "src")

        # P0.1: Must run EDA first
        subprocess.run(
            [sys.executable, "-m", f"{package_name}.eda"],
            cwd=output_dir,
            env=env,
            check=True
        )

        result = subprocess.run(
            [sys.executable, "-m", f"{package_name}.advisor"],
            cwd=output_dir,
            env=env,
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)

        # Check report
        report_path = output_dir / "reports/dataset-advice.md"
        self.assertTrue(report_path.exists())
        content = report_path.read_text()

        self.assertIn("## Suggested Starting Models", content)
        self.assertIn("Random Forest / HistGradientBoosting (with class_weight='balanced')", content)
        self.assertIn("Recall-optimized Evaluation", content)
        self.assertIn("Cross-validation + Simple Models", content)
        self.assertIn("Dummy Models (Baseline)", content)

        # Check JSON output
        json_path = output_dir / "configs/suggested_pipeline.json"
        with open(json_path, "r") as f:
            results = json.load(f)

        self.assertIn("model_recommendations", results)
        self.assertTrue(len(results["model_recommendations"]) > 0)

if __name__ == "__main__":
    unittest.main()
