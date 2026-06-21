import unittest
import os
import shutil
import tempfile
import subprocess
import sys
import csv
from pathlib import Path
from tests.helpers import run_generator

class TestAdvisor(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_advisor_generation(self):
        """Verify the advisor script is generated correctly with expected content."""
        project_name = "advisor_gen_project"
        package_name = "advisor_gen_pkg"
        output_dir = self.test_dir / project_name

        # 12 optionals: eda, preprocessing, metrics, optimization, feature_measurement,
        # visualization, notebook_factory, model_report, experiment_log, advisor, insights, learning, baseline_lab
        optionals = ["n", "n", "n", "n", "n", "n", "n", "n", "n", "y", "n", "n", "n", "n", "n", "n"]

        run_generator(
            project_name=project_name,
            package_name=package_name,
            output_dir=output_dir,
            optional_profile="4",
            optionals=optionals,
            include_ml_basics="y"
        )

        advisor_path = output_dir / f"src/{package_name}/advisor.py"
        self.assertTrue(advisor_path.exists())

        content = advisor_path.read_text()
        self.assertIn("class DatasetAdvisor:", content)
        self.assertIn("def run_checks(self):", content)

    def test_advisor_execution(self):
        """Verify the advisor runs and creates artifacts if dependencies are present."""
        is_ci = os.environ.get("GITHUB_ACTIONS") == "true"
        try:
            import pandas
            import numpy
            import sklearn
        except ImportError:
            if is_ci:
                self.fail("ML dependencies (pandas, numpy, sklearn) missing in CI environment.")
            self.skipTest("ML dependencies (pandas, numpy, sklearn) not found. Skipping advisor execution test.")

        project_name = "advisor_exec_project"
        package_name = "advisor_exec_pkg"
        output_dir = self.test_dir / project_name

        optionals = ["y", "n", "n", "n", "n", "n", "n", "n", "n", "y", "n", "n", "n", "n", "n", "n"]

        run_generator(
            project_name=project_name,
            package_name=package_name,
            output_dir=output_dir,
            optional_profile="4",
            optionals=optionals,
            include_ml_basics="y"
        )

        # Create a dummy dataset with various signals using standard csv module
        dataset_path = output_dir / "data/raw/dataset.csv"
        dataset_path.parent.mkdir(parents=True, exist_ok=True)

        headers = ["target", "num_missing", "num_outliers", "cat_high", "date_col", "corr_1", "corr_2"]
        with open(dataset_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for i in range(50):
                target = 1 if i < 5 else 0 # Imbalance (10% vs 90%)
                num_missing = "" if i % 5 == 0 else float(i) # 20% missing
                num_outliers = 100.0 if i % 5 == 0 else 1.0 # Outliers
                cat_high = f"val_{i % 15}" # 15 unique
                date_col = f"2023-01-{(i % 28) + 1:02d}"
                corr_1 = float(i)
                corr_2 = float(i) * 1.000001
                writer.writerow([target, num_missing, num_outliers, cat_high, date_col, corr_1, corr_2])

        # Run the advisor
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

        self.assertEqual(result.returncode, 0, msg=f"Advisor failed with output: {result.stdout}\n{result.stderr}")

        # Verify artifacts
        report_path = output_dir / "reports/dataset-advice.md"
        json_path = output_dir / "configs/suggested_pipeline.json"
        pipeline_path = output_dir / f"src/{package_name}/suggested_pipeline.py"

        self.assertTrue(report_path.exists())
        self.assertTrue(json_path.exists())
        self.assertTrue(pipeline_path.exists())

        report_content = report_path.read_text()
        self.assertIn("Small dataset detected", report_content)
        self.assertIn("Missing values", report_content)
        self.assertIn("Outliers detected", report_content)
        self.assertIn("Imbalanced target", report_content)
        self.assertIn("High numeric correlation", report_content)

        # Verify summary and top next steps in report
        self.assertIn("## Summary", report_content)
        self.assertIn("## Top next steps", report_content)
        self.assertIn("Dataset shape", report_content)
        self.assertIn("Target column", report_content)

        # Verify JSON metadata
        import json
        with open(json_path, "r", encoding="utf-8") as f:
            results = json.load(f)
            self.assertIn("summary", results)
            self.assertIn("next_steps", results)
            self.assertEqual(results["summary"]["dataset_shape"], [50, 7])
            self.assertEqual(results["summary"]["target_column"], "target")
            self.assertGreater(len(results["next_steps"]), 0)

if __name__ == "__main__":
    unittest.main()
