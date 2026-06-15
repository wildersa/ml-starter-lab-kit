import unittest
from pathlib import Path
import shutil
import tempfile
import os
import sys
import subprocess
import json
from tests.helpers import run_generator

class TestGeneratedProjectFullGuidedFlow(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_full_guided_flow(self):
        """Verify the full guided flow: synthetic -> data -> train -> evaluate."""
        package_name = "guided_pkg"
        output_dir = self.test_dir / "guided_project"

        # 1. Run generator in Guided Learning Mode
        run_generator(
            project_name="Guided Project",
            package_name=package_name,
            output_dir=output_dir,
            task="2", # supervised
            experience_mode="2", # guided
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
        self.assertTrue((output_dir / "data/synthetic/classification.csv").exists())

        # 4. Run lab data
        result = subprocess.run(
            [sys.executable, "-m", f"{package_name}.lab", "data"],
            cwd=output_dir,
            env=env,
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0, f"Lab data failed: {result.stdout}\n{result.stderr}")
        self.assertTrue((output_dir / "data/processed/modeling_table.csv").exists())

        # 5. Run lab train
        result = subprocess.run(
            [sys.executable, "-m", f"{package_name}.lab", "train"],
            cwd=output_dir,
            env=env,
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0, f"Lab train failed: {result.stdout}\n{result.stderr}")
        self.assertTrue((output_dir / "models/model.json").exists())

        # 6. Run lab evaluate
        result = subprocess.run(
            [sys.executable, "-m", f"{package_name}.lab", "evaluate"],
            cwd=output_dir,
            env=env,
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0, f"Lab evaluate failed: {result.stdout}\n{result.stderr}")
        self.assertTrue((output_dir / "reports/evaluation-report.md").exists())
        self.assertTrue((output_dir / "reports/metrics.json").exists())

if __name__ == "__main__":
    unittest.main()
