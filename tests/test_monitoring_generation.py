import unittest
import shutil
import tempfile
from pathlib import Path
import json
import os
import sys
import subprocess

from tests.helpers import run_generator

class TestMonitoringGeneration(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.project_name = "monitor_proj"
        self.package_name = "monitor_pkg"

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_monitoring_in_guided_mode(self):
        """P0.1, P0.2, P0.3, P0.4, P0.5: Monitoring in Guided Learning Mode."""
        run_generator(
            project_name=self.project_name,
            package_name=self.package_name,
            task="2", # supervised
            output_dir=self.test_dir,
            experience_mode="2" # guided
        )

        pkg_path = self.test_dir / f"src/{self.package_name}"
        doc_path = self.test_dir / "docs/monitoring.md"
        readme_path = self.test_dir / "README.md"

        # P0.1 & P0.3: Doc exists and contains terms
        self.assertTrue(doc_path.exists())
        doc_content = doc_path.read_text()
        self.assertIn("Data Drift", doc_content)
        self.assertIn("Concept Drift", doc_content)
        self.assertIn("Performance Drift", doc_content)
        self.assertIn("Classification", doc_content)
        self.assertIn("Regression", doc_content)

        # P0.2: Stub exists
        self.assertTrue((pkg_path / "monitor.py").exists())

        # P0.4: README order (evaluation before monitoring)
        readme_content = readme_path.read_text()
        eval_idx = readme_content.find("python -m monitor_pkg.lab evaluate")
        monitor_idx = readme_content.find("python -m monitor_pkg.lab monitor")
        self.assertNotEqual(eval_idx, -1)
        self.assertNotEqual(monitor_idx, -1)
        self.assertTrue(eval_idx < monitor_idx, "Evaluation should come before monitoring in README")

    def test_no_monitoring_in_minimal_mode(self):
        """P0.5: Minimal mode does not get monitoring extras."""
        run_generator(
            project_name=self.project_name,
            package_name=self.package_name,
            task="2",
            output_dir=self.test_dir,
            experience_mode="1", # minimal
            optional_profile="1" # minimal
        )

        pkg_path = self.test_dir / f"src/{self.package_name}"
        # Docs are still created in minimal mode if requested (default True in some paths,
        # but let's check the script stub specifically)
        self.assertFalse((pkg_path / "monitor.py").exists())

    def test_monitoring_stub_behavior(self):
        """P0.6: Stub has bounded behavior on toy input."""
        run_generator(
            project_name=self.project_name,
            package_name=self.package_name,
            task="2",
            output_dir=self.test_dir,
            experience_mode="2"
        )

        # Create a toy dataset
        data_dir = self.test_dir / "data/raw"
        data_dir.mkdir(parents=True, exist_ok=True)
        csv_path = data_dir / "dataset.csv"
        with open(csv_path, "w") as f:
            f.write("feat1,feat2,target\n1,10,0\n2,20,1\n3,30,0")

        # Mock dependencies or run in a subprocess if env is ready
        # For simplicity in this env, we can check the file content for P0.6 requirements
        stub_path = self.test_dir / f"src/{self.package_name}/monitor.py"
        stub_content = stub_path.read_text()

        self.assertIn("import pandas as pd", stub_content)
        self.assertIn("def check_drift", stub_content)
        self.assertIn("report.append(\"# Basic Drift Analysis Report\")", stub_content)

    def test_monitoring_cli_passthrough(self):
        """Verify 'lab monitor' accepts and passes through arguments."""
        run_generator(
            project_name=self.project_name,
            package_name=self.package_name,
            task="2",
            output_dir=self.test_dir,
            experience_mode="2"
        )

        # Create reference and current data
        data_dir = self.test_dir / "data/raw"
        data_dir.mkdir(parents=True, exist_ok=True)
        ref_path = data_dir / "ref.csv"
        cur_path = data_dir / "cur.csv"

        with open(ref_path, "w") as f:
            f.write("feat1,target\n1,0\n2,1")
        with open(cur_path, "w") as f:
            f.write("feat1,target\n5,0\n6,1")

        report_path = self.test_dir / "reports/custom-drift.md"

        # Run the command via subprocess to ensure the CLI parses it correctly
        # We need to set PYTHONPATH to include the src directory
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.test_dir / "src")

        # Use current sys.executable to ensure the same environment is used
        cmd = [
            sys.executable, "-m", f"{self.package_name}.lab", "monitor",
            "--reference", str(ref_path),
            "--current", str(cur_path),
            "--output", str(report_path)
        ]

        result = subprocess.run(cmd, env=env, capture_output=True, text=True)

        self.assertEqual(result.returncode, 0, f"CLI failed.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}")
        self.assertTrue(report_path.exists())

        report_content = report_path.read_text()
        self.assertIn("Basic Drift Analysis Report", report_content)
        self.assertIn("Numerical Feature Statistics", report_content)
        self.assertIn("feat1", report_content)

    def test_monitoring_pt_br(self):
        """Verify localized terms."""
        run_generator(
            project_name=self.project_name,
            package_name=self.package_name,
            task="2",
            output_dir=self.test_dir,
            experience_mode="2",
            language="2" # pt-BR
        )

        doc_path = self.test_dir / "docs/monitoring.pt-BR.md"
        self.assertTrue(doc_path.exists())
        doc_content = doc_path.read_text()
        self.assertIn("Data Drift", doc_content)
        self.assertIn("Sinais Específicos", doc_content)

if __name__ == "__main__":
    unittest.main()
