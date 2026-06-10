import unittest
from pathlib import Path
import shutil
import tempfile
import os
from tests.helpers import run_generator

class TestBanditGating(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_guided_supervised_no_bandit_by_default(self):
        """P0.1: Guided supervised projects do NOT include Bandit Lab by default."""
        package_name = "guided_supervised_pkg"
        output_dir = self.test_dir / "guided_supervised"

        run_generator(
            project_name="Guided Supervised",
            package_name=package_name,
            output_dir=output_dir,
            task="2", # supervised
            experience_mode="2", # guided
            optional_profile="2" # recommended
        )

        bandit_lab_path = output_dir / f"src/{package_name}/bandit_lab.py"
        self.assertFalse(bandit_lab_path.exists(), "Bandit Lab should not be generated for supervised task by default.")

        readme_content = (output_dir / "README.md").read_text()
        self.assertNotIn("lab bandit", readme_content)
        self.assertNotIn("Multi-Armed Bandit Lab", readme_content)

    def test_guided_bandit_task_includes_bandit(self):
        """P0.3: Bandit-task projects include Bandit Lab even in Guided mode."""
        package_name = "guided_bandit_pkg"
        output_dir = self.test_dir / "guided_bandit"

        run_generator(
            project_name="Guided Bandit",
            package_name=package_name,
            output_dir=output_dir,
            task="6", # bandit
            experience_mode="2", # guided
            optional_profile="2" # recommended
        )

        bandit_lab_path = output_dir / f"src/{package_name}/bandit_lab.py"
        self.assertTrue(bandit_lab_path.exists(), "Bandit Lab should be generated for bandit task.")

        readme_content = (output_dir / "README.md").read_text()
        self.assertIn("lab bandit", readme_content)
        self.assertIn("Multi-Armed Bandit Lab", readme_content)

    def test_guided_supervised_with_full_profile_includes_bandit(self):
        """P0.2: Guided supervised projects include Bandit Lab if 'full' profile is selected."""
        package_name = "guided_full_pkg"
        output_dir = self.test_dir / "guided_full"

        run_generator(
            project_name="Guided Full",
            package_name=package_name,
            output_dir=output_dir,
            task="2", # supervised
            experience_mode="2", # guided
            optional_profile="3" # full
        )

        bandit_lab_path = output_dir / f"src/{package_name}/bandit_lab.py"
        self.assertTrue(bandit_lab_path.exists(), "Bandit Lab should be generated when 'full' profile is selected.")

    def test_guided_supervised_custom_bandit_includes_bandit(self):
        """P0.2: Explicit Bandit Lab selection still sets/generates the feature."""
        package_name = "guided_custom_bandit_pkg"
        output_dir = self.test_dir / "guided_custom_bandit"

        # custom optionals: eda, preproc, metrics, opt, feat, viz, nb, rep, exp, advisor, learn, baseline, bandit
        optionals = ["n"] * 12 + ["y"]

        run_generator(
            project_name="Guided Custom Bandit",
            package_name=package_name,
            output_dir=output_dir,
            task="2",
            experience_mode="2",
            optional_profile="4", # custom
            optionals=optionals
        )

        bandit_lab_path = output_dir / f"src/{package_name}/bandit_lab.py"
        self.assertTrue(bandit_lab_path.exists(), "Bandit Lab should be generated when explicitly selected in custom profile.")

if __name__ == "__main__":
    unittest.main()
