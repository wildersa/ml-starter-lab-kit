import unittest
import shutil
import tempfile
from pathlib import Path
import json
import subprocess
import os
import sys

from tests.helpers import run_generator

class TestInvoiceAgentGeneration(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.project_name = "invoice_agent_project"
        self.package_name = "invoice_agent_project"

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_generate_invoice_agent_lab(self):
        # Task "7" is invoice_agent
        run_generator(
            project_name=self.project_name,
            task="7",
            output_dir=self.test_dir,
            optional_profile="1" # minimal
        )

        pkg_path = self.test_dir / "src" / self.package_name

        # Verify directories
        self.assertTrue((self.test_dir / "contracts").exists())
        self.assertTrue((self.test_dir / "data/samples/invoices").exists())

        # Verify files
        self.assertTrue((pkg_path / "invoice_pipeline.py").exists())
        self.assertTrue((pkg_path / "invoice_rules.py").exists())
        self.assertTrue((pkg_path / "invoice_agent_tools.py").exists())
        self.assertTrue((pkg_path / "erp_output.py").exists())
        self.assertTrue((self.test_dir / "configs/invoice_agent_config.json").exists())
        self.assertTrue((self.test_dir / "contracts/invoice-extraction.schema.json").exists())
        self.assertTrue((self.test_dir / "data/samples/invoices/sample_invoice.json").exists())
        self.assertTrue((self.test_dir / "docs/invoice-agent-lab.md").exists())

        # Verify lab.py wiring
        lab_path = pkg_path / "lab.py"
        with open(lab_path) as f:
            content = f.read()
            self.assertIn("invoice-agent", content)
            self.assertIn("run_invoice_agent", content)

    def test_invoice_agent_demo_run(self):
        run_generator(
            project_name=self.project_name,
            task="7",
            output_dir=self.test_dir,
            optional_profile="1"
        )

        # We need to be able to import the generated package.
        # We'll run it as a subprocess with PYTHONPATH set to the src directory.
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.test_dir / "src")

        cmd = [
            sys.executable, "-m", f"{self.package_name}.lab", "invoice-agent", "demo"
        ]

        result = subprocess.run(
            cmd,
            env=env,
            capture_output=True,
            text=True,
            cwd=self.test_dir
        )

        print(result.stdout)
        print(result.stderr)

        self.assertEqual(result.returncode, 0)
        self.assertIn("Loading invoice extraction: sample_invoice.json", result.stdout)
        self.assertIn("Running deterministic validation rules...", result.stdout)
        self.assertIn("Running agent-assisted reconciliation simulation...", result.stdout)
        self.assertIn("Generating ERP output draft...", result.stdout)

        # Verify artifacts
        reports_dir = self.test_dir / "reports"
        self.assertTrue((reports_dir / "invoice-validation-result-sample-001.json").exists())
        self.assertTrue((reports_dir / "invoice-agent-dossier-sample-001.md").exists())
        self.assertTrue((reports_dir / "erp-output-draft-sample-001.json").exists())

if __name__ == "__main__":
    unittest.main()
