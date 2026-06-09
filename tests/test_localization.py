import unittest
import shutil
import tempfile
import json
import os
import subprocess
import sys
from pathlib import Path
from tests.helpers import run_generator

class TestLocalization(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.project_name = "local_proj"
        self.package_name = "local_pkg"

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_english_default_output(self):
        output = run_generator(
            language="1", # English
            project_name=self.project_name,
            package_name=self.package_name,
            output_dir=self.test_dir,
            optional_profile="4", # custom
            optionals=["y"] + ["n"] * 8 + ["y", "n", "n", "n"] # eda and advisor
        )

        # CLI Output
        self.assertIn("Project basics", output)
        self.assertIn("Starter-kit created successfully!", output)

        # README
        readme_path = self.test_dir / "README.md"
        content = readme_path.read_text(encoding="utf-8")
        self.assertIn("This is a generated Machine Learning project", content)
        self.assertIn("## Structure", content)

        # Metadata
        profile_path = self.test_dir / "configs/problem_profile.json"
        with open(profile_path) as f:
            profile = json.load(f)
            self.assertEqual(profile["language"], "en")

        # Advisor Report
        # First we need to create dummy data to run advisor
        data_dir = self.test_dir / "data/raw"
        data_dir.mkdir(parents=True, exist_ok=True)
        (data_dir / "dataset.csv").write_text("col1,target\n1,0\n2,1\n")

        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.test_dir / "src")

        try:
            import pandas
            import numpy
            import sklearn

            # P0.1: Must run EDA first
            subprocess.run(
                [sys.executable, "-m", f"{self.package_name}.eda"],
                cwd=self.test_dir,
                env=env,
                check=True
            )

            # We need to make sure we have pandas and numpy to run advisor,
            # but the environment should already have them if they are in the current sys.path
            result = subprocess.run(
                [sys.executable, "-m", f"{self.package_name}.advisor"],
                cwd=self.test_dir,
                env=env,
                capture_output=True,
                text=True
            )
            self.assertEqual(result.returncode, 0, msg=f"Advisor failed: {result.stderr}")

            report_path = self.test_dir / "reports/dataset-advice.md"
            report_content = report_path.read_text(encoding="utf-8")
            self.assertIn("# Dataset Advisor Report", report_content)
            self.assertIn("What I found", report_content)
        except ImportError:
            # If ML deps are missing, we can still verify at least that the template was generated with localized markers
            advisor_path = self.test_dir / f"src/{self.package_name}/advisor.py"
            content = advisor_path.read_text(encoding="utf-8")
            self.assertIn('"report_title": "Dataset Advisor Report"', content)

    def test_portuguese_output(self):
        output = run_generator(
            language="2", # pt-BR
            project_name=self.project_name,
            package_name=self.package_name,
            output_dir=self.test_dir,
            optional_profile="4", # custom
            optionals=["y"] + ["n"] * 8 + ["y", "n", "n", "n"] # eda and advisor
        )

        # CLI Output
        self.assertIn("Informações básicas", output)
        self.assertIn("Starter-kit criado com sucesso!", output)

        # README
        readme_path = self.test_dir / "README.md"
        content = readme_path.read_text(encoding="utf-8")
        self.assertIn("Este é um projeto de Machine Learning gerado", content)
        self.assertIn("## Estrutura", content)

        # Metadata
        profile_path = self.test_dir / "configs/problem_profile.json"
        with open(profile_path) as f:
            profile = json.load(f)
            self.assertEqual(profile["language"], "pt-BR")

        # Advisor Report
        data_dir = self.test_dir / "data/raw"
        data_dir.mkdir(parents=True, exist_ok=True)
        (data_dir / "dataset.csv").write_text("col1,target\n1,0\n2,1\n")

        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.test_dir / "src")

        try:
            import pandas
            import numpy
            import sklearn

            # P0.1: Must run EDA first
            subprocess.run(
                [sys.executable, "-m", f"{self.package_name}.eda"],
                cwd=self.test_dir,
                env=env,
                check=True
            )

            result = subprocess.run(
                [sys.executable, "-m", f"{self.package_name}.advisor"],
                cwd=self.test_dir,
                env=env,
                capture_output=True,
                text=True
            )
            self.assertEqual(result.returncode, 0, msg=f"Advisor failed: {result.stderr}")

            report_path = self.test_dir / "reports/dataset-advice.md"
            report_content = report_path.read_text(encoding="utf-8")
            self.assertIn("# Relatório do Dataset Advisor", report_content)
            self.assertIn("O que eu encontrei", report_content)
        except ImportError:
            advisor_path = self.test_dir / f"src/{self.package_name}/advisor.py"
            content = advisor_path.read_text(encoding="utf-8")
            self.assertIn('"report_title": "Relatório do Dataset Advisor"', content)

    def test_technical_identifiers_remain_english_in_pt(self):
        run_generator(
            language="2", # pt-BR
            project_name=self.project_name,
            package_name="meu_pacote",
            output_dir=self.test_dir,
        )

        # Check folders
        self.assertTrue((self.test_dir / "src/meu_pacote").exists())
        self.assertTrue((self.test_dir / "configs").exists())
        self.assertTrue((self.test_dir / "data/raw").exists())

        # Check config keys
        config_path = self.test_dir / "configs/config.json"
        with open(config_path) as f:
            config = json.load(f)
            self.assertIn("project", config)
            self.assertIn("package", config["project"])
            self.assertEqual(config["project"]["package"], "meu_pacote")

        # Check README commands
        readme_content = (self.test_dir / "README.md").read_text()
        self.assertIn("python -m meu_pacote.lab check", readme_content)

if __name__ == "__main__":
    unittest.main()
