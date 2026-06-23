import unittest
import shutil
import tempfile
import os
import json
from pathlib import Path
import sys
import subprocess
import csv

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
        # 1. Generate project with insights enabled
        run_generator(
            project_name=self.project_name,
            package_name=self.package_name,
            task="2", # supervised
            dataset_path="data/raw/dataset.csv",
            target_column="target",
            include_demo="n", # we'll create custom data
            output_dir=self.test_dir,
            optional_profile="2", # recommended includes insights
            include_ml_basics="y"
        )

        pkg_path = self.test_dir / "src" / self.package_name
        insights_py = pkg_path / "data_insights.py"
        self.assertTrue(insights_py.exists(), "data_insights.py should be generated")

        # 2. Create a dummy dataset with specific signals to trigger warnings
        data_dir = self.test_dir / "data/raw"
        data_dir.mkdir(parents=True, exist_ok=True)
        dataset_path = data_dir / "dataset.csv"

        # signals:
        # - constant column (const)
        # - leakage name (target_leaked)
        # - high multicollinearity (corr1, corr2)
        # - near perfect signal (perfect_feat)
        # - imbalance (target) - we need < 10% for the warning to trigger
        with open(dataset_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["target", "const", "target_leaked", "corr1", "corr2", "perfect_feat", "noise"])
            for i in range(100):
                target = 1 if i < 5 else 0 # 5% imbalance
                const = 1
                leaked = target
                c1 = float(i)
                c2 = float(i) * 1.0001
                perfect = target
                noise = float(i % 7)
                writer.writerow([target, const, leaked, c1, c2, perfect, noise])

        # 3. Execute the insights command via CLI
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.test_dir / "src")

        # We also need an EDA summary as it's a typical prerequisite for modeling modules in this scaffold
        # though DataInsights currently loads config directly, let's follow the standard flow
        subprocess.run(
            [sys.executable, "-m", f"{self.package_name}.eda"],
            cwd=self.test_dir,
            env=env,
            check=True
        )

        result = subprocess.run(
            [sys.executable, "-m", f"{self.package_name}.lab", "insights"],
            cwd=self.test_dir,
            env=env,
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0, f"Insights command failed: {result.stdout}\n{result.stderr}")

        # 4. Verify artifacts
        reports_dir = self.test_dir / "reports"
        md_report = reports_dir / "data-quality-report.md"
        json_report = reports_dir / "data-insights.json"
        csv_screening = reports_dir / "feature-screening.csv"

        self.assertTrue(md_report.exists())
        self.assertTrue(json_report.exists())
        self.assertTrue(csv_screening.exists())

        # 5. Verify content of artifacts
        with open(json_report, "r") as f:
            insights = json.load(f)
            warnings = insights["warnings"]
            warning_types = [w["type"] for w in warnings]

            self.assertIn("constant_column", warning_types)
            self.assertIn("leakage_name", warning_types)
            self.assertIn("multicollinearity", warning_types)
            self.assertIn("leakage_signal", warning_types)
            self.assertIn("imbalance", warning_types)

        md_content = md_report.read_text()
        self.assertIn("Dataset Intelligence Report", md_content)
        self.assertIn("WARNING", md_content)

    def test_insights_custom_selection(self):
        # 17 optionals (after adding feature_screening), insights is at index 10
        optionals = ["n"] * 17
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
