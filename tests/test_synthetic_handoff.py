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

class TestSyntheticHandoff(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_synthetic_to_pipeline_handoff(self):
        """Verify the full flow: synthetic generation -> config update -> data -> train."""
        package_name = "handoff_pkg"
        output_dir = self.test_dir / "handoff_project"

        # 1. Run generator
        run_generator(
            project_name="Handoff Project",
            package_name=package_name,
            output_dir=output_dir,
            task="2", # supervised
            experience_mode="1", # minimal
            optional_profile="2" # recommended (includes synthetic)
        )

        env = os.environ.copy()
        env["PYTHONPATH"] = str(output_dir / "src")

        # 2. Update synthetic config to activate
        synth_config_path = output_dir / "configs/synthetic_data.json"
        with open(synth_config_path, "r") as f:
            synth_config = json.load(f)

        synth_config["activate_as_project_dataset"] = True
        synth_config["scenario"] = "classification"

        with open(synth_config_path, "w") as f:
            json.dump(synth_config, f)

        # 3. Run synthetic generation
        result = subprocess.run(
            [sys.executable, "-m", f"{package_name}.lab", "synthetic"],
            cwd=output_dir,
            env=env,
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0, f"Synthetic generation failed: {result.stdout}\n{result.stderr}")
        self.assertIn("Project configuration updated!", result.stdout)

        # 4. Verify config.json update
        config_path = output_dir / "configs/config.json"
        with open(config_path, "r") as f:
            project_config = json.load(f)

        self.assertEqual(project_config["data"]["raw_path"], "data/synthetic/classification.csv")
        self.assertEqual(project_config["target"]["column"], "target")

        # 5. Run lab data
        result = subprocess.run(
            [sys.executable, "-m", f"{package_name}.lab", "data"],
            cwd=output_dir,
            env=env,
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0, f"Lab data failed: {result.stdout}\n{result.stderr}")

        processed_path = output_dir / "data/processed/modeling_table.csv"
        self.assertTrue(processed_path.exists())

        # Verify it actually contains the synthetic data
        df = pd.read_csv(processed_path)
        self.assertGreater(len(df), 0)
        self.assertIn("target", df.columns)

        # 6. Run lab train
        result = subprocess.run(
            [sys.executable, "-m", f"{package_name}.lab", "train"],
            cwd=output_dir,
            env=env,
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0, f"Lab train failed: {result.stdout}\n{result.stderr}")

        model_path = output_dir / "models/model.json"
        self.assertTrue(model_path.exists())

        # 7. Run lab evaluate
        result = subprocess.run(
            [sys.executable, "-m", f"{package_name}.lab", "evaluate"],
            cwd=output_dir,
            env=env,
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0, f"Lab evaluate failed: {result.stdout}\n{result.stderr}")
        self.assertTrue((output_dir / "reports/evaluation-report.md").exists())

    def test_synthetic_manual_handoff_instructions(self):
        """Verify that manual instructions are correctly printed when auto-activation is off."""
        package_name = "manual_pkg"
        output_dir = self.test_dir / "manual_project"

        run_generator(
            project_name="Manual Project",
            package_name=package_name,
            output_dir=output_dir,
            task="2",
            experience_mode="1",
            optional_profile="2"
        )

        env = os.environ.copy()
        env["PYTHONPATH"] = str(output_dir / "src")

        # Ensure activate_as_project_dataset is False (default)
        synth_config_path = output_dir / "configs/synthetic_data.json"
        with open(synth_config_path, "r") as f:
            synth_config = json.load(f)
        synth_config["activate_as_project_dataset"] = False
        synth_config["scenario"] = "timeseries"
        with open(synth_config_path, "w") as f:
            json.dump(synth_config, f)

        result = subprocess.run(
            [sys.executable, "-m", f"{package_name}.lab", "synthetic"],
            cwd=output_dir,
            env=env,
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("Manual configuration required:", result.stdout)
        self.assertIn("- Set 'data.raw_path' to 'data/synthetic/timeseries.csv'", result.stdout)
        self.assertIn("- Set 'target.column' to 'value'", result.stdout)
        self.assertIn(f"python -m {package_name}.lab data", result.stdout)
        self.assertIn(f"python -m {package_name}.lab train", result.stdout)
        self.assertIn(f"python -m {package_name}.lab evaluate", result.stdout)

if __name__ == "__main__":
    unittest.main()
