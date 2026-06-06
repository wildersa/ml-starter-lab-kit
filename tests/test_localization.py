import unittest
import shutil
import tempfile
from pathlib import Path
import json

from tests.helpers import run_generator

class TestLocalization(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_english_output(self):
        output = run_generator(
            project_name="en_proj",
            package_name="en_pkg",
            language="1",  # en
            output_dir=self.test_dir,
            optional_profile="2" # recommended (includes advisor)
        )

        # Check CLI output
        self.assertIn("ML Starter Kit Builder", output)
        self.assertIn("Starter-kit created.", output)
        self.assertIn("Next steps:", output)

        # Check README
        readme_path = self.test_dir / "README.md"
        self.assertTrue(readme_path.exists())
        readme_content = readme_path.read_text(encoding="utf-8")
        self.assertIn("This is a generated Machine Learning project", readme_content)
        self.assertIn("Suggested flow", readme_content)

        # Check Advisor Report (requires running it, but we can check the template code)
        advisor_path = self.test_dir / "src/en_pkg/advisor.py"
        self.assertTrue(advisor_path.exists())
        advisor_content = advisor_path.read_text(encoding="utf-8")
        self.assertIn('"report_title": "Dataset Advisor Report"', advisor_content)

        # Check problem_profile.json
        profile_path = self.test_dir / "configs/problem_profile.json"
        self.assertTrue(profile_path.exists())
        with open(profile_path) as f:
            profile = json.load(f)
            self.assertEqual(profile["language"], "en")

    def test_portuguese_output(self):
        output = run_generator(
            project_name="pt_proj",
            package_name="pt_pkg",
            language="2",  # pt-BR
            output_dir=self.test_dir,
            optional_profile="2"
        )

        # Check CLI output
        self.assertIn("ML Starter Kit Builder", output)
        self.assertIn("Starter-kit criado.", output)
        self.assertIn("Próximos passos:", output)

        # Check README
        readme_path = self.test_dir / "README.md"
        self.assertTrue(readme_path.exists())
        readme_content = readme_path.read_text(encoding="utf-8")
        self.assertIn("Este é um projeto de Machine Learning gerado", readme_content)
        self.assertIn("Fluxo sugerido", readme_content)

        # Check Advisor Report template
        advisor_path = self.test_dir / "src/pt_pkg/advisor.py"
        self.assertTrue(advisor_path.exists())
        advisor_content = advisor_path.read_text(encoding="utf-8")
        self.assertIn('"report_title": "Relatório do Dataset Advisor"', advisor_content)

        # Check problem_profile.json
        profile_path = self.test_dir / "configs/problem_profile.json"
        self.assertTrue(profile_path.exists())
        with open(profile_path) as f:
            profile = json.load(f)
            self.assertEqual(profile["language"], "pt-BR")

    def test_technical_identifiers_remain_english(self):
        # Even in Portuguese, technical parts must stay English
        run_generator(
            project_name="tech_proj",
            package_name="tech_pkg",
            language="2",
            output_dir=self.test_dir
        )

        # Folder and file names
        self.assertTrue((self.test_dir / "configs").exists())
        self.assertTrue((self.test_dir / "data/raw").exists())
        self.assertTrue((self.test_dir / "src/tech_pkg/train.py").exists())

        # Config keys
        with open(self.test_dir / "configs/config.json") as f:
            config = json.load(f)
            self.assertIn("project", config)
            self.assertIn("data", config)
            self.assertEqual(config["project"]["package"], "tech_pkg")

        # README commands
        readme_content = (self.test_dir / "README.md").read_text(encoding="utf-8")
        self.assertIn("python -m tech_pkg.data", readme_content)
        self.assertIn("python -m tech_pkg.train", readme_content)

if __name__ == "__main__":
    unittest.main()
