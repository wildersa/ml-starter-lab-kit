import unittest
import shutil
import tempfile
import os
import subprocess
import json
import sys
from pathlib import Path
from tests.helpers import run_generator

class TestRunContract(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.project_name = "contract_proj"
        self.package_name = "contract_pkg"

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_run_contract_supervised(self):
        # 1. Generate project
        run_generator(
            project_name=self.project_name,
            package_name=self.package_name,
            task="2", # supervised
            dataset_path="data/raw/train.csv",
            target_column="target",
            output_dir=self.test_dir,
            include_ml_basics="n"
        )

        # 2. Create dummy data
        data_dir = self.test_dir / "data/raw"
        data_dir.mkdir(parents=True, exist_ok=True)
        train_csv = data_dir / "train.csv"
        with open(train_csv, "w") as f:
            f.write("feature1,target\n1,A\n2,B\n3,A\n")

        # 3. Run modules using python -m contract_pkg.<module>
        # We use PYTHONPATH=src to simulate an installed package in the src/ layout
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.test_dir / "src")

        # Run data.py
        subprocess.check_call(
            [sys.executable, "-m", f"{self.package_name}.data"],
            cwd=self.test_dir,
            env=env
        )
        self.assertTrue((self.test_dir / "data/processed/modeling_table.csv").exists())

        # Run train.py
        subprocess.check_call(
            [sys.executable, "-m", f"{self.package_name}.train"],
            cwd=self.test_dir,
            env=env
        )
        self.assertTrue((self.test_dir / "models/model.json").exists())

        with open(self.test_dir / "models/model.json") as f:
            model = json.load(f)
            self.assertEqual(model["prediction"], "A")

        # Run evaluate.py
        subprocess.check_call(
            [sys.executable, "-m", f"{self.package_name}.evaluate"],
            cwd=self.test_dir,
            env=env
        )
        self.assertTrue((self.test_dir / "reports/metrics.json").exists())

        with open(self.test_dir / "reports/metrics.json") as f:
            metrics = json.load(f)
            self.assertIn("accuracy", metrics)

if __name__ == "__main__":
    unittest.main()
