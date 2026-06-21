import unittest
import shutil
import tempfile
import os
from pathlib import Path
from unittest.mock import patch
from tests.helpers import run_generator

class TestCLISummaryOrder(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.project_name = "order_proj"
        self.package_name = "order_pkg"

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_summary_order_with_pyproject(self):
        output = run_generator(
            project_name=self.project_name,
            package_name=self.package_name,
            output_dir=self.test_dir,
            include_pyproject="y",
            optional_profile="2" # recommended (includes EDA)
        )

        # Verify concise steps
        self.assertIn("Open START_HERE.md", output)
        self.assertIn("Start with the learning trail", output)

    def test_summary_order_without_pyproject(self):
        output = run_generator(
            project_name=self.project_name,
            package_name=self.package_name,
            output_dir=self.test_dir,
            include_pyproject="n"
        )

        # Verify concise steps even without pyproject
        self.assertIn("Open START_HERE.md", output)
        self.assertIn("Start with the learning trail", output)

    def test_summary_current_directory(self):
        # Using option 1 for output location: current directory
        # We need to mock Path.cwd() to be self.test_dir
        with patch("pathlib.Path.cwd", return_value=self.test_dir):
            output = run_generator(
                project_name=self.project_name,
                package_name=self.package_name,
                output_dir_sequence=["1"], # Select current directory
                include_pyproject="y"
            )

        self.assertIn("Open START_HERE.md", output)

    def test_summary_pt_br(self):
        output = run_generator(
            language="2",
            project_name=self.project_name,
            package_name=self.package_name,
            output_dir=self.test_dir,
            include_pyproject="y"
        )

        self.assertIn("Abra START_HERE.md", output)
        self.assertIn("Comece pela trilha de aprendizado", output)

if __name__ == "__main__":
    unittest.main()
