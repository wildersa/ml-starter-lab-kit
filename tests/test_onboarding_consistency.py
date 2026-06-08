import unittest
from pathlib import Path
import os
import shutil
import tempfile
from tests.helpers import run_generator

class TestOnboardingConsistency(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_cli_summary_output_consistency(self):
        """P0.2 & P0.3 - Verify CLI summary doesn't use python -m src."""
        output = run_generator(
            project_name="consistency_proj",
            package_name="consistency_pkg",
            task="1",
            output_dir=self.test_dir,
            include_pyproject="n"
        )

        # Should contain the correct commands
        self.assertIn("python -m consistency_pkg.lab check", output)
        self.assertIn("python -m consistency_pkg.lab train", output)
        self.assertIn("python -m consistency_pkg.lab evaluate", output)

        # Should NOT contain the old src. prefix
        self.assertNotIn("python -m src.consistency_pkg.data", output)

    def test_root_readme_clone_urls(self):
        """P0.1 & P0.4 - Verify root READMEs use the correct clone URL."""
        root_dir = Path(__file__).parent.parent
        readmes = ["README.md", "README.pt-BR.md"]

        correct_url = "https://github.com/wildersa/ml-starter-lab-kit.git"
        old_url = "https://github.com/lucasoliveira/ml-starter-lab-kit.git"

        for readme_name in readmes:
            readme_path = root_dir / readme_name
            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn(correct_url, content, f"{readme_name} should contain the correct clone URL")
                self.assertNotIn(old_url, content, f"{readme_name} should NOT contain the old clone URL")

    def test_no_stale_command_prefixes_in_codebase(self):
        """P0.3 - Search codebase for 'python -m src.' to ensure no stale occurrences."""
        root_dir = Path(__file__).parent.parent
        stale_pattern = "python -m src."

        # We search in .py and .md files, excluding the tests directory themselves if they are testing this
        for root, _, files in os.walk(root_dir):
            if "tests" in root or ".git" in root or "examples" in root:
                continue
            for file in files:
                if file.endswith((".py", ".md", ".tpl")):
                    file_path = Path(root) / file
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        self.assertNotIn(stale_pattern, content, f"Stale pattern '{stale_pattern}' found in {file_path}")

if __name__ == "__main__":
    unittest.main()
