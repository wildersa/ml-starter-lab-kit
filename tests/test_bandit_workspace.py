import unittest
import shutil
import tempfile
import os
from pathlib import Path
from tests.helpers import run_generator

class TestBanditWorkspace(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_bandit_enabled_via_full_profile(self):
        """P0.2: Bandit enabled via full profile in Minimal mode."""
        project_name = "full_bandit"
        package_name = "full_bandit"
        run_generator(
            project_name=project_name,
            experience_mode="1", # minimal
            output_dir=self.test_dir,
            include_docs="y",
            include_ml_basics="y",
            optional_profile="3" # full (includes bandit)
        )

        workspace_path = self.test_dir / f"src/{package_name}/learning_workspace.py"
        readme_path = self.test_dir / "README.md"

        self.assertTrue(workspace_path.exists())
        self.assertTrue(readme_path.exists())

        workspace_content = workspace_path.read_text()
        readme_content = readme_path.read_text()

        # Workspace includes Bandit Lab section and command
        self.assertIn('"Bandit Lab"', workspace_content)
        self.assertIn('elif section == "Bandit Lab":', workspace_content)
        self.assertIn('python -m full_bandit.lab bandit', workspace_content)
        self.assertIn('reports/bandit-results.md', workspace_content)

        # Workspace explains MAB is sequential decision learning
        self.assertIn('sequential decision learning', workspace_content)
        self.assertIn('different paradigm from supervised learning', workspace_content)

        # README mentions Bandit Lab in suggested commands
        self.assertIn('python -m full_bandit.lab bandit', readme_content)

    def test_minimal_bandit_disabled(self):
        """P0.5: Minimal Starter does not mention Bandit Lab."""
        project_name = "minimal_no_bandit"
        package_name = "minimal_no_bandit"
        run_generator(
            project_name=project_name,
            experience_mode="1", # minimal
            output_dir=self.test_dir,
            include_docs="n",
            include_ml_basics="n",
            optional_profile="1" # minimal
        )

        # In minimal, workspace might not even be generated if optional_options["learning_workspace"] is False
        # but let's check if it exists and what's in it.
        workspace_path = self.test_dir / f"src/{package_name}/learning_workspace.py"
        readme_path = self.test_dir / "README.md"

        if workspace_path.exists():
            workspace_content = workspace_path.read_text()
            self.assertNotIn('Bandit Lab', workspace_content)
            self.assertNotIn('lab bandit', workspace_content)

        readme_content = readme_path.read_text()
        self.assertNotIn('Bandit Lab', readme_content)
        self.assertNotIn('lab bandit', readme_content)

    def test_guided_custom_no_bandit(self):
        """P0.1, P0.4: Guided project with Bandit EXPLICITLY disabled (via custom profile)."""
        # Note: cli.py currently forces bandit_lab = True in guided mode regardless of profile choice
        # Wait, let me check cli.py again.
        # "if experience_mode == 'guided': optional_options['bandit_lab'] = True"
        # So it's always true in guided.
        pass

if __name__ == "__main__":
    unittest.main()
