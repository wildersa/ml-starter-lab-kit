import unittest
import shutil
import tempfile
from pathlib import Path
from tests.helpers import run_generator

class TestOnboardingPolish(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_minimal_onboarding_concise(self):
        """P0.1 - Minimal Starter onboarding is concise and doesn't push Streamlit."""
        output = run_generator(
            project_name="min_proj",
            package_name="min_pkg",
            output_dir=self.test_dir,
            experience_mode="1"  # minimal
        )

        # Check terminal summary - should point to START_HERE.md
        next_steps = output.split("[Next steps]")[1]
        self.assertIn("START_HERE.md", next_steps)
        self.assertNotIn("workspace", next_steps.lower())
        self.assertNotIn("streamlit", next_steps.lower())

        # Check README
        readme_path = self.test_dir / "README.md"
        content = readme_path.read_text()
        self.assertNotIn("Interactive Learning Workspace", content)
        self.assertNotIn("python -m min_pkg.lab workspace", content)
        self.assertNotIn("python -m min_pkg.lab eda", content)
        self.assertNotIn("python -m min_pkg.lab advisor", content)
        self.assertNotIn("python -m min_pkg.lab learn", content)
        self.assertNotIn("python -m min_pkg.lab baseline", content)

    def test_guided_visual_first_onboarding(self):
        """P0.2 - Guided Learning onboarding makes START_HERE.md the main entry point."""
        output = run_generator(
            project_name="gui_proj",
            package_name="gui_pkg",
            output_dir=self.test_dir,
            experience_mode="2"  # guided
        )

        # Check terminal summary
        next_steps = output.split("[Next steps]")[1]
        self.assertIn("START_HERE.md", next_steps)

        # Check README
        readme_path = self.test_dir / "README.md"
        content = readme_path.read_text()
        self.assertIn("## Interactive Learning Workspace (Recommended)", content)
        self.assertIn("python -m gui_pkg.lab workspace", content)

    def test_eda_first_rule_documented(self):
        """P0.3 - Onboarding guide explains the EDA-first rule."""
        run_generator(
            project_name="eda_rule_proj",
            package_name="eda_rule_pkg",
            output_dir=self.test_dir,
            experience_mode="2"  # guided
        )

        # Check START_HERE.md
        guide_path = self.test_dir / "START_HERE.md"
        content = guide_path.read_text()
        self.assertIn("do not skip", content.lower())

        # Check README
        readme_path = self.test_dir / "README.md"
        content = readme_path.read_text()
        self.assertIn("IMPORTANT**: You must run the **Exploratory Data Analysis (EDA)** step", content)

    def test_cli_alternatives_documented(self):
        """P0.4 - CLI alternatives are documented for Guided Learning."""
        run_generator(
            project_name="cli_alt_proj",
            package_name="cli_alt_pkg",
            output_dir=self.test_dir,
            experience_mode="2"  # guided
        )

        readme_path = self.test_dir / "README.md"
        content = readme_path.read_text()
        self.assertIn("**CLI Alternatives:**", content)
        self.assertIn("python -m cli_alt_pkg.lab eda", content)
        self.assertIn("python -m cli_alt_pkg.lab advisor", content)
        self.assertIn("python -m cli_alt_pkg.lab learn", content)
        self.assertIn("python -m cli_alt_pkg.lab baseline", content)

    def test_commands_use_package_name(self):
        """P0.5 - Commands use the correct package name and not src/ layout prefix."""
        package_name = "custom_pkg_name"
        run_generator(
            project_name="Pkg Name Proj",
            package_name=package_name,
            output_dir=self.test_dir,
            experience_mode="2"
        )

        readme_path = self.test_dir / "README.md"
        content = readme_path.read_text()

        self.assertIn(f"python -m {package_name}.lab check", content)
        self.assertIn(f"python -m {package_name}.lab workspace", content)
        self.assertNotIn(f"python -m src.{package_name}.lab", content)

if __name__ == "__main__":
    unittest.main()
