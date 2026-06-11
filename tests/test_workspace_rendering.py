import unittest
import shutil
import tempfile
import os
from pathlib import Path
from unittest.mock import MagicMock, patch
from tests.helpers import run_generator
from ml_starter_generator.templates import load_template

class TestWorkspaceRendering(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_doc_generation(self):
        """P0.1, P0.6: Ensure docs are generated in the project."""
        project_name = "test_docs_proj"
        package_name = "test_docs_pkg"
        run_generator(
            project_name=project_name,
            experience_mode="guided",
            output_dir=self.test_dir,
            task="supervised"
        )

        expected_docs = [
            "docs/evaluation.md",
            "docs/monitoring.md",
            "docs/data-dictionary.md",
        ]
        for doc in expected_docs:
            self.assertTrue((self.test_dir / doc).exists(), f"Missing {doc}")

    def test_pt_br_doc_generation(self):
        """P0.1: Ensure PT-BR docs are generated when language is PT-BR."""
        project_name = "test_docs_pt"
        run_generator(
            language="2", # PT-BR
            project_name=project_name,
            experience_mode="guided",
            output_dir=self.test_dir,
            task="supervised"
        )

        expected_docs = [
            "docs/evaluation.pt-BR.md",
            "docs/monitoring.pt-BR.md",
        ]
        for doc in expected_docs:
            self.assertTrue((self.test_dir / doc).exists(), f"Missing {doc}")

    def test_bandit_doc_generation(self):
        """P0.1: Ensure Bandit doc is generated only when bandit is enabled."""
        # 1. Enabled
        run_generator(
            project_name="with_bandit",
            experience_mode="guided",
            output_dir=self.test_dir / "with_bandit",
            task="6" # bandit
        )
        self.assertTrue((self.test_dir / "with_bandit/docs/mab-lab.md").exists())

        # 2. Disabled
        run_generator(
            project_name="no_bandit",
            experience_mode="minimal",
            output_dir=self.test_dir / "no_bandit",
            task="supervised",
            optional_profile="1" # minimal
        )
        self.assertFalse((self.test_dir / "no_bandit/docs/mab-lab.md").exists())

    def test_workspace_allowlist_logic(self):
        """P0.4: Verify allowlist enforcement in the template logic."""
        # We can't easily run the Streamlit app, but we can verify the template content
        # or mock the render_project_doc function if we were testing the rendered code.
        # Instead, let's verify the template contains the expected allowlist.
        values = {
            "PROJECT_NAME": "Test Project",
            "PACKAGE_NAME": "test_pkg",
            "GENERATE_BANDIT": "true",
            "LANGUAGE": "en"
        }
        content = load_template("learning_workspace.py", values)

        self.assertIn('"docs/evaluation.md"', content)
        self.assertIn('"reports/evaluation-report.md"', content)
        self.assertIn("if relative_path not in allowed_paths:", content)
        self.assertIn("st.error(f\"Access denied:", content)

    def test_evaluation_report_generation(self):
        """P0.2: Verify evaluate.py generates the markdown report."""
        project_name = "eval_test"
        package_name = "eval_test"
        run_generator(
            project_name=project_name,
            experience_mode="guided",
            output_dir=self.test_dir,
            task="supervised",
            include_demo="y"
        )

        # We need to simulate running evaluate.py
        # But first we need to run data processing and training to have the model

        pkg_path = self.test_dir / "src" / package_name

        # Mock some files to make evaluate.py work
        (self.test_dir / "models").mkdir(exist_ok=True)
        (self.test_dir / "models/model.json").write_text('{"target_column": "target", "prediction": "0", "model_type": "majority_class_baseline"}')

        (self.test_dir / "data/processed").mkdir(parents=True, exist_ok=True)
        (self.test_dir / "data/processed/dataset.csv").write_text("col1,target\n1,0\n2,0")

        # Update config to point to the processed path
        config_path = self.test_dir / "configs/config.json"
        import json
        config = json.loads(config_path.read_text())
        config["data"]["processed_path"] = "data/processed/dataset.csv"
        config_path.write_text(json.dumps(config))

        # Run evaluate.py
        import sys
        sys.path.append(str(self.test_dir / "src"))

        # Use subprocess to avoid side effects in the test process
        import subprocess
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.test_dir / "src")
        result = subprocess.run(
            [sys.executable, "-m", f"{package_name}.evaluate"],
            cwd=self.test_dir,
            env=env,
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.test_dir / "reports/evaluation-report.md").exists())
        report_content = (self.test_dir / "reports/evaluation-report.md").read_text()
        self.assertIn("# Evaluation Report", report_content)
        self.assertIn("majority_class_baseline", report_content)

if __name__ == "__main__":
    unittest.main()
