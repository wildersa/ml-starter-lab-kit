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

class TestFeatureScreening(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.project_name = "screening_project"
        self.package_name = "screening_project"

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_screening_generation_and_execution(self):
        # 1. Generate project with screening enabled
        # screening is at index 11 (if we count eda=0, pre=1, met=2, opt=3, feat_m=4, vis=5, nb=6, rep=7, exp=8, adv=9, ins=10, scr=11)
        # Let's verify the order in cli.py or use recommended profile
        run_generator(
            project_name=self.project_name,
            package_name=self.package_name,
            task="2", # supervised
            dataset_path="data/raw/dataset.csv",
            target_column="target",
            include_demo="n",
            output_dir=self.test_dir,
            optional_profile="2", # recommended includes screening
            include_ml_basics="y"
        )

        pkg_path = self.test_dir / "src" / self.package_name
        screening_py = pkg_path / "feature_screening.py"
        self.assertTrue(screening_py.exists(), "feature_screening.py should be generated")

        # 2. Create a dummy dataset
        data_dir = self.test_dir / "data/raw"
        data_dir.mkdir(parents=True, exist_ok=True)
        dataset_path = data_dir / "dataset.csv"

        with open(dataset_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["target", "feat1", "feat2", "leak"])
            for i in range(100):
                target = i % 2
                feat1 = float(i)
                feat2 = 0.5
                leak = target # Perfect leakage
                writer.writerow([target, feat1, feat2, leak])

        # 3. Execute the screening command via CLI
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.test_dir / "src")

        result = subprocess.run(
            [sys.executable, "-m", f"{self.package_name}.lab", "screening"],
            cwd=self.test_dir,
            env=env,
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0, f"Screening command failed: {result.stdout}\n{result.stderr}")

        # 4. Verify artifacts
        reports_dir = self.test_dir / "reports"
        md_report = reports_dir / "quick-model-report.md"
        json_metrics = reports_dir / "quick-model-metrics.json"
        csv_importance = reports_dir / "feature-importance.csv"

        self.assertTrue(md_report.exists())
        self.assertTrue(json_metrics.exists())
        self.assertTrue(csv_importance.exists())

        # 5. Verify content
        with open(json_metrics, "r") as f:
            results = json.load(f)
            self.assertIn("metrics", results)
            self.assertIn("accuracy", results["metrics"])
            self.assertGreater(len(results["warnings"]), 0, "Leakage warning should be present")

        md_content = md_report.read_text()
        self.assertIn("Diagnostic Model & Feature Importance", md_content)
        self.assertIn("SUSPICIOUS SIGNAL", md_content)

if __name__ == "__main__":
    unittest.main()
