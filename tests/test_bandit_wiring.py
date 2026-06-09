import unittest
from pathlib import Path
import shutil
import tempfile
import os
import sys
import subprocess
from tests.helpers import run_generator

class TestBanditWiring(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.starter_root = self.test_dir / "ml-starter-lab-kit"
        self.starter_root.mkdir()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_bandit_lab_generated_in_guided_mode(self):
        """P0.1: Guided project contains bandit_lab.py and configs/bandit_config.json."""
        package_name = "bandit_guided_pkg"
        output_dir = self.test_dir / "bandit_guided_project"

        run_generator(
            project_name="Bandit Guided Project",
            package_name=package_name,
            output_dir=output_dir,
            experience_mode="2" # Guided Learning Mode
        )

        self.assertTrue((output_dir / f"src/{package_name}/bandit_lab.py").exists())
        self.assertTrue((output_dir / "configs/bandit_config.json").exists())

        # P0.5: Placeholder text check
        lab_content = (output_dir / f"src/{package_name}/bandit_lab.py").read_text()
        self.assertIn("Bandit Lab is planned but not implemented", lab_content)

        # P0.3: lab.py contains bandit command
        lab_py_content = (output_dir / f"src/{package_name}/lab.py").read_text()
        self.assertIn('subparsers.add_parser("bandit"', lab_py_content)
        self.assertIn('elif args.command == "bandit":', lab_py_content)
        self.assertIn('run_bandit()', lab_py_content)

        # P0.4: README contains the command
        readme_content = (output_dir / "README.md").read_text()
        self.assertIn(f"python -m {package_name}.lab bandit", readme_content)

    def test_bandit_lab_omitted_in_minimal_mode(self):
        """P0.2: Minimal project does not contain Bandit Lab files or README commands."""
        package_name = "bandit_minimal_pkg"
        output_dir = self.test_dir / "bandit_minimal_project"

        run_generator(
            project_name="Bandit Minimal Project",
            package_name=package_name,
            output_dir=output_dir,
            experience_mode="1" # Minimal Starter
        )

        self.assertFalse((output_dir / f"src/{package_name}/bandit_lab.py").exists())
        self.assertFalse((output_dir / "configs/bandit_config.json").exists())

        # README should NOT contain the command
        readme_content = (output_dir / "README.md").read_text()
        self.assertNotIn(f"python -m {package_name}.lab bandit", readme_content)

    def test_bandit_lab_custom_option(self):
        """Verify Bandit Lab can be enabled via custom profile."""
        package_name = "bandit_custom_pkg"
        output_dir = self.test_dir / "bandit_custom_project"

        # Option sequence for custom profile:
        # eda, preprocessing, metrics, optimization, feature_measurement,
        # visualization, notebook_factory, model_report, experiment_log,
        # advisor, learning, baseline_lab, bandit_lab
        # Total 13 options now.
        optionals = ["n"] * 12 + ["y"]

        run_generator(
            project_name="Bandit Custom Project",
            package_name=package_name,
            output_dir=output_dir,
            experience_mode="1",
            optional_profile="4", # Custom
            optionals=optionals
        )

        self.assertTrue((output_dir / f"src/{package_name}/bandit_lab.py").exists())
        self.assertTrue((output_dir / "configs/bandit_config.json").exists())

    def test_bandit_command_execution_placeholder(self):
        """Verify the bandit command runs the placeholder."""
        package_name = "bandit_run_pkg"
        output_dir = self.test_dir / "bandit_run_project"

        run_generator(
            project_name="Bandit Run Project",
            package_name=package_name,
            output_dir=output_dir,
            experience_mode="2"
        )

        env = os.environ.copy()
        env["PYTHONPATH"] = str(output_dir / "src")
        result = subprocess.run(
            [sys.executable, "-m", f"{package_name}.lab", "bandit"],
            cwd=output_dir,
            env=env,
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("Bandit Lab is planned but not implemented", result.stdout)

if __name__ == "__main__":
    unittest.main()
