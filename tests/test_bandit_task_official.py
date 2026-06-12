import unittest
import shutil
import tempfile
import json
from pathlib import Path
from tests.helpers import run_generator

class TestBanditTaskOfficial(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_bandit_task_in_wizard_and_generation(self):
        """P0.1, P0.2: Wizard exposes Bandit option and generates relevant assets."""
        project_name = "official_bandit"
        package_name = "official_bandit_pkg"
        output_dir = self.test_dir / project_name

        # task="6" is the new Bandit option
        output = run_generator(
            project_name=project_name,
            package_name=package_name,
            task="6",
            output_dir=output_dir,
            experience_mode="1", # minimal
            include_demo="y"
        )

        # P0.1: Check wizard exposure in output
        self.assertIn("6. bandit        - Multi-Armed Bandit / adaptive decisions", output)

        # P0.2: Check relevant assets
        self.assertTrue((output_dir / "src" / package_name / "bandit_lab.py").exists())
        self.assertTrue((output_dir / "docs/mab-lab.md").exists())
        self.assertTrue((output_dir / "configs/bandit_config.json").exists())

        # Check config.json task
        with open(output_dir / "configs/config.json") as f:
            config = json.load(f)
            self.assertEqual(config["project"]["task"], "bandit")
            self.assertEqual(config["target"]["column"], "reward")

        # Check README next steps
        readme_content = (output_dir / "README.md").read_text()
        self.assertIn("Bandit Lab (adaptive decisions)", readme_content)
        self.assertIn("python -m official_bandit_pkg.lab bandit", readme_content)

    def test_supervised_no_bandit_by_default(self):
        """P0.3: Non-bandit tasks (like supervised) do not receive Bandit assets by default."""
        project_name = "supervised_no_bandit"
        package_name = "supervised_no_bandit_pkg"
        output_dir = self.test_dir / project_name

        run_generator(
            project_name=project_name,
            package_name=package_name,
            task="2", # supervised
            output_dir=output_dir,
            experience_mode="1",
            optional_profile="1" # minimal
        )

        self.assertFalse((output_dir / "src" / package_name / "bandit_lab.py").exists())
        self.assertFalse((output_dir / "docs/mab-lab.md").exists())

    def test_bandit_task_config_roundtrip(self):
        """P0.4: New task value round-trips through config."""
        project_name = "config_roundtrip"
        output_dir = self.test_dir / project_name

        run_generator(
            project_name=project_name,
            task="6", # bandit
            output_dir=output_dir
        )

        config_path = output_dir / "configs/config.json"
        with open(config_path) as f:
            config = json.load(f)
            self.assertEqual(config["project"]["task"], "bandit")

    def test_bandit_vs_non_bandit_distinct(self):
        """P0.5: Bandit vs non-bandit projects differ in expected content."""
        bandit_dir = self.test_dir / "bandit_proj"
        supervised_dir = self.test_dir / "supervised_proj"

        run_generator(task="6", output_dir=bandit_dir, package_name="b_pkg")
        run_generator(task="2", output_dir=supervised_dir, package_name="s_pkg")

        # Bandit has bandit_lab.py, supervised doesn't (by default)
        self.assertTrue((bandit_dir / "src/b_pkg/bandit_lab.py").exists())
        self.assertFalse((supervised_dir / "src/s_pkg/bandit_lab.py").exists())

        # Check train.py content
        bandit_train = (bandit_dir / "src/b_pkg/train.py").read_text()
        supervised_train = (supervised_dir / "src/s_pkg/train.py").read_text()

        self.assertIn("bandit_placeholder", bandit_train)
        self.assertNotIn("bandit_placeholder", supervised_train)

if __name__ == "__main__":
    unittest.main()
