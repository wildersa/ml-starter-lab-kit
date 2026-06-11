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
            problem_priority="1" # interpretability (NOT learning)
        )

        bandit_lab_path = output_dir / f"src/{package_name}/bandit_lab.py"
        self.assertFalse(bandit_lab_path.exists(), "Bandit Lab should not be generated for supervised task by default.")

        readme_content = (output_dir / "README.md").read_text()
        self.assertNotIn("lab bandit", readme_content)
        self.assertNotIn("Multi-Armed Bandit Lab", readme_content)

    def test_guided_regression_no_bandit(self):
        """P0.1: Guided regression projects do NOT include Bandit Lab by default."""
        package_name = "guided_reg_pkg"
        output_dir = self.test_dir / "guided_reg"

        run_generator(
            project_name="Guided Regression",
            package_name=package_name,
            output_dir=output_dir,
            task="2", # supervised
            experience_mode="2", # guided
            problem_goal="2", # predict a number (regression)
            problem_priority="2" # performance
        )

        bandit_lab_path = output_dir / f"src/{package_name}/bandit_lab.py"
        self.assertFalse(bandit_lab_path.exists())

    def test_guided_timeseries_no_bandit(self):
        """P0.1: Guided time-series projects do NOT include Bandit Lab by default."""
        package_name = "guided_ts_pkg"
        output_dir = self.test_dir / "guided_ts"

        run_generator(
            project_name="Guided Time Series",
            package_name=package_name,
            output_dir=output_dir,
            task="4", # timeseries
            experience_mode="2", # guided
            problem_priority="2" # performance
        )

        bandit_lab_path = output_dir / f"src/{package_name}/bandit_lab.py"
        self.assertFalse(bandit_lab_path.exists())

    def test_cli_summary_hides_bandit_when_absent(self):
        """P0.4: CLI summary (terminal output) does not mention bandit if not generated."""
        package_name = "no_bandit_summary_pkg"
        output_dir = self.test_dir / "no_bandit_summary"

        output = run_generator(
            project_name="No Bandit Summary",
            package_name=package_name,
            output_dir=output_dir,
            task="2",
            experience_mode="2",
            problem_priority="1"
        )

        # The output of run_generator is the captured stdout
        self.assertNotIn("lab bandit", output)
        self.assertNotIn("Bandit Lab", output)

    def test_guided_learning_priority_includes_bandit(self):
        """Guided projects with 'learning' priority include Bandit Lab (P1-D logic)."""
        package_name = "guided_learning_pkg"
        output_dir = self.test_dir / "guided_learning"

        run_generator(
            project_name="Guided Learning",
            package_name=package_name,
            output_dir=output_dir,
            task="2", # supervised
            experience_mode="2", # guided
            problem_priority="5" # learning/experimentation
        )

        bandit_lab_path = output_dir / f"src/{package_name}/bandit_lab.py"
        self.assertTrue(bandit_lab_path.exists(), "Bandit Lab should be generated for 'learning' priority in Guided mode.")

        readme_content = (output_dir / "README.md").read_text()
        self.assertIn("lab bandit", readme_content)
        self.assertIn("Multi-Armed Bandit Lab", readme_content)

    def test_minimal_supervised_full_profile_includes_bandit(self):
        """P0.2: Explicit Bandit Lab selection (via full profile) still sets/generates the feature."""
        package_name = "minimal_full_pkg"
        output_dir = self.test_dir / "minimal_full"

        run_generator(
            project_name="Minimal Full",
            package_name=package_name,
            output_dir=output_dir,
            task="2", # supervised
            experience_mode="1", # minimal
            optional_profile="3" # full
        )

        bandit_lab_path = output_dir / f"src/{package_name}/bandit_lab.py"
        self.assertTrue(bandit_lab_path.exists(), "Bandit Lab should be generated when 'full' profile is selected.")

    def test_minimal_supervised_custom_bandit_includes_bandit(self):
        """P0.2: Explicit Bandit Lab selection still sets/generates the feature."""
        package_name = "minimal_custom_bandit_pkg"
        output_dir = self.test_dir / "minimal_custom_bandit"

        # custom optionals: eda, preproc, metrics, opt, feat, viz, nb, rep, exp, advisor, learn, baseline, bandit
        optionals = ["n"] * 12 + ["y"]

        run_generator(
            project_name="Minimal Custom Bandit",
            package_name=package_name,
            output_dir=output_dir,
            task="2",
            experience_mode="1",
            optional_profile="4", # custom
            optionals=optionals
        )

        bandit_lab_path = output_dir / f"src/{package_name}/bandit_lab.py"
        self.assertTrue(bandit_lab_path.exists(), "Bandit Lab should be generated when explicitly selected in custom profile.")

if __name__ == "__main__":
    unittest.main()
