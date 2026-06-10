import unittest
import shutil
import tempfile
import os
import sys
import subprocess
import json
import pandas as pd
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

        # P0.5: lab.py should NOT contain bandit-dashboard
        lab_py_path = output_dir / f"src/{package_name}/lab.py"
        lab_py_content = lab_py_path.read_text()
        self.assertNotIn('bandit-dashboard', lab_py_content)
        self.assertNotIn('run_bandit_dashboard', lab_py_content)

    def test_bandit_dashboard_data_loading(self):
        """P0.2, P0.4: Test the data-loading function directly."""
        # Mock streamlit to avoid requiring it for just testing the data loader
        from unittest.mock import MagicMock
        if 'streamlit' not in sys.modules:
            sys.modules['streamlit'] = MagicMock()

        package_name = "bandit_loader"
        output_dir = self.test_dir / "bandit_loader"

        run_generator(
            project_name="Bandit Loader",
            package_name=package_name,
            output_dir=output_dir,
            experience_mode="2"
        )

        # We need to import the function from the generated file
        # We add the src dir to sys.path
        sys.path.insert(0, str(output_dir / "src"))
        try:
            import importlib
            dashboard_module = importlib.import_module(f"{package_name}.bandit_dashboard")
            get_bandit_outputs = dashboard_module.get_bandit_outputs

            # Case 1: Missing files (P0.4)
            status, results, df = get_bandit_outputs(output_dir)
            self.assertEqual(status, "MISSING")
            self.assertIsNone(results)
            self.assertIsNone(df)

            # Case 2: Valid files (P0.2)
            configs_dir = output_dir / "configs"
            reports_dir = output_dir / "reports"
            configs_dir.mkdir(parents=True, exist_ok=True)
            reports_dir.mkdir(parents=True, exist_ok=True)

            sample_results = {"random": {"total_reward": 10, "average_reward": 0.1, "cumulative_regret": 5, "best_arm_selection_rate": 0.3}}
            with open(configs_dir / "bandit_results.json", "w") as f:
                json.dump(sample_results, f)

            sample_history = pd.DataFrame({
                "round": [1, 2],
                "policy": ["random", "random"],
                "cumulative_reward": [1, 2],
                "cumulative_regret": [0.5, 1.0],
                "selected_arm": ["A", "B"]
            })
            sample_history.to_csv(reports_dir / "bandit-history.csv", index=False)

            status, results, df = get_bandit_outputs(output_dir)
            self.assertEqual(status, "OK")
            self.assertEqual(results, sample_results)
            self.assertIsNotNone(df)
            self.assertEqual(len(df), 2)

            # Case 3: Error (corrupt JSON)
            with open(configs_dir / "bandit_results.json", "w") as f:
                f.write("invalid json")

            status, results, df = get_bandit_outputs(output_dir)
            self.assertEqual(status, "ERROR")

        finally:
            sys.path.pop(0)
            # Remove module from cache to avoid issues with other tests
            if f"{package_name}.bandit_dashboard" in sys.modules:
                del sys.modules[f"{package_name}.bandit_dashboard"]

    def test_bandit_dashboard_syntax(self):
        """Verify the generated dashboard has correct syntax."""
        package_name = "bandit_syntax"
        output_dir = self.test_dir / "bandit_syntax"

        run_generator(
            project_name="Bandit Syntax",
            package_name=package_name,
            output_dir=output_dir,
            experience_mode="2"
        )

        dashboard_path = output_dir / f"src/{package_name}/bandit_dashboard.py"
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(dashboard_path)],
            capture_output=True
        )
        self.assertEqual(result.returncode, 0, f"Syntax error in generated dashboard: {result.stderr}")

if __name__ == "__main__":
    unittest.main()
