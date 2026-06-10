import unittest
import shutil
import tempfile
import os
import sys
import subprocess
from pathlib import Path
from tests.helpers import run_generator

class TestBanditDashboard(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_bandit_dashboard_generated_in_guided_mode(self):
        """P0.1: Guided project contains bandit_dashboard.py."""
        package_name = "bandit_dashboard_pkg"
        output_dir = self.test_dir / "bandit_dashboard_project"

        run_generator(
            project_name="Bandit Dashboard Project",
            package_name=package_name,
            output_dir=output_dir,
            experience_mode="2" # Guided
        )

        dashboard_path = output_dir / f"src/{package_name}/bandit_dashboard.py"
        self.assertTrue(dashboard_path.exists())

        content = dashboard_path.read_text()
        self.assertIn("Bandit Lab Dashboard", content)
        self.assertIn("st.line_chart", content)
        self.assertIn("pd.read_csv", content)

        # Check lab.py wiring
        lab_py_content = (output_dir / f"src/{package_name}/lab.py").read_text()
        self.assertIn('subparsers.add_parser("bandit-dashboard"', lab_py_content)
        self.assertIn('def run_bandit_dashboard():', lab_py_content)

    def test_bandit_dashboard_omitted_in_minimal_mode(self):
        """P0.5: Minimal project does not contain Bandit dashboard."""
        package_name = "minimal_no_bandit_dashboard"
        output_dir = self.test_dir / "minimal_no_bandit_dashboard"

        run_generator(
            project_name="Minimal No Bandit",
            package_name=package_name,
            output_dir=output_dir,
            experience_mode="1" # Minimal
        )

        dashboard_path = output_dir / f"src/{package_name}/bandit_dashboard.py"
        self.assertFalse(dashboard_path.exists())

    def test_bandit_dashboard_handles_missing_data(self):
        """P0.4: Dashboard shows message when data is missing."""
        package_name = "bandit_missing_data"
        output_dir = self.test_dir / "bandit_missing_data"

        run_generator(
            project_name="Bandit Missing Data",
            package_name=package_name,
            output_dir=output_dir,
            experience_mode="2"
        )

        dashboard_path = output_dir / f"src/{package_name}/bandit_dashboard.py"
        content = dashboard_path.read_text()

        # Verify it has the warning for missing data
        self.assertIn("missing_data", content)
        self.assertIn("run_instruction", content)
        self.assertIn("configs/bandit_results.json", content)

    def test_bandit_dashboard_imports_and_structure(self):
        """Verify the generated dashboard has correct imports and main function."""
        package_name = "bandit_structure"
        output_dir = self.test_dir / "bandit_structure"

        run_generator(
            project_name="Bandit Structure",
            package_name=package_name,
            output_dir=output_dir,
            experience_mode="2"
        )

        dashboard_path = output_dir / f"src/{package_name}/bandit_dashboard.py"

        # We can't easily run it because of streamlit dependency,
        # but we can check the syntax
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(dashboard_path)],
            capture_output=True
        )
        self.assertEqual(result.returncode, 0, f"Syntax error in generated dashboard: {result.stderr}")

if __name__ == "__main__":
    unittest.main()
