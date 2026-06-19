import unittest
import shutil
import tempfile
from pathlib import Path
from tests.helpers import run_generator

class TestOnboardingGuide(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.project_name = "onboarding_proj"
        self.package_name = "onboarding_pkg"

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_onboarding_guide_generation_en(self):
        output = run_generator(
            language="1", # English
            project_name=self.project_name,
            package_name=self.package_name,
            task="2", # supervised
            output_dir=self.test_dir
        )

        guide_path = self.test_dir / "START_HERE.md"
        self.assertTrue(guide_path.exists())

        content = guide_path.read_text()
        self.assertIn(f"# Welcome to {self.project_name}!", content)
        self.assertIn(f"- **Project Name**: {self.project_name}", content)
        self.assertIn("- **ML Task**: supervised", content)
        self.assertIn(f"- **Package Name**: `{self.package_name}`", content)
        self.assertIn("notebooks/01_eda.ipynb", content)

        # Verify concise terminal output
        self.assertIn("Open START_HERE.md in the created project.", output)
        self.assertIn(f"Start with EDA: notebooks/01_eda.ipynb or python -m {self.package_name}.lab eda", output)
        # Verify old long steps are NOT in output
        self.assertNotIn("Review and adjust metadata in", output)
        self.assertNotIn("Define your features in", output)

    def test_onboarding_guide_generation_pt_br(self):
        output = run_generator(
            language="2", # pt-BR
            project_name="projeto_legal",
            package_name="pacote_legal",
            task="2",
            output_dir=self.test_dir
        )

        guide_path = self.test_dir / "START_HERE.md"
        self.assertTrue(guide_path.exists())

        content = guide_path.read_text()
        self.assertIn("# Bem-vindo ao projeto_legal!", content)
        self.assertIn("notebooks/01_eda.ipynb", content)

        # Verify concise terminal output
        self.assertIn("Abra START_HERE.md no projeto criado.", output)
        self.assertIn("Comece pela EDA: notebooks/01_eda.ipynb ou python -m pacote_legal.lab eda", output)

    def test_onboarding_guide_without_docs(self):
        """Verify that START_HERE.md does not contain broken links when docs are disabled."""
        run_generator(
            project_name="no_docs_proj",
            package_name="no_docs_pkg",
            task="2",
            include_docs="n", # Disable docs
            output_dir=self.test_dir
        )

        guide_path = self.test_dir / "START_HERE.md"
        self.assertTrue(guide_path.exists())

        content = guide_path.read_text()
        self.assertNotIn("## 6. Documentation", content)
        self.assertNotIn("docs/data-dictionary.md", content)
        self.assertNotIn("docs/learning-path.md", content)

    def test_onboarding_guide_with_docs(self):
        """Verify that START_HERE.md contains the Documentation section when docs are enabled."""
        run_generator(
            project_name="with_docs_proj",
            package_name="with_docs_pkg",
            task="2",
            include_docs="y", # Enable docs
            output_dir=self.test_dir,
            optional_profile="2" # Recommended (includes advisor)
        )

        guide_path = self.test_dir / "START_HERE.md"
        self.assertTrue(guide_path.exists())

        content = guide_path.read_text()
        self.assertIn("## 6. Documentation", content)
        self.assertIn("docs/data-dictionary.md", content)
        self.assertIn("docs/learning-path.md", content)
        self.assertIn("- **Advisor**:", content) # Should also have advisor

if __name__ == "__main__":
    unittest.main()
