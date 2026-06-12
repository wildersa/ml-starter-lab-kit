import unittest
import shutil
import tempfile
import os
import subprocess
import json
import sys
from pathlib import Path
from tests.helpers import run_generator

class TestEvaluateTasks(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.project_name = "task_proj"
        self.package_name = "task_pkg"

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def run_pipeline(self, project_path, package_name):
        env = os.environ.copy()
        env["PYTHONPATH"] = str(project_path / "src")

        # Run train.py
        subprocess.check_call(
            [sys.executable, "-m", f"{package_name}.train"],
            cwd=project_path,
            env=env
        )

        # Run evaluate.py
        subprocess.check_call(
            [sys.executable, "-m", f"{package_name}.evaluate"],
            cwd=project_path,
            env=env
        )

        metrics_json = project_path / "reports/metrics.json"
        with open(metrics_json) as f:
            return json.load(f)

    def test_p0_1_classification_evaluation(self):
        """P0.1: Classification evaluation includes precision/recall/F1 or confusion data."""
        run_generator(
            project_name=self.project_name,
            package_name=self.package_name,
            task="2", # supervised
            problem_goal="predict a category",
            output_dir=self.test_dir
        )

        # Create dummy data
        data_dir = self.test_dir / "data/processed"
        data_dir.mkdir(parents=True, exist_ok=True)
        with open(data_dir / "modeling_table.csv", "w") as f:
            f.write("f1,target\n1,A\n2,A\n3,B\n4,B\n")

        metrics = self.run_pipeline(self.test_dir, self.package_name)

        self.assertEqual(metrics["metric"], "accuracy")
        self.assertIn("precision", metrics)
        self.assertIn("recall", metrics)
        self.assertIn("f1_score", metrics)
        self.assertIn("confusion_matrix", metrics)
        self.assertIn("tp", metrics["confusion_matrix"])

    def test_p0_2_regression_evaluation(self):
        """P0.2: Regression evaluation includes MAE/RMSE/MAPE or R² and does not include accuracy."""
        run_generator(
            project_name=self.project_name,
            package_name=self.package_name,
            task="2", # supervised
            problem_goal="predict a number",
            output_dir=self.test_dir
        )

        # Create dummy data
        data_dir = self.test_dir / "data/processed"
        data_dir.mkdir(parents=True, exist_ok=True)
        with open(data_dir / "modeling_table.csv", "w") as f:
            f.write("f1,target\n1,10\n2,20\n3,30\n4,40\n")

        metrics = self.run_pipeline(self.test_dir, self.package_name)

        self.assertEqual(metrics["metric"], "rmse")
        self.assertIn("rmse", metrics)
        self.assertIn("mae", metrics)
        self.assertIn("mape", metrics)
        self.assertIn("r2", metrics)
        self.assertNotIn("accuracy", metrics)

    def test_p0_3_timeseries_evaluation(self):
        """P0.3: Time-series evaluation includes forecast metric family and time-aware limitation."""
        run_generator(
            project_name=self.project_name,
            package_name=self.package_name,
            task="4", # timeseries
            output_dir=self.test_dir
        )

        # Create dummy data
        data_dir = self.test_dir / "data/processed"
        data_dir.mkdir(parents=True, exist_ok=True)
        with open(data_dir / "modeling_table.csv", "w") as f:
            f.write("date,target\n2023-01-01,10\n2023-01-02,20\n")

        metrics = self.run_pipeline(self.test_dir, self.package_name)

        self.assertEqual(metrics["metric"], "rmse")
        self.assertIn("rmse", metrics)
        self.assertIn("note", metrics)
        self.assertIn("Backtesting", metrics["note"])

    def test_p0_4_placeholders(self):
        """P0.4: Clustering/vision/bandit avoid wrong generic metrics and use placeholders."""
        tasks = [
            ("3", "silhouette_placeholder"), # unsupervised
            ("5", "mAP_placeholder"),        # vision
        ]

        for task_id, expected_metric in tasks:
            subdir = self.test_dir / f"task_{task_id}"
            run_generator(
                project_name=self.project_name,
                package_name=self.package_name,
                task=task_id,
                output_dir=subdir
            )

            # Create dummy data
            data_dir = subdir / "data/processed"
            data_dir.mkdir(parents=True, exist_ok=True)
            with open(data_dir / "modeling_table.csv", "w") as f:
                f.write("f1,target\n1,A\n2,B\n")

            metrics = self.run_pipeline(subdir, self.package_name)
            self.assertEqual(metrics["metric"], expected_metric)
            self.assertIn("note", metrics)

    def test_p0_5_generic_fallback(self):
        """P0.5: Unknown/generic task falls back safely."""
        run_generator(
            project_name=self.project_name,
            package_name=self.package_name,
            task="1", # generic
            output_dir=self.test_dir
        )

        # Create dummy data
        data_dir = self.test_dir / "data/processed"
        data_dir.mkdir(parents=True, exist_ok=True)
        with open(data_dir / "modeling_table.csv", "w") as f:
            f.write("f1,target\n1,A\n2,B\n")

        metrics = self.run_pipeline(self.test_dir, self.package_name)
        # Generic task currently defaults to classification baseline in train.py.tpl
        self.assertEqual(metrics["metric"], "accuracy")

if __name__ == "__main__":
    unittest.main()
