import unittest
import shutil
import tempfile
import json
import io
from pathlib import Path
from unittest.mock import patch
from ml_starter_generator.cli import main

class TestNumericSelection(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_bandit_numeric_selection(self):
        """Verify that bandit prompts accept numeric selection."""
        project_name = "bandit_numeric"
        package_name = "bandit_pkg"
        output_dir = self.test_dir / project_name

        # Inputs for the generator using numbers where possible
        inputs = [
            "1", # Language: 1 (English)
            project_name,
            package_name,
            "6", # Task: 6 (bandit)
            "1", # Experience mode: 1 (minimal)
            "data/raw/dataset.csv",
            "reward", # Target column
            "n", # Include demo: no
            "1", # Bandit Action: 1 (offer/product)
            "2", # Bandit Reward: 2 (conversion)
            "2", # Bandit Context: 2 (contextual)
            "1", # Bandit Delay: 1 (immediate)
            "3", # Bandit Baseline: 3 (random)
            "Test note", # Domain note
            "n", # Create env files: no
            "n", # Create docs: no
            "1", # Optional profile: 1 (minimal)
            "4", # Output location: 4 (custom)
            str(output_dir),
            "y", # Overwrite
            "y"  # Create project files
        ]

        with patch("ml_starter_generator.cli.input", side_effect=inputs):
            with patch("sys.stdout", new=io.StringIO()):
                main()

        # Verify problem_profile.json
        profile_path = output_dir / "configs/problem_profile.json"
        self.assertTrue(profile_path.exists())
        with open(profile_path, "r") as f:
            profile = json.load(f)

        self.assertEqual(profile["bandit_action"], "offer/product")
        self.assertEqual(profile["bandit_reward"], "conversion")
        self.assertEqual(profile["bandit_context"], "contextual bandit (uses features)")
        self.assertEqual(profile["bandit_delay"], "immediate")
        self.assertEqual(profile["bandit_baseline"], "random")

    def test_bandit_custom_option_numeric(self):
        """Verify that picking 'custom' by number prompts for custom value."""
        project_name = "bandit_custom"
        package_name = "bandit_pkg"
        output_dir = self.test_dir / project_name

        inputs = [
            "1", # Language: 1 (English)
            project_name,
            package_name,
            "6", # Task: 6 (bandit)
            "1", # Experience mode: 1 (minimal)
            "data/raw/dataset.csv",
            "reward",
            "n",
            "4", # Bandit Action: 4 (custom)
            "my_custom_action", # The custom value
            "5", # Bandit Reward: 5 (custom metric)
            "my_custom_reward", # The custom value
            "1", # Context: simple
            "1", # Delay: immediate
            "4", # Baseline: 4 (custom)
            "my_custom_baseline", # The custom value
            "Test note",
            "n", "n", "1", "4", str(output_dir), "y", "y"
        ]

        with patch("ml_starter_generator.cli.input", side_effect=inputs):
            with patch("sys.stdout", new=io.StringIO()):
                main()

        profile_path = output_dir / "configs/problem_profile.json"
        with open(profile_path, "r") as f:
            profile = json.load(f)

        self.assertEqual(profile["bandit_action"], "my_custom_action")
        self.assertEqual(profile["bandit_reward"], "my_custom_reward")
        self.assertEqual(profile["bandit_baseline"], "my_custom_baseline")

    def test_invalid_selection_retry(self):
        """Verify that invalid numeric selection shows error and retries."""
        project_name = "retry_project"
        package_name = "retry_pkg"
        output_dir = self.test_dir / project_name

        inputs = [
            "1",
            project_name,
            package_name,
            "99", # Invalid task
            "2",  # Correct task (supervised)
            "1",
            "data.csv",
            "target",
            "n",
            "1", # goal
            "1", # priority
            "1", # error
            "1", # size
            "y", # baseline
            "",  # note
            "n", "n", "1", "4", str(output_dir), "y", "y"
        ]

        with patch("ml_starter_generator.cli.input", side_effect=inputs):
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()

        self.assertIn("Invalid option", output)
        self.assertTrue((output_dir / "configs/config.json").exists())

    def test_default_with_enter(self):
        """Verify that pressing Enter uses the default option."""
        project_name = "default_project"
        package_name = "default_pkg"
        output_dir = self.test_dir / project_name

        inputs = [
            "", # Language default (English)
            project_name,
            package_name,
            "", # Task default (supervised)
            "", # Experience mode default (minimal)
            "data.csv",
            "", # Target default (target)
            "", # Demo default (no)
            "", # Goal default
            "", # Priority default
            "", # Error cost default
            "", # Size default
            "", # Baseline default
            "", # Note default
            "n", "n", "1", "4", str(output_dir), "y", "y"
        ]

        with patch("ml_starter_generator.cli.input", side_effect=inputs):
            main()

        config_path = output_dir / "configs/config.json"
        with open(config_path, "r") as f:
            config = json.load(f)
        self.assertEqual(config["project"]["task"], "supervised")

if __name__ == "__main__":
    unittest.main()
