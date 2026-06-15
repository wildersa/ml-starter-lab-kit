import unittest
import shutil
import tempfile
import json
import io
from pathlib import Path
from unittest.mock import patch
from ml_starter_generator.cli import main

class TestBanditWizard(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_bandit_wizard_prompts(self):
        """Verify that selecting Bandit shows Bandit-specific prompts and skips generic ones."""
        project_name = "bandit_project"
        package_name = "bandit_pkg"
        output_dir = self.test_dir / project_name

        # Inputs for the generator
        inputs = [
            "1", # Language: English
            project_name,
            package_name,
            "6", # Task: bandit
            "1", # Experience mode: minimal
            "data/raw/dataset.csv",
            "reward", # Target column (default is reward for bandit)
            "n", # Include demo: no
            "offer/product", # Bandit Action
            "click", # Bandit Reward
            "contextual bandit (uses features)", # Bandit Context
            "immediate", # Bandit Delay
            "random", # Bandit Baseline
            "Test bandit note", # Domain note
            "n", # Create env files: no
            "n", # Create docs: no
            "1", # Optional profile: minimal
            "4", # Output location: custom
            str(output_dir),
            "y", # Overwrite
            "y"  # Create project files
        ]

        with patch("ml_starter_generator.cli.input", side_effect=inputs):
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()

        # Check if Bandit-specific prompts are present
        self.assertIn("What action should the system choose?", output)
        self.assertIn("What reward will be observed?", output)
        self.assertIn("Is there user/event context?", output)
        self.assertIn("Is the reward immediate or delayed?", output)
        self.assertIn("What initial baseline should be used?", output)

        # Check if generic prompts are NOT present
        self.assertNotIn("Main goal?", output)
        self.assertNotIn("What matters most?", output)
        self.assertNotIn("Which error is more costly?", output)
        self.assertNotIn("Expected dataset size?", output)

        # Verify problem_profile.json
        profile_path = output_dir / "configs/problem_profile.json"
        self.assertTrue(profile_path.exists())
        with open(profile_path, "r") as f:
            profile = json.load(f)

        self.assertEqual(profile["goal"], "Multi-Armed Bandit / adaptive decisions")
        self.assertEqual(profile["bandit_action"], "offer/product")
        self.assertEqual(profile["bandit_reward"], "click")
        self.assertEqual(profile["bandit_context"], "contextual bandit (uses features)")
        self.assertEqual(profile["bandit_delay"], "immediate")
        self.assertEqual(profile["bandit_baseline"], "random")
        self.assertEqual(profile["domain_note"], "Test bandit note")

    def test_non_bandit_wizard_keeps_generic_prompts(self):
        """Verify that selecting a non-Bandit task keeps generic prompts."""
        project_name = "supervised_project"
        package_name = "supervised_pkg"
        output_dir = self.test_dir / project_name

        inputs = [
            "1", # Language: English
            project_name,
            package_name,
            "2", # Task: supervised
            "1", # Experience mode: minimal
            "data/raw/dataset.csv",
            "target", # Target column
            "n", # Include demo: no
            "predict a category", # Main goal
            "learning/experimentation", # Priority
            "not sure", # Error cost
            "not sure", # Dataset size
            "y", # Simple baseline
            "Test supervised note", # Domain note
            "n", # Create env files: no
            "n", # Create docs: no
            "1", # Optional profile: minimal
            "4", # Output location: custom
            str(output_dir),
            "y", # Overwrite
            "y"  # Create project files
        ]

        with patch("ml_starter_generator.cli.input", side_effect=inputs):
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()

        # Check if generic prompts are present
        self.assertIn("Main goal?", output)
        self.assertIn("What matters most?", output)

        # Check if Bandit-specific prompts are NOT present
        self.assertNotIn("What action should the system choose?", output)

    def test_bandit_default_target_column(self):
        """Verify that the target column defaults to 'reward' for Bandit."""
        project_name = "bandit_default_target"
        package_name = "bandit_default_pkg"
        output_dir = self.test_dir / project_name

        # We simulate pressing Enter for target column
        inputs = [
            "1", # Language: English
            project_name,
            package_name,
            "6", # Task: bandit
            "1", # Experience mode: minimal
            "data/raw/dataset.csv",
            "", # Target column: default (should be reward)
            "n", # Include demo: no
            "", # Bandit Action: default
            "", # Bandit Reward: default
            "", # Bandit Context: default
            "", # Bandit Delay: default
            "", # Bandit Baseline: default
            "", # Domain note: default
            "n", # Create env files: no
            "n", # Create docs: no
            "1", # Optional profile: minimal
            "4", # Output location: custom
            str(output_dir),
            "y", # Overwrite
            "y"  # Create project files
        ]

        with patch("ml_starter_generator.cli.input", side_effect=inputs):
            main()

        config_path = output_dir / "configs/config.json"
        self.assertTrue(config_path.exists())
        with open(config_path, "r") as f:
            config = json.load(f)

        self.assertEqual(config["target"]["column"], "reward")

if __name__ == "__main__":
    unittest.main()
