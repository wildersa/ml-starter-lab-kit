import unittest
import shutil
import tempfile
from pathlib import Path
from tests.helpers import run_generator

class TestPythonVersionInstructions(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_python_3_14_instructions_en(self):
        # language="1" is English
        # python_profile="2" is Python 3.14 (modern)
        output = run_generator(
            language="1",
            project_name="ver_test_en",
            package_name="ver_test_en",
            task="1",
            output_dir=self.test_dir,
            python_profile="2",
            include_pyproject="y"
        )

        # 1. Check START_HERE.md
        guide_path = self.test_dir / "START_HERE.md"
        self.assertTrue(guide_path.exists())
        guide_content = guide_path.read_text()

        self.assertIn("python3.14 -m venv .venv", guide_content)
        self.assertIn("py -3.14 -m venv .venv", guide_content)

        # 2. Check README.md
        readme_path = self.test_dir / "README.md"
        self.assertTrue(readme_path.exists())
        readme_content = readme_path.read_text()

        self.assertIn("python3.14 -m venv .venv", readme_content)
        self.assertIn("py -3.14 -m venv .venv", readme_content)
        self.assertIn("python --version", readme_content)

    def test_python_3_14_instructions_pt(self):
        # language="2" is Portuguese
        # python_profile="2" is Python 3.14 (modern)
        output = run_generator(
            language="2",
            project_name="ver_test_pt",
            package_name="ver_test_pt",
            task="1",
            output_dir=self.test_dir,
            python_profile="2",
            include_pyproject="y"
        )

        # 1. Check START_HERE.md
        guide_path = self.test_dir / "START_HERE.md"
        self.assertTrue(guide_path.exists())
        guide_content = guide_path.read_text()

        self.assertIn("python3.14 -m venv .venv", guide_content)
        self.assertIn("py -3.14 -m venv .venv", guide_content)

        # 2. Check README.md (which is the localized README in this project structure)
        readme_path = self.test_dir / "README.md"
        self.assertTrue(readme_path.exists())
        readme_content = readme_path.read_text()

        self.assertIn("python3.14 -m venv .venv", readme_content)
        self.assertIn("py -3.14 -m venv .venv", readme_content)
        self.assertIn("python --version", readme_content)

if __name__ == "__main__":
    unittest.main()
