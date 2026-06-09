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

        # Verify Navigation
        self.assertIn("cd ", output)

        # Verify setup steps
        setup_steps = ["python -m venv .venv", "pip install -r requirements.txt", "pip install -e ."]
        module_commands = [f"python -m {self.package_name}.lab eda", f"python -m {self.package_name}.lab train"]

        for step in setup_steps:
            self.assertIn(step, output)

        # Verify order: navigation -> setup -> data/config -> run
        # We need to find the occurrence within [Next steps] panel
        next_steps_output = output.split("[Next steps]")[1]

        nav_idx = next_steps_output.find("cd ")
        setup_idx = next_steps_output.find("python -m venv .venv")
        install_idx = next_steps_output.find("pip install -e .")
        # Find the line with the dataset path
        dataset_line_idx = next_steps_output.find(self.test_dir.name + "/data/raw/dataset.csv")
        if dataset_line_idx == -1:
            # Fallback for how it might be displayed
            dataset_line_idx = next_steps_output.find("data/raw/dataset.csv")

        data_cmd_idx = next_steps_output.find(f"python -m {self.package_name}.lab eda")

        self.assertLess(nav_idx, setup_idx, "Navigation should be before setup")
        self.assertLess(setup_idx, install_idx, "Venv setup should be before editable install")
        self.assertLess(install_idx, dataset_line_idx, "Editable install should be before dataset instructions")
        self.assertLess(dataset_line_idx, data_cmd_idx, "Dataset instructions should be before running data module")

    def test_summary_order_without_pyproject(self):
        output = run_generator(
            project_name=self.project_name,
            package_name=self.package_name,
            output_dir=self.test_dir,
            include_pyproject="n"
        )

        # Should NOT promise editable install
        self.assertNotIn("pip install -e .", output)
        self.assertNotIn("python -m venv .venv", output)

        # P0.5: It must either show the correct PYTHONPATH=src style alternative or explicitly state that package setup is required
        self.assertIn("PYTHONPATH=src", output)
        self.assertIn("required", output.lower())

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

        self.assertIn("You are already in the project directory", output)
        self.assertNotIn("cd ", output.split("[Next steps]")[1])

    def test_summary_pt_br(self):
        output = run_generator(
            language="2",
            project_name=self.project_name,
            package_name=self.package_name,
            output_dir=self.test_dir,
            include_pyproject="y"
        )

        self.assertIn("Navegue para o diretório do projeto", output)
        self.assertIn("Configure o ambiente", output)
        self.assertIn("Instale o pacote em modo editável", output)

if __name__ == "__main__":
    unittest.main()
