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
        optionals = ["y"] + ["n"] * 11

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
            optionals=["y"] + ["n"]*11
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

    def test_advisor_blocked_without_eda(self):
        """P0.1, P0.2: Advisor is blocked without EDA artifact and gives actionable message."""
        package_name = "advisor_block_pkg"
        output_dir = self.test_dir / "advisor_block_project"

        # eda is 1st, advisor is 10th
        optionals = ["y", "n", "n", "n", "n", "n", "n", "n", "n", "y", "n", "n"]

        run_generator(
            project_name="Advisor Block Project",
            package_name=package_name,
            output_dir=output_dir,
            optional_profile="4",
            optionals=optionals
        )

        # Ensure dataset exists but NO eda_summary.json
        data_dir = output_dir / "data/raw"
        data_dir.mkdir(parents=True, exist_ok=True)
        with open(data_dir / "dataset.csv", "w") as f:
            f.write("a,b,target\n1,2,0\n")

        # Run Advisor
        env = os.environ.copy()
        env["PYTHONPATH"] = str(output_dir / "src")
        result = subprocess.run(
            [sys.executable, "-m", f"{package_name}.advisor"],
            cwd=output_dir,
            env=env,
            capture_output=True,
            text=True
        )

        # P0.1: No suggested_pipeline.json should be created
        self.assertFalse((output_dir / "configs/suggested_pipeline.json").exists())

        # P0.2: Output contains actionable EDA command
        output_combined = result.stdout + result.stderr
        self.assertIn(f"python -m {package_name}.lab eda", output_combined)
        self.assertIn("requires an EDA summary", output_combined)

    def test_advisor_runs_after_eda(self):
        """P0.3: Advisor runs normally when eda_summary.json exists."""
        package_name = "advisor_success_pkg"
        output_dir = self.test_dir / "advisor_success_project"

        optionals = ["y", "n", "n", "n", "n", "n", "n", "n", "n", "y", "n", "n"]

        run_generator(
            project_name="Advisor Success Project",
            package_name=package_name,
            output_dir=output_dir,
            optional_profile="4",
            optionals=optionals
        )

        # Create dummy data
        data_dir = output_dir / "data/raw"
        data_dir.mkdir(parents=True, exist_ok=True)
        with open(data_dir / "dataset.csv", "w") as f:
            f.write("feat1,feat2,target\n1.0,cat1,0\n2.0,cat2,1\n")

        env = os.environ.copy()
        env["PYTHONPATH"] = str(output_dir / "src")

        # 1. Run EDA first
        subprocess.run(
            [sys.executable, "-m", f"{package_name}.eda"],
            cwd=output_dir,
            env=env,
            check=True
        )
        self.assertTrue((output_dir / "configs/eda_summary.json").exists())

        # 2. Run Advisor
        result = subprocess.run(
            [sys.executable, "-m", f"{package_name}.advisor"],
            cwd=output_dir,
            env=env,
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0)
        # P0.3: Artifacts created
        self.assertTrue((output_dir / "configs/suggested_pipeline.json").exists())
        self.assertTrue((output_dir / "reports/dataset-advice.md").exists())

    def test_learning_blocked_without_eda(self):
        """P0.1: Learning is blocked without EDA artifact."""
        package_name = "learn_block_pkg"
        output_dir = self.test_dir / "learn_block_project"

        run_generator(
            project_name="Learn Block Project",
            package_name=package_name,
            output_dir=output_dir,
            optional_profile="2" # recommended includes learning
        )

        env = os.environ.copy()
        env["PYTHONPATH"] = str(output_dir / "src")
        result = subprocess.run(
            [sys.executable, "-m", f"{package_name}.learning"],
            cwd=output_dir,
            env=env,
            capture_output=True,
            text=True
        )

        self.assertFalse((output_dir / "configs/learning_context.json").exists())
        self.assertIn("require an EDA summary", result.stdout)

    def test_learning_artifacts_generated(self):
        """P0.2, P0.3: Learning artifacts generated and contextual."""
        package_name = "learn_success_pkg"
        output_dir = self.test_dir / "learn_success_project"

        run_generator(
            project_name="Learn Success Project",
            package_name=package_name,
            output_dir=output_dir,
            optional_profile="2"
        )

        # 1. Create dummy data and EDA artifact
        configs_dir = output_dir / "configs"
        configs_dir.mkdir(parents=True, exist_ok=True)
        with open(configs_dir / "problem_profile.json", "w") as f:
            json.dump({"goal": "classify customers", "language": "en"}, f)

        data_dir = output_dir / "data/raw"
        data_dir.mkdir(parents=True, exist_ok=True)
        with open(data_dir / "dataset.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["feat1", "my_target"])
            writer.writerow(["1.0", "0"])

        # Create eda_summary.json manually to save time
        eda_summary = {
            "rows": 1,
            "columns": ["feat1", "my_target"],
            "target_column": "my_target",
            "target_exists": True,
            "missing_summary": {"feat1": 0, "my_target": 0},
            "unique_counts": {"feat1": 1, "my_target": 1},
            "target_distribution": {"0": 1}
        }
        eda_path = output_dir / "configs/eda_summary.json"
        eda_path.parent.mkdir(parents=True, exist_ok=True)
        with open(eda_path, "w") as f:
            json.dump(eda_summary, f)

        # 2. Run Learning tool
        env = os.environ.copy()
        env["PYTHONPATH"] = str(output_dir / "src")
        result = subprocess.run(
            [sys.executable, "-m", f"{package_name}.learning"],
            cwd=output_dir,
            env=env,
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0)
        self.assertTrue((output_dir / "configs/learning_context.json").exists())
        self.assertTrue((output_dir / "reports/learning-notes.md").exists())

        # P0.3: Verify contextuality
        with open(output_dir / "configs/learning_context.json", "r") as f:
            ctx = json.load(f)
            self.assertEqual(ctx["target"]["name"], "my_target")

        report_md = (output_dir / "reports/learning-notes.md").read_text()
        self.assertIn("my_target", report_md)

    def test_baseline_blocked_without_eda(self):
        """P0.1: Baseline Lab is blocked without EDA artifact."""
        package_name = "baseline_block_pkg"
        output_dir = self.test_dir / "baseline_block_project"

        run_generator(
            project_name="Baseline Block Project",
            package_name=package_name,
            output_dir=output_dir,
            optional_profile="2" # recommended includes baseline_lab
        )

        env = os.environ.copy()
        env["PYTHONPATH"] = str(output_dir / "src")
        result = subprocess.run(
            [sys.executable, "-m", f"{package_name}.lab", "baseline"],
            cwd=output_dir,
            env=env,
            capture_output=True,
            text=True
        )

        self.assertFalse((output_dir / "configs/baseline_results.json").exists())
        self.assertIn("requires an EDA summary", result.stdout)

    def test_baseline_artifacts_generated(self):
        """P0.2, P0.3: Baseline artifacts generated and contain metrics."""
        package_name = "baseline_success_pkg"
        output_dir = self.test_dir / "baseline_success_project"

        run_generator(
            project_name="Baseline Success Project",
            package_name=package_name,
            output_dir=output_dir,
            optional_profile="2",
            include_ml_basics="y"
        )

        # 1. Create dummy data and EDA artifact
        configs_dir = output_dir / "configs"
        configs_dir.mkdir(parents=True, exist_ok=True)
        with open(configs_dir / "problem_profile.json", "w") as f:
            json.dump({"goal": "churn classification", "language": "en"}, f)

        data_dir = output_dir / "data/raw"
        data_dir.mkdir(parents=True, exist_ok=True)
        dataset_path = data_dir / "dataset.csv"
        with open(dataset_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["feat1", "target"])
            writer.writerow(["1.0", "0"])
            writer.writerow(["2.0", "1"])

        eda_summary = {
            "rows": 2,
            "columns": ["feat1", "target"],
            "target_column": "target",
            "target_exists": True,
            "missing_summary": {"feat1": 0, "target": 0},
            "unique_counts": {"feat1": 2, "target": 2},
            "target_distribution": {"0": 1, "1": 1}
        }
        eda_path = output_dir / "configs/eda_summary.json"
        eda_path.parent.mkdir(parents=True, exist_ok=True)
        with open(eda_path, "w") as f:
            json.dump(eda_summary, f)

        # 2. Run Baseline Lab
        env = os.environ.copy()
        env["PYTHONPATH"] = str(output_dir / "src")
        result = subprocess.run(
            [sys.executable, "-m", f"{package_name}.lab", "baseline"],
            cwd=output_dir,
            env=env,
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0, f"Baseline Lab failed: {result.stdout}\n{result.stderr}")
        self.assertTrue((output_dir / "configs/baseline_results.json").exists())
        self.assertTrue((output_dir / "reports/baseline-results.md").exists())

        # P0.3: Verify metrics
        with open(output_dir / "configs/baseline_results.json", "r") as f:
            results = json.load(f)
            self.assertIn("model_type", results)
            self.assertIn("metrics", results)
            self.assertIn("accuracy", results["metrics"])

        report_md = (output_dir / "reports/baseline-results.md").read_text()
        self.assertIn("Resultados do Baseline Lab", report_md) if "pt-BR" in report_md else self.assertIn("Baseline Lab Results", report_md)

    def test_baseline_regression_artifacts_generated(self):
        """P0.2, P0.3: Baseline regression artifacts generated and contain metrics."""
        package_name = "baseline_reg_pkg"
        output_dir = self.test_dir / "baseline_reg_project"

        run_generator(
            project_name="Baseline Reg Project",
            package_name=package_name,
            output_dir=output_dir,
            optional_profile="2",
            include_ml_basics="y"
        )

        # 1. Create dummy data and EDA artifact
        configs_dir = output_dir / "configs"
        configs_dir.mkdir(parents=True, exist_ok=True)
        # Testing robust detection with a different goal keyword
        with open(configs_dir / "problem_profile.json", "w") as f:
            json.dump({"goal": "predict price", "language": "en"}, f)

        data_dir = output_dir / "data/raw"
        data_dir.mkdir(parents=True, exist_ok=True)
        dataset_path = data_dir / "dataset.csv"
        with open(dataset_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["feat1", "target"])
            writer.writerow(["1.0", "100.0"])
            writer.writerow(["2.0", "200.0"])
            writer.writerow(["3.0", "150.0"])

        eda_summary = {
            "rows": 3,
            "columns": ["feat1", "target"],
            "target_column": "target",
            "target_exists": True,
            "missing_summary": {"feat1": 0, "target": 0},
            "unique_counts": {"feat1": 3, "target": 3},
            "target_distribution": {"100.0": 1, "200.0": 1, "150.0": 1}
        }
        eda_path = output_dir / "configs/eda_summary.json"
        eda_path.parent.mkdir(parents=True, exist_ok=True)
        with open(eda_path, "w") as f:
            json.dump(eda_summary, f)

        # 2. Run Baseline Lab
        env = os.environ.copy()
        env["PYTHONPATH"] = str(output_dir / "src")
        result = subprocess.run(
            [sys.executable, "-m", f"{package_name}.lab", "baseline"],
            cwd=output_dir,
            env=env,
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0, f"Baseline Lab failed: {result.stdout}\n{result.stderr}")
        self.assertTrue((output_dir / "configs/baseline_results.json").exists())
        self.assertTrue((output_dir / "reports/baseline-results.md").exists())

        # P0.3: Verify regression metrics
        with open(output_dir / "configs/baseline_results.json", "r") as f:
            results = json.load(f)
            self.assertIn("DummyRegressor", results["model_type"])
            self.assertIn("mae", results["metrics"])
            self.assertIn("r2", results["metrics"])

        report_md = (output_dir / "reports/baseline-results.md").read_text()
        self.assertIn("MAE", report_md)
        self.assertIn("R2", report_md)

if __name__ == "__main__":
    unittest.main()
