import unittest
from pathlib import Path
import shutil
import tempfile
import os
import sys
import subprocess
import json
import pandas as pd
from tests.helpers import run_generator

class TestSyntheticDataLab(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_synthetic_data_generation_scenarios(self):
        """Verify that all synthetic data scenarios can be generated."""
        package_name = "synth_test_pkg"
        output_dir = self.test_dir / "synth_test_project"

        run_generator(
            project_name="Synthetic Test Project",
            package_name=package_name,
            output_dir=output_dir,
            task="2",
            experience_mode="1",
            optional_profile="3" # Full profile includes synthetic_data
        )

        scenarios = [
            "classification",
            "regression",
            "clustering",
            "timeseries",
            "bandit_simple",
            "bandit_contextual_events"
        ]

        env = os.environ.copy()
        env["PYTHONPATH"] = str(output_dir / "src")

        config_path = output_dir / "configs/synthetic_data.json"

        for scenario in scenarios:
            # Update config for the scenario
            with open(config_path, "r") as f:
                config = json.load(f)

            config["scenario"] = scenario
            if scenario in config.get("scenario_examples", {}):
                config["parameters"] = config["scenario_examples"][scenario]

            with open(config_path, "w") as f:
                json.dump(config, f)

            # Run synthetic data generation
            result = subprocess.run(
                [sys.executable, "-m", f"{package_name}.lab", "synthetic"],
                cwd=output_dir,
                env=env,
                capture_output=True,
                text=True
            )

            self.assertEqual(result.returncode, 0, f"Scenario {scenario} failed:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}")

            # Check if artifacts exist
            data_file = output_dir / f"data/synthetic/{scenario}.csv"
            meta_file = output_dir / f"data/synthetic/{scenario}_meta.json"
            report_file = output_dir / "reports/synthetic-data-summary.md"

            self.assertTrue(data_file.exists(), f"Data file for {scenario} missing")
            self.assertTrue(meta_file.exists(), f"Meta file for {scenario} missing")
            self.assertTrue(report_file.exists(), f"Report file for {scenario} missing")

            # Basic data validation
            df = pd.read_csv(data_file)
            self.assertGreater(len(df), 0)

            if scenario == "classification":
                self.assertIn("target", df.columns)
            elif scenario == "regression":
                self.assertIn("target", df.columns)
            elif scenario == "timeseries":
                self.assertIn("date", df.columns)
                self.assertIn("value", df.columns)
            elif scenario == "bandit_simple":
                self.assertIn("round", df.columns)
                self.assertIn("arm", df.columns)
                self.assertIn("reward", df.columns)
            elif scenario == "bandit_contextual_events":
                self.assertIn("action", df.columns)
                self.assertIn("reward", df.columns)
                self.assertTrue(any(c.startswith("context_") for c in df.columns))

    def test_synthetic_data_determinism(self):
        """Verify that synthetic data generation is deterministic with the same seed."""
        package_name = "synth_det_pkg"
        output_dir = self.test_dir / "synth_det_project"

        run_generator(
            project_name="Synthetic Determinism Project",
            package_name=package_name,
            output_dir=output_dir,
            task="2",
            experience_mode="1",
            optional_profile="3"
        )

        env = os.environ.copy()
        env["PYTHONPATH"] = str(output_dir / "src")

        # Run twice and compare
        data_paths = []
        for i in range(2):
            subprocess.run(
                [sys.executable, "-m", f"{package_name}.lab", "synthetic"],
                cwd=output_dir,
                env=env,
                capture_output=True
            )
            df = pd.read_csv(output_dir / "data/synthetic/classification.csv")
            data_paths.append(df)

        pd.testing.assert_frame_equal(data_paths[0], data_paths[1])

if __name__ == "__main__":
    unittest.main()
