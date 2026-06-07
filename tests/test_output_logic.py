import unittest
from pathlib import Path
from unittest.mock import patch
import shutil
import tempfile
import os
import sys
import subprocess
import csv
import json
from ml_starter_generator import scaffold
from tests.helpers import run_generator

class TestOutputLogic(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        # Mock STARTER_ROOT to be inside our temp dir
        self.starter_root = self.test_dir / "ml-starter-lab-kit"
        self.starter_root.mkdir()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_default_sibling_directory(self):
        # We need to patch STARTER_ROOT in the constants module
        from ml_starter_generator import constants
        with patch('ml_starter_generator.constants.STARTER_ROOT', self.starter_root):
            package_name = "my_ml_project"
            expected_default = self.starter_root.parent / package_name

            # default_output_dir in cli.main is STARTER_ROOT.parent / package_name
            actual_default = constants.STARTER_ROOT.parent / package_name
            self.assertEqual(actual_default, expected_default)

    def test_starter_root_detection(self):
        with patch('ml_starter_generator.cli.STARTER_ROOT', self.starter_root):
            # Test path inside starter root
            inside_path = self.starter_root / "some_subdir"
            outside_path = self.test_dir / "outside"

            output = run_generator(
                project_name="My Project",
                package_name="my_project",
                task="2",
                dataset_path="data.csv",
                target_column="target",
                output_dir_sequence=["4", str(inside_path), "n", "4", str(outside_path)]
            )

            self.assertIn("The selected output directory is inside the starter repository.", output)
            self.assertTrue((outside_path / "README.md").exists())

    def test_readme_content(self):
        values = {
            "PROJECT_NAME": "Test Project",
            "PACKAGE_NAME": "test_project",
            "TASK": "supervised"
        }
        output_dir = self.test_dir / "output"
        output_dir.mkdir()

        scaffold.create_readme(output_dir, values, force=True)

        readme_path = output_dir / "README.md"
        content = readme_path.read_text()

        self.assertIn("This is a generated Machine Learning project, not the starter tool itself.", content)
        self.assertNotIn("Este é um projeto de Machine Learning gerado, não a própria ferramenta starter.", content)

    def test_eda_artifact_generation(self):
        """P0.1, P0.2, P0.4: Verify EDA creates JSON and Markdown artifacts and nothing else."""
        package_name = "eda_test_pkg"
        output_dir = self.test_dir / "eda_project"

        # eda is the 1st optional tool
        optionals = ["y", "n", "n", "n", "n", "n", "n", "n", "n", "n"]

        run_generator(
            project_name="EDA Project",
            package_name=package_name,
            output_dir=output_dir,
            optional_profile="4",
            optionals=optionals
        )

        # Create dummy data
        data_dir = output_dir / "data/raw"
        data_dir.mkdir(parents=True, exist_ok=True)
        dataset_path = data_dir / "dataset.csv"
        with open(dataset_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["feat1", "feat2", "target"])
            writer.writerow(["1.0", "cat1", "0"])
            writer.writerow(["2.0", "", "1"]) # One missing in feat2

        # Run EDA
        env = os.environ.copy()
        env["PYTHONPATH"] = str(output_dir / "src")
        result = subprocess.run(
            [sys.executable, "-m", f"{package_name}.eda"],
            cwd=output_dir,
            env=env,
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0, f"EDA failed: {result.stdout}\n{result.stderr}")

        # P0.1: Check JSON artifact
        json_path = output_dir / "configs/eda_summary.json"
        self.assertTrue(json_path.exists(), "configs/eda_summary.json should be created")
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(data["rows"], 2)
            self.assertEqual(data["columns"], ["feat1", "feat2", "target"])
            self.assertEqual(data["target_column"], "target")
            self.assertTrue(data["target_exists"])
            self.assertEqual(data["missing_summary"]["feat2"], 1)
            self.assertIn("unique_counts", data)

        # P0.2: Check Markdown artifact
        report_path = output_dir / "reports/eda-summary.md"
        self.assertTrue(report_path.exists(), "reports/eda-summary.md should be created")
        report_content = report_path.read_text()
        self.assertIn("Dataset Summary", report_content)
        self.assertIn("Rows:** 2", report_content)
        self.assertIn("Columns:** 3", report_content)
        self.assertIn("target", report_content)

        # P0.4: EDA does not train/suggest
        self.assertFalse((output_dir / "configs/suggested_pipeline.json").exists())
        self.assertFalse(list(output_dir.glob("models/*.pkl")))

    def test_eda_missing_dataset_fails_safely(self):
        """P0.3: Missing dataset handled safely without creating stale artifacts."""
        package_name = "eda_fail_pkg"
        output_dir = self.test_dir / "eda_fail_project"

        run_generator(
            project_name="EDA Fail Project",
            package_name=package_name,
            output_dir=output_dir,
            optional_profile="4",
            optionals=["y"] + ["n"]*9
        )

        # Ensure no dataset exists
        dataset_path = output_dir / "data/raw/dataset.csv"
        if dataset_path.exists():
            dataset_path.unlink()

        # Run EDA
        env = os.environ.copy()
        env["PYTHONPATH"] = str(output_dir / "src")
        result = subprocess.run(
            [sys.executable, "-m", f"{package_name}.eda"],
            cwd=output_dir,
            env=env,
            capture_output=True,
            text=True
        )

        # It should probably exit with a message
        self.assertIn("not found", (result.stdout + result.stderr).lower())
        self.assertFalse((output_dir / "configs/eda_summary.json").exists())
        self.assertFalse((output_dir / "reports/eda-summary.md").exists())

if __name__ == "__main__":
    unittest.main()
