import unittest
from pathlib import Path
import shutil
import tempfile
import os
import sys
import subprocess
from tests.helpers import run_generator

class TestBanditMetricsDependency(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_bandit_lab_forces_metrics_generation(self):
        """Verify that enabling Bandit Lab forces metrics.py generation even if not selected."""
        package_name = "bandit_no_metrics_pkg"
        output_dir = self.test_dir / "bandit_no_metrics_project"

        # Experience Mode 1 (Minimal), Task 2 (Classification)
        # Profile 4 (Custom) - we will need to simulate the interactive selection
        # But wait, run_generator in helpers.py might not support custom selection well.

        # Let's check tests/helpers.py to see how run_generator handles input

        # Index mapping in cli.py:
        # 0: eda, 1: preprocessing, 2: metrics, 3: optimization, 4: feature_measurement,
        # 5: visualization, 6: notebook_factory, 7: model_report, 8: experiment_log,
        # 9: advisor, 10: learning, 11: baseline_lab, 12: bandit_lab

        # We want to enable bandit_lab (index 12) and DISABLE metrics (index 2)
        optionals = ["n"] * 16
        optionals[2] = "n" # Metrics
        optionals[12] = "y" # Bandit Lab

        run_generator(
            project_name="Bandit No Metrics Project",
            package_name=package_name,
            output_dir=output_dir,
            task="1", # Tabular Classification
            experience_mode="1", # Minimal
            optional_profile="4", # Custom
            optionals=optionals
        )

        # Check if metrics.py exists
        metrics_py_path = output_dir / f"src/{package_name}/metrics.py"
        bandit_lab_py_path = output_dir / f"src/{package_name}/bandit_lab.py"

        self.assertTrue(bandit_lab_py_path.exists(), "bandit_lab.py should be generated")
        self.assertTrue(metrics_py_path.exists(), "metrics.py should be forced by bandit_lab")

        # Verify it runs without ModuleNotFoundError
        env = os.environ.copy()
        env["PYTHONPATH"] = str(output_dir / "src")
        result = subprocess.run(
            [sys.executable, "-m", f"{package_name}.lab", "bandit"],
            cwd=output_dir,
            env=env,
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0, f"Bandit Lab failed to run: {result.stderr}")
        self.assertIn("Bandit Lab simulation complete", result.stdout)

if __name__ == "__main__":
    unittest.main()
