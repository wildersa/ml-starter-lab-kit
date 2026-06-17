import unittest
import shutil
import tempfile
from pathlib import Path
from tests.helpers import run_generator

class TestNavigationRefresh(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_bandit_navigation_present_in_bandit_project(self):
        # Verify Bandit-specific navigation in README.md for a bandit task
        # Task "6" is bandit
        run_generator(
            project_name="bandit_proj",
            task="6",
            optional_profile="3", # full profile includes labs
            output_dir=self.test_dir
        )
        readme_content = (self.test_dir / "README.md").read_text()
        self.assertIn("## Educational Labs & Synthetic Data", readme_content)
        self.assertIn("Multi-Armed Bandit Lab", readme_content)
        self.assertIn("docs/bandit-walkthrough.md", readme_content)
        self.assertIn("docs/mab-lab.md", readme_content)
        self.assertIn("python -m bandit_proj.lab bandit", readme_content)

    def test_synthetic_navigation_present_when_enabled(self):
        # Verify Synthetic-specific navigation in README.md (using custom profile to enable it)
        optionals = ["n"] * 16
        optionals[14] = "y" # synthetic

        run_generator(
            project_name="synth_proj",
            task="2", # supervised
            optional_profile="4", # custom
            optionals=optionals,
            output_dir=self.test_dir
        )
        readme_content = (self.test_dir / "README.md").read_text()
        self.assertIn("## Educational Labs & Synthetic Data", readme_content)
        self.assertIn("Synthetic Data Lab", readme_content)
        self.assertIn("docs/synthetic-data-lab.md", readme_content)
        self.assertIn("python -m synth_proj.lab synthetic", readme_content)

    def test_dataset_advisor_present_in_minimal_with_advisor(self):
        # Verify Dataset Advisor is still present in minimal mode when explicitly enabled
        optionals = ["n"] * 16
        optionals[9] = "y" # advisor

        run_generator(
            project_name="advisor_proj",
            task="2", # supervised
            experience_mode="1", # minimal
            optional_profile="4", # custom
            optionals=optionals,
            output_dir=self.test_dir
        )
        readme_content = (self.test_dir / "README.md").read_text()
        self.assertIn("### 4. Run the Dataset Advisor", readme_content)
        self.assertIn("python -m advisor_proj.lab advisor", readme_content)

    def test_bandit_bridge_description_in_synthetic_docs(self):
        # Verify the bridge description in the generated synthetic-data-lab.md
        optionals = ["n"] * 16
        optionals[14] = "y" # synthetic

        run_generator(
            project_name="bridge_proj",
            task="2", # supervised
            optional_profile="4", # custom
            optionals=optionals,
            output_dir=self.test_dir
        )
        synth_doc_content = (self.test_dir / "docs/synthetic-data-lab.md").read_text()
        self.assertIn("Bridge to Bandit Lab", synth_doc_content)
        self.assertIn("logged data", synth_doc_content.lower())

        # PT-BR check
        shutil.rmtree(self.test_dir)
        self.test_dir = Path(tempfile.mkdtemp())
        run_generator(
            language="2", # Português
            project_name="bridge_proj_pt",
            task="2", # supervised
            optional_profile="4", # custom
            optionals=optionals,
            output_dir=self.test_dir
        )
        synth_doc_pt_content = (self.test_dir / "docs/synthetic-data-lab.pt-BR.md").read_text()
        self.assertIn("Ponte para o Bandit Lab", synth_doc_pt_content)
        self.assertIn("dados logados", synth_doc_pt_content.lower())

if __name__ == "__main__":
    unittest.main()
