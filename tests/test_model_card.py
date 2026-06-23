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

class TestModelCard(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.project_name = "model_card_project"
        self.package_name = "model_card_project"

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_model_card_generation(self):
        # 1. Generate project with all diagnostic tools
        run_generator(
            project_name=self.project_name,
            package_name=self.package_name,
            task="2", # supervised
            dataset_path="data/raw/dataset.csv",
            target_column="target",
            include_demo="n",
            output_dir=self.test_dir,
            optional_profile="2", # recommended includes insights, screening, etc.
            include_ml_basics="y"
        )

        pkg_path = self.test_dir / "src" / self.package_name
        model_card_py = pkg_path / "model_card.py"
        self.assertTrue(model_card_py.exists(), "model_card.py should be generated")

        # 2. Create a dummy dataset
        data_dir = self.test_dir / "data/raw"
        data_dir.mkdir(parents=True, exist_ok=True)
        dataset_path = data_dir / "dataset.csv"

        with open(dataset_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["target", "feat1", "feat2"])
            for i in range(100):
                target = i % 2
                feat1 = float(i)
                feat2 = 0.5
                writer.writerow([target, feat1, feat2])

        # 3. Create problem profile
        configs_dir = self.test_dir / "configs"
        configs_dir.mkdir(parents=True, exist_ok=True)
        with open(configs_dir / "problem_profile.json", "w") as f:
            json.dump({
                "goal": "Test model card generation",
                "language": "en",
                "next_steps": ["Improve features", "Try more models"]
            }, f)

        # 4. Run insights and screening to have some artifacts
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.test_dir / "src")

        subprocess.run(
            [sys.executable, "-m", f"{self.package_name}.lab", "insights"],
            cwd=self.test_dir, env=env, capture_output=True
        )
        subprocess.run(
            [sys.executable, "-m", f"{self.package_name}.lab", "screening"],
            cwd=self.test_dir, env=env, capture_output=True
        )

        # 5. Run model-card command
        result = subprocess.run(
            [sys.executable, "-m", f"{self.package_name}.lab", "model-card"],
            cwd=self.test_dir,
            env=env,
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0, f"Model Card command failed: {result.stdout}\n{result.stderr}")

        # 6. Verify artifact
        model_card_md = self.test_dir / "reports" / "model-card.md"
        self.assertTrue(model_card_md.exists())

        content = model_card_md.read_text()
        self.assertIn("Model Card — model_card_project", content)
        self.assertIn("## 1. Project Summary", content)
        self.assertIn("## 2. Dataset and Features", content)
        self.assertIn("## 4. Performance Metrics", content)
        self.assertIn("Diagnostic Metrics", content)
        self.assertIn("Improve features", content)

    def test_model_card_graceful_degradation(self):
        # Test generation even when other artifacts are missing
        run_generator(
            project_name=self.project_name,
            package_name=self.package_name,
            task="2",
            dataset_path="data/raw/dataset.csv",
            target_column="target",
            include_demo="n",
            output_dir=self.test_dir,
            optional_profile="2",
            include_ml_basics="y"
        )

        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.test_dir / "src")

        result = subprocess.run(
            [sys.executable, "-m", f"{self.package_name}.lab", "model-card"],
            cwd=self.test_dir,
            env=env,
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0)
        model_card_md = self.test_dir / "reports" / "model-card.md"
        self.assertTrue(model_card_md.exists())

        content = model_card_md.read_text()
        self.assertIn("Not available yet", content)

if __name__ == "__main__":
    unittest.main()
