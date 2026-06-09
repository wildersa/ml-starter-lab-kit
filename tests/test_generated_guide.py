import unittest
import os
import shutil
import tempfile
import subprocess
import sys
from pathlib import Path
from tests.helpers import run_generator

class TestGeneratedGuide(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.package_name = "test_pkg"

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def run_guide(self, cwd):
        env = os.environ.copy()
        env["PYTHONPATH"] = str(cwd / "src")
        env["PYTHONIOENCODING"] = "utf-8"
        result = subprocess.run(
            [sys.executable, "-m", f"{self.package_name}.guide"],
            cwd=cwd,
            capture_output=True,
            text=True,
            env=env
        )
        return result

    def test_guide_creation_and_basic_behavior(self):
        """P0.1, P0.2, P0.3, P0.4, P0.6, P0.8"""
        run_generator(
            project_name="test_proj",
            package_name=self.package_name,
            task="2",
            dataset_path="data/raw/dataset.csv",
            target_column="target",
            output_dir=self.test_dir,
            optional_profile="2" # recommended (includes advisor)
        )

        guide_path = self.test_dir / "src" / self.package_name / "guide.py"
        self.assertTrue(guide_path.exists(), "P0.1: guide.py should be created")

        # Create a dummy dataset
        data_dir = self.test_dir / "data/raw"
        data_dir.mkdir(parents=True, exist_ok=True)
        dataset_path = data_dir / "dataset.csv"
        with open(dataset_path, "w", encoding="utf-8") as f:
            f.write("feat1,feat2,target,date_col\n1.0,cat1,0,2023-01-01\n2.0,cat2,1,2023-01-02")

        result = self.run_guide(self.test_dir)
        output = result.stdout

        self.assertEqual(result.returncode, 0, f"Guide should run successfully. Error: {result.stderr}")
        self.assertIn("data/raw/dataset.csv", output, "P0.2: Should mention dataset path")
        self.assertIn("feat1", output, "P0.3: Should list columns")
        self.assertIn("target", output, "P0.4: Should find target")
        self.assertIn("numeric", output.lower(), "P0.3: Should suggest types")
        self.assertIn(f"python -m {self.package_name}.lab advisor", output, "P0.6: Should suggest advisor")
        self.assertIn(f"python -m {self.package_name}.lab eda", output, "P0.6: Should suggest eda")

    def test_guide_missing_target(self):
        """P0.5"""
        run_generator(
            project_name="test_proj",
            package_name=self.package_name,
            task="2",
            dataset_path="data/raw/dataset.csv",
            target_column="wrong_target",
            output_dir=self.test_dir
        )

        data_dir = self.test_dir / "data/raw"
        data_dir.mkdir(parents=True, exist_ok=True)
        dataset_path = data_dir / "dataset.csv"
        with open(dataset_path, "w", encoding="utf-8") as f:
            f.write("feat1,actual_target\n1.0,0")

        result = self.run_guide(self.test_dir)
        output = result.stdout

        self.assertIn("WARNING", output.upper(), "P0.5: Should warn about missing target")
        self.assertIn("wrong_target", output, "P0.5: Should mention missing target")
        self.assertIn("actual_target", output, "P0.5: Should suggest candidates")

    def test_guide_missing_dataset(self):
        """P0.7"""
        run_generator(
            project_name="test_proj",
            package_name=self.package_name,
            task="2",
            dataset_path="data/raw/missing.csv",
            output_dir=self.test_dir
        )

        result = self.run_guide(self.test_dir)
        output = result.stdout

        self.assertIn("not found", output.lower(), "P0.7: Should inform about missing dataset")
        self.assertIn("data/raw/missing.csv", output, "P0.7: Should mention the path")
        self.assertNotIn("Traceback", output, "P0.7: Should not show traceback")

    def test_guide_no_advisor(self):
        """P0.6: advisor command appears only when generated"""
        run_generator(
            project_name="test_proj",
            package_name=self.package_name,
            task="2",
            output_dir=self.test_dir,
            optional_profile="1" # minimal (no advisor)
        )

        # Create dummy data so it doesn't stop at missing dataset
        data_dir = self.test_dir / "data/raw"
        data_dir.mkdir(parents=True, exist_ok=True)
        dataset_path = data_dir / "dataset.csv"
        with open(dataset_path, "w", encoding="utf-8") as f:
            f.write("feat1,target\n1.0,0")

        result = self.run_guide(self.test_dir)
        output = result.stdout

        self.assertNotIn(f"python -m {self.package_name}.lab advisor", output, "P0.6: Should NOT suggest advisor")

if __name__ == "__main__":
    unittest.main()
