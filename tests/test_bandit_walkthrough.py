import unittest
import shutil
import tempfile
import os
from pathlib import Path
from tests.helpers import run_generator

class TestBanditWalkthrough(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_walkthrough_generation_bandit_task(self):
        """P0.1: Bandit walkthrough generated for Bandit task."""
        project_name = "bandit_task"
        package_name = "bandit_task"
        # Task 6 is Bandit
        run_generator(
            project_name=project_name,
            experience_mode="2", # guided
            output_dir=self.test_dir,
            include_docs="y",
            include_ml_basics="y",
            task="6"
        )

        walkthrough_path = self.test_dir / "docs/bandit-walkthrough.md"
        self.assertTrue(walkthrough_path.exists())

        content = walkthrough_path.read_text()

        # P0.2: Walkthrough contains required concepts
        required_terms = [
            "Context", "Arm / Action", "Reward", "Policy",
            "Baseline", "Regret", "Lift", "Delayed Reward", "Drift"
        ]
        for term in required_terms:
            self.assertIn(term, content)

        # P0.3: Explicit warning about supervised target
        self.assertIn("CRITICAL WARNING", content)
        self.assertIn("supervised dataset as your Bandit reward", content)
        self.assertIn("Impressions/Events", content)
        self.assertIn("Actions", content)
        self.assertIn("Rewards", content)

        # P0.5: Workspace navigation exposes the walkthrough
        workspace_path = self.test_dir / f"src/{package_name}/learning_workspace.py"
        workspace_content = workspace_path.read_text()
        self.assertIn("bandit-walkthrough.md", workspace_content)
        self.assertIn("bandit_tabs = st.tabs", workspace_content)
        self.assertIn('"Walkthrough"', workspace_content)

        # Reference links to walkthrough
        mab_lab_path = self.test_dir / "docs/mab-lab.md"
        self.assertIn("bandit-walkthrough.md", mab_lab_path.read_text())

        readme_path = self.test_dir / "README.md"
        self.assertIn("docs/bandit-walkthrough.md", readme_path.read_text())

    def test_walkthrough_generation_pt_br(self):
        """Verify PT-BR generation."""
        project_name = "bandit_pt"
        package_name = "bandit_pt"
        # Task 6 is Bandit
        run_generator(
            project_name=project_name,
            experience_mode="2", # guided
            output_dir=self.test_dir,
            include_docs="y",
            include_ml_basics="y",
            task="6",
            language="2" # 2 is pt-BR
        )

        walkthrough_path = self.test_dir / "docs/bandit-walkthrough.pt-BR.md"
        self.assertTrue(walkthrough_path.exists())

        content = walkthrough_path.read_text()
        self.assertIn("AVISO CRÍTICO", content)
        self.assertIn("Braço", content)

        workspace_path = self.test_dir / f"src/{package_name}/learning_workspace.py"
        workspace_content = workspace_path.read_text()
        self.assertIn("bandit-walkthrough.pt-BR.md", workspace_content)
        self.assertIn('"Guia de Início"', workspace_content)

    def test_no_walkthrough_for_non_bandit(self):
        """P0.4: Non-Bandit projects do not receive Bandit walkthrough."""
        project_name = "classic_ml"
        run_generator(
            project_name=project_name,
            experience_mode="2", # guided
            output_dir=self.test_dir,
            include_docs="y",
            include_ml_basics="y",
            task="1" # classification
        )

        walkthrough_path = self.test_dir / "docs/bandit-walkthrough.md"
        self.assertFalse(walkthrough_path.exists())

        readme_path = self.test_dir / "README.md"
        self.assertNotIn("bandit-walkthrough.md", readme_path.read_text())

if __name__ == "__main__":
    unittest.main()
