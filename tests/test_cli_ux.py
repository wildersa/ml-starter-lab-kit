import unittest
import os
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch
from tests.helpers import run_generator

class TestCLIUX(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_sections_and_panels_presence(self):
        output = run_generator(
            project_name="ux_project",
            task="2",
            output_dir=self.test_dir
        )

        # Check for section labels
        self.assertIn("--- 1. Project basics ---", output)
        self.assertIn("--- 2. Dataset and target ---", output)
        self.assertIn("--- 3. Problem framing ---", output)
        self.assertIn("--- 4. Environment ---", output)
        self.assertIn("--- 5. Optional tools ---", output)
        self.assertIn("--- 6. Output location ---", output)
        self.assertIn("--- 7. Final summary ---", output)

        # Check for educational panels
        self.assertIn("[Supervised Learning]", output)
        self.assertIn("In supervised learning, you need a 'target' column", output)
        self.assertIn("[Problem Framing]", output)
        self.assertIn("[Next steps]", output)

    def test_output_directory_options(self):
        # Test "Current directory" option (Option 1)
        # We need a custom run_generator or a way to pass specific inputs
        from ml_starter_generator.cli import main
        import io

        # Mocking inputs for option 1 (current directory)
        # Sequence:
        # 0. Language: "1" (en)
        # Project basics
        # 1. Project name: "current_dir_proj"
        # 2. Package name: "current_dir_pkg"
        # 3. Task: "1" (generic)
        # Dataset and target
        # 4. Dataset path: "data.csv"
        # (Target column skipped for generic)
        # Problem framing
        # 5-10. goal, priority, error, size, baseline, note: all ""
        # Environment
        # 11. Create pyproject: "y"
        # 12. Python profile: "1"
        # 13. ML basics: "n"
        # 14. Torch variant: "1"
        # Optional tools
        # 15. Create docs: "y"
        # 16. Optional profile: "1" (minimal)
        # Output location
        # 17. Output choice: "1" (current directory)
        # 18. Overwrite: "y"
        # Final summary
        # 19. Confirm: "y"
        inputs = [
            "1",
            "current_dir_proj", "current_dir_pkg", "1",
            "data.csv",
            "", "", "", "", "", "",
            "y", "1", "n", "1",
            "y", "1",
            "1",
            "y", "y"
        ]

        with patch("ml_starter_generator.cli.input", side_effect=inputs):
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                with patch("pathlib.Path.cwd", return_value=self.test_dir):
                    main()
                    output = fake_out.getvalue()

        self.assertTrue((self.test_dir / "README.md").exists())
        self.assertIn("Destination: " + str(self.test_dir.resolve()), output)

    def test_no_color_fallback(self):
        with patch.dict(os.environ, {"NO_COLOR": "1"}):
            output = run_generator(
                project_name="no_color_proj",
                output_dir=self.test_dir
            )
            # ANSI escape codes look like \033[...m
            self.assertNotIn("\033[94m", output)
            self.assertIn("--- 1. Project basics ---", output)

    def test_final_summary_content(self):
        output = run_generator(
            project_name="summary_proj",
            package_name="summary_pkg",
            task="supervised",
            dataset_path="my_data.csv",
            target_column="my_target",
            output_dir=self.test_dir
        )

        self.assertIn("Project name:      summary_proj", output)
        self.assertIn("Package name:      summary_pkg", output)
        self.assertIn("ML Task:           supervised", output)
        self.assertIn("Dataset path:      my_data.csv", output)
        self.assertIn("Target column:     my_target", output)
        self.assertIn("Output directory:  " + str(self.test_dir.resolve()), output)

if __name__ == "__main__":
    unittest.main()
