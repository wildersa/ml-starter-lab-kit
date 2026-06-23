import unittest
import shutil
import tempfile
import json
from pathlib import Path
from tests.helpers import run_generator

class TestExperienceMode(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_minimal_starter_config(self):
        run_generator(
            project_name="minimal_proj",
            experience_mode="1", # minimal
            output_dir=self.test_dir,
            include_docs="n",
            include_ml_basics="n",
            optional_profile="1" # minimal
        )

        config_path = self.test_dir / "configs/config.json"
        self.assertTrue(config_path.exists())
        with open(config_path) as f:
            config = json.load(f)
            self.assertEqual(config["learning"]["enabled"], False)
            self.assertEqual(config["learning"]["mode"], "minimal")

        # Verify minimal stays clean
        self.assertFalse((self.test_dir / "docs").exists())
        self.assertFalse((self.test_dir / "src/minimal_proj/eda.py").exists())
        self.assertFalse((self.test_dir / "src/minimal_proj/advisor.py").exists())

    def test_guided_learning_mode_config_and_prerequisites(self):
        # Guided Learning Mode (experience_mode="2")
        # should force docs, ML basics, EDA and Advisor.
        run_generator(
            project_name="guided_proj",
            experience_mode="2", # guided
            output_dir=self.test_dir,
            include_docs="n",   # Should be overridden
            include_ml_basics="n", # Should be overridden
            optional_profile="1" # Should be overridden
        )

        config_path = self.test_dir / "configs/config.json"
        self.assertTrue(config_path.exists())
        with open(config_path) as f:
            config = json.load(f)
            self.assertEqual(config["learning"]["enabled"], True)
            self.assertEqual(config["learning"]["mode"], "guided")

        # Verify Guided enables prerequisites
        self.assertTrue((self.test_dir / "docs").exists())
        self.assertTrue((self.test_dir / "src/guided_proj/eda.py").exists())
        self.assertTrue((self.test_dir / "src/guided_proj/advisor.py").exists())

        # Verify ML basics were forced in requirements
        req_ml = self.test_dir / "requirements-ml.txt"
        self.assertTrue(req_ml.exists())

    def test_guided_learning_custom_profile_override(self):
        # Even with custom profile, guided should force eda and advisor
        optionals = ["n"] * 17
        run_generator(
            project_name="guided_custom",
            experience_mode="2",
            output_dir=self.test_dir,
            optional_profile="4",
            optionals=optionals
        )

        pkg_path = self.test_dir / "src/guided_custom"
        self.assertTrue((pkg_path / "eda.py").exists())
        self.assertTrue((pkg_path / "advisor.py").exists())

    def test_minimal_starter_with_defaults(self):
        # Simulation of pressing Enter for everything after selecting Minimal Starter
        from ml_starter_generator.cli import main
        import io
        from unittest.mock import patch

        # Sequence:
        # 1. Language: "1" (en)
        # Project basics
        # 2. Project name: "min_default"
        # 3. Package name: "" (default min_default)
        # 4. Task: "2" (supervised)
        # 5. Experience mode: "1" (minimal)
        # Dataset and target
        # 6. Dataset path: "" (default data/raw/dataset.csv)
        # 7. Target column: "" (default target)
        # 8. Include demo: "" (default n)
        # Problem framing
        # 9-14. goal, priority, error, size, baseline, note: all ""
        # Environment
        # 15. Create pyproject: "" (default y)
        # 16. Python profile: "" (default 1)
        # 17. ML basics: "" (default n in minimal mode)
        # 18. MLflow: "" (default n)
        # 19. Torch: "" (default 1 - none)
        # Optional tools
        # 20. Create docs: "" (default n in minimal mode)
        # 21. Optional profile: "" (default 1 in minimal mode)
        # Output location
        # 22. Output choice: "4" (custom)
        # 23. Custom path: self.test_dir
        # 24. Overwrite: "y"
        # Final summary
        # 25. Confirm: "y"
        inputs = [
            "1",
            "min_default", "", "2", "1",
            "", "", "",
            "", "", "", "", "", "",
            "", "", "", "", "",
            "", "",
            "4", str(self.test_dir), "y", "y"
        ]

        with patch("ml_starter_generator.cli.input", side_effect=inputs):
            with patch("sys.stdout", new=io.StringIO()):
                main()

        pkg_path = self.test_dir / "src/min_default"

        # Verify it is clean
        self.assertFalse((self.test_dir / "docs").exists())
        self.assertFalse((pkg_path / "eda.py").exists())
        self.assertFalse((pkg_path / "advisor.py").exists())
        self.assertFalse((self.test_dir / "requirements-ml.txt").exists())

if __name__ == "__main__":
    unittest.main()
