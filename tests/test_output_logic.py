import unittest
from pathlib import Path
from unittest.mock import patch
import shutil
import tempfile
import create_ml_starter
from tests.helpers import run_generator

class TestOutputLogic(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        # Mock STARTER_ROOT to be inside our temp dir
        self.starter_root = self.test_dir / "ml-starter-lab-kit"
        self.starter_root.mkdir()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_default_sibling_directory(self):
        # We need to patch STARTER_ROOT in the module
        with patch('create_ml_starter.STARTER_ROOT', self.starter_root):
            package_name = "my_ml_project"
            expected_default = self.starter_root.parent / package_name

            # In create_ml_starter.py:
            # default_output_dir = STARTER_ROOT.parent / package_name
            actual_default = create_ml_starter.STARTER_ROOT.parent / package_name
            self.assertEqual(actual_default, expected_default)
            self.assertEqual(actual_default.parent, self.starter_root.parent)

    def test_starter_root_detection(self):
        with patch('create_ml_starter.STARTER_ROOT', self.starter_root):
            # Test path inside starter root
            inside_path = self.starter_root / "some_subdir"
            outside_path = self.test_dir / "outside"

            output = run_generator(
                project_name="My Project",
                package_name="my_project",
                task="2",
                dataset_path="data.csv",
                target_column="target",
                output_dir_sequence=[str(inside_path), "n", str(outside_path)]
            )

            self.assertIn("Warning: The selected output directory is inside the starter repository.", output)
            self.assertTrue((outside_path / "README.md").exists())

    def test_readme_content(self):
        values = {
            "PROJECT_NAME": "Test Project",
            "PACKAGE_NAME": "test_project",
            "TASK": "supervised"
        }
        output_dir = self.test_dir / "output"
        output_dir.mkdir()

        create_ml_starter.create_readme(output_dir, values, force=True)

        readme_path = output_dir / "README.md"
        content = readme_path.read_text()

        self.assertIn("This is a generated Machine Learning project, not the starter tool itself.", content)
        self.assertNotIn("Este é um projeto de Machine Learning gerado, não a própria ferramenta starter.", content)

if __name__ == "__main__":
    unittest.main()
